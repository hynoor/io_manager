# A class implements the main manipulations of I/O relevant, the interface class to ouside caller
from io_engine.io_operator import IoOperator
from io_host import IoHost
import select
import time
from collections import defaultdict


class IoManager:
    """
    IoManager manager IoHost and IoEngine objects
    """
    __slots__ = (
        '_hosts',
        '_engine',
        '_command',
    )

    def __init__(self, io_engine=None, io_hosts=None):
        """Initialized the IoManager
        :param io_engine : <IoEngine> the underlying io engine object
        :param io_hosts   : <List> a list of ip addresses of IoHost
        :return          : <None>
        """
        self._engine = io_engine
        self._hosts = set()
        self._command = 'python /tmp/test_file.py'

    def load_engine(self, io_engine=None):
        """ load specific io engine
        :param io_engine : <IoEngine> the underlying io engine object
        :return          : <None>
        """
        assert isinstance(io_engine, IoOperator), "Error: Parameter 'io_engine' is required as IoEngine object"
        self._engine = io_engine

    def add_host(self, host_ip=None):
        """ add io host 
        :param host_ip : <IoHost> the underlying io host object to issue I/O
        :return        : <None>
        """
        assert host_ip is not None, "Error: Parameter 'io_engine' is required as IoEngine object"
        host = IoHost(ip=host_ip)
        self._hosts.add(host)

    def remove_host(self, host_ip=None):
        """ add io host
        :param host_ip : <IoHost> the underlying io host to be removed from host pool
        :return        : <None>
        """
        assert host_ip is not None, "Error: Parameter 'io_engine' is required as IoEngine object"
        host = IoHost(ip=host_ip)
        if host in self._hosts:
            self._hosts.remove(host)
        del host

    def start_io(self, workers=1, output=False, async=False, timeout=7200):
        """ io executor
        :param workers : <Number> the underlying io host object to issue I/O
        :param output  : <Boolean> if print stdout during waiting
        :param async   : <Bool> If asynchronously execute the io, if async is False, run host one by one
        :param timeout : <Number> timeout to be waited
        :return        : return a task object to track the IO jobs running on remote hosts
        """
        task = []
        # assign the jobs to works in round robin fashion
        workers_per_host = workers // len(self._hosts)
        remain_workers = workers % len(self._hosts)
        allocated_workers = []
        for w in range(len(self._hosts)):
            allocated_workers.append(workers_per_host)
        for r in range(remain_workers):
            allocated_workers[r] += 1
        for h, w in zip(self._hosts, allocated_workers):
            task = task + h.run_async(workers=w, task=self._command)
        task_obj = IoTask(jobs=task)
        if async:
            return task_obj
        else:
            task_obj.wait(timeout=timeout, output=output, interval=3)


class IoTask:
    """
    Class IoTask
    """
    __slots__ = (
        '_status',
        '_done',
        '_running',
        '_job_status'
        '_host',
        '_exception',
        '_output_size',
        '_output',
    )

    def __init__(self, jobs=None):
        """ Initialize object
        """
        assert isinstance(jobs, list), RuntimeError("Error: Parameter list requires a list type")
        self._done = list()
        self._job_status = defaultdict()
        # initializing coming jobs ...
        for j, h in jobs:
            # data structure: {channel : [host_ip, status]}
            self._job_status[j] = [h, 'running']
        self._exception = list()
        self._output_size = 1024
        self._output = list()

    def _update(self):
        """ refresh task status (running|completed|failed)
        :return: running|completed|failed
        """
        for job in self._job_status.keys():
            if job.exit_status_ready():
                self._job_status[job][1] = 'completed'
        self._done = [job for job in self._job_status.keys() if self._job_status[job][1] == 'completed']
        if len([job for job in self._job_status.keys() if self._job_status[job][1] == 'running']) > 0:
            status = 'running'
        elif len([job for job in self._job_status.keys() if self._job_status[job][1] == 'running']) == 0:
            status = 'completed'
        else:
            raise RuntimeError("ERROR: Invalid status!")

        return status

    def wait(self, output=False, timeout=7200, interval=30):
        """ Wai the task till completed
        :param timeout  : <number> the timeout to wait
        :param output   : <Boolean> if print output during waiting
        :param interval : <number> the interval for polling status
        :return:
        """
        # blocking mode doesn't have to use even to all callback just simply waiting
        duration_left = timeout
        while duration_left > 0:
            if self.status == 'running':
                if output:
                    print(self.stdout)
                time.sleep(interval)
                duration_left -= interval
            else:
                return
        raise RuntimeError("Error: Task didn't completed in %d timeout!" % timeout)

    @property
    def running_job(self):
        """
        Number of jobs are running
        :return:
        """
        # update status
        self._update()
        return len([job for job in self._job_status.keys() if self._job_status[job][1] == 'running'])

    @property
    def stdout(self, mode='increment'):
        """
        Output of running task
        :param mode : Complete or incremental
        :return: stdout
        """
        self._update()
        if len(self._done) > 0:
            r, w, x = select.select(self._done, [], [], 3)
            if len(r) > 0:
                for job in self._done:
                    res = job.recv(self._output_size)
                    if res != '':
                        self._output.append(res)
                        if mode == 'increment':
                            return res
        return self._output

    @property
    def stderr(self):
        """
        Output of running task
        :return: output
        """
        self._update()
        for job in self._done:
            if job.recv_stderr_ready():
                self._exception.append(job.recv_stderr(self._output_size))
        return self._exception

    @property
    def status(self):
        """
        Task overall status
        :return: (running|completed|failed)
        """
        return self._update()


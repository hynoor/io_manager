# A class implements the main manipulations of I/O relevant, the interface class to ouside caller
from io_engine import IoEngine
from io_host import IoHost
import select


class IoManager:
    """
    IoManager manager IoHost and IoEngine objects
    """
    __slots__ = (
        '_hosts',
        '_engine',
    )

    def __init__(self, io_engine=None, io_hosts=None):
        """Initialized the IoManager
        :param io_engine : <IoEngine> the underlying io engine object
        :param io_hosts   : <List> a list of ip addresses of IoHost
        :return          : <None>
        """
        self._engine = io_engine
        self._hosts = set()

    def load_engine(self, io_engine=None):
        """ load specific io engine
        :param io_engine : <IoEngine> the underlying io engine object
        :return          : <None>
        """
        assert isinstance(io_engine, IoEngine), "Error: Parameter 'io_engine' is required as IoEngine object"
        self._engine = io_engine

    def add_host(self, host_ip=None):
        """ add io host 
        :param host_ip : <IoHost> the underlying io host object to issue I/O
        :return        : <None>
        """
        assert host_ip is not None, "Error: Parameter 'io_engine' is required as IoEngine object"
        host = IoHost(ip=host_ip)
        self._hosts.add(host)
        
    def start_io(self, workers=1, async=False):
        """ io executor
        :param workers : <Number> the underlying io host object to issue I/O
        :param async   : <Bool> If asynchronously execute the io, if async is False, run host one by one
        :return        : return a task object to track the IO jobs running on remote hosts
        """
        task = []
        if async:
            for h in self._hosts:
                task = task + h.run_async(workers=workers, task='python /tmp/test_file.py')
            return IoTask(jobs=task)

        #h.run(workers=workers, task='python /tmp/test_file.py', background=False)


class IoTask:
    """
    Class IoTask
    """
    __slots__ = (
        '_status',
        '_finished_jobs',
        '_running_jobs',
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
        self._finished_jobs = list()
        self._job_status = dict()
        for idx, job in enumerate(jobs, start=1):
            self._job_status[idx] = [job, 'running']
        self._exception = []
        self._output_size = 1024
        self._output = []

    def _update(self):
        """ Query task status (running|finished|failed)
        :return: running|finished|failed
        """
        status = 'running'
        for idx, job in self._job_status.items():
            if job[0].exit_status_ready():
                self._job_status[idx][1] = 'finished'
                self._finished_jobs.append(job[0])
        if len(self._finished_jobs) < len(self._job_status.keys()):
            status = 'running'
        elif len(self._finished_jobs) == len(self._job_status.keys()):
            status = 'finished'

        if status == 'finished':
            r, w, x = select.select(self._finished_jobs, [], [])
            if len(r) > 0:
                for job in self._finished_jobs:
                    res = job.recv(self._output_size)
                    self._output.append(res)

            for job in self._finished_jobs:
                if job.recv_stderr_ready():
                    self._exception.append(job.recv_stderr(self._output_size))
        return status

    @property
    def running_job(self):
        """
        Number of jobs are running
        :return:
        """
        # update status
        self._update()
        return len([job for job in self._job_status.values() if job[1] == 'running'])

    @property
    def output(self):
        """
        Output of running task
        :return: output
        """
        self._update()
        return self._output

    @property
    def exception(self):
        """
        Output of running task
        :return: output
        """
        self._update()
        return self._exception

    @property
    def status(self):
        """
        Task overall status
        :return: (running|finished|failed)
        """
        return self._update()





# a class wrappers the host used to issue I/O reques
import paramiko
import os.path

class IoHost:
    """ IoHost class
    """
    __slots__ = (
        '_name',
        '_ip',
        '_port',
        '_user',
        '_password',
        '_workers',
        '_output_size',
        '_disks',
        '_jobs',
    )

    def __init__(self, ip=None, port=22, user='root', password='Password123!'):
        """ initializer
        :param ip       : host ip address
        :param port     : port number to be connected
        :param user     : user to be used for connection
        :param password : password to be used for connection
        """
        self._ip = ip
        self._port = port
        self._user = user
        self._disks = set()
        self._jobs = None
        self._password = password
        self._output_size = 1024
        
        self._client = paramiko.SSHClient()
        self._client.load_system_host_keys()

        self._client.set_missing_host_key_policy(paramiko.MissingHostKeyPolicy())
        self._client.connect(self._ip, self._port, self._user, self._password)

    def run_async(self, workers=1, command=None):
        """ execute given task asynchronously
        :param workers: number of processes to be launched
        :param task: specific task to be executed
        :return: a list of fd to track job status
        """
        if command is None:
            raise RuntimeError("Error: Parameter 'task' is required")
        self._reallocate(number_jobs=workers)
        channels = []
        allocated_jobs = self._reallocate()
        for _, d in zip(allocated_jobs, self._disks) :
            channel = self._client.get_transport().open_session()
            channel.exec_command(command)
            self._jobs.add(channel)
            channels.append((channel, self._ip))

        return channels

    def _reallocate(self, number_jobs=1):
        """ allocate jobs to targets storage objects in round-robin fashion
        """
        assert len(self._disks) > 0, RuntimeError("No storage target was added to host")
        jobs_per_target = number_jobs // len(self._disks)
        remain_jobs = number_jobs % len(self._disks)
        allocated_jobs = []
        for _ in range(number_jobs):
            allocated_jobs.append(jobs_per_target)
        for r in range(remain_jobs):
            allocated_jobs[r] += 1
        return allocated_jobs

    def add_disk(self, path=None):
        """ add storage to host
        :param disk: disk object to be added for I/O
        :return: 
        """
        self._disks.add(BlockStoreage(path=path))

    def remove_disk(self, disk=None):
        """
        :param disk: disk object to be removed from host's disk pool
        :return:
        """
        disk = BlockStoreage(path=path)
        if disk in self._disks():
            self._disks.remove(disk)
        else:
            del disk

    @property
    def ip_address(self):
        """ ip address
        :return: ip
        """
        return self._ip
    
    @property
    def name(self):
        """ host name
        :return: name
        """
        return self._ip


class IoStorage:
    """
    Class IoStorage
    """

    __slots__ = (
        '_path',
        '_size',
    )

    def __init__(self, path=None):
        """
        Initializing
        :param path: storage accessing path
        """
        self._path = path
        self._size = os.path.getsize(self._path)

    @property
    def size(self):
        """
        property 'size'
        :return: size
        """
        return self._size

    def path(self):
        """
        property 'path'
        :return: path
        """
        return self._path


class BlockStoreage(IoStorage):
    """
    Class block device
    """



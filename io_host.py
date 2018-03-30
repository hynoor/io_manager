# a class wrappers the host used to issue I/O reques
import paramiko
import select


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
        '_output_size'
    )

    def __init__(self, ip=None, port=22, user='root', password='hynoor'):
        """ initializer
        :param ip       : host ip address
        :param port     : port number to be connected
        :param user     : user to be used for connection
        :param password : password to be used for connection
        """
        self._ip = ip
        self._port = port
        self._user = user
        self._password = password
        self._output_size = 1024
        
        self._client = paramiko.SSHClient()
        self._client.load_system_host_keys()

        self._client.set_missing_host_key_policy(paramiko.MissingHostKeyPolicy())
        self._client.connect(self._ip, self._port, self._user, self._password)

    def run(self, workers=1, task=None, background=True):
        """ execute given task
        :param workers : number of processes to be launched
        :param task    : specific task to be executed
        :return        : results of finished task
        """
        if task is None:
            raise RuntimeError("Error: Parameter 'task' is required")
        channels = []
        exceptions = []
        output = []
        for _ in xrange(workers):
            channel = self._client.get_transport().open_session()
            channels.append(channel)
            channel.exec_command(task)
        while True:
            done = True
            for ch in channels:
                if not ch.exit_status_ready():
                    done = False
            if done:
                break
        r, w, x = select.select(channels, [], [])
        if len(r) > 0:
            for ch in channels:
                res = ch.recv(self._output_size)
                output.append(res)
                if not background:
                    print(res)
        if ch.recv_stderr_ready():
            exceptions.append(ch.recv_stderr(self._output_size))
        if len(exceptions) > 0:
            raise IOError(exceptions)
        return output
        
    def run_async(self, workers=1, task=None):
        """ execute given task asynchronously 
        :param workers: number of processes to be launched
        :param task: specific task to be executed
        :return: a list of fd to track job status
        """
        if task is None:
            raise RuntimeError("Error: Parameter 'task' is required")
        channels = []
        for _ in xrange(workers):
            channel = self._client.get_transport().open_session()
            channels.append(channel)
            channel.exec_command(task)

        return channels

    def add_disk(self, disk=None):
        """
        :param disk: disk object 
        :return: 
        """

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



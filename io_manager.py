# A class implements the main manipulations of I/O relevant, the interface class to ouside caller
from io_engine import IoEngine

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
        self._hosts.add(io_hosts)

    def load_engine(self, io_engine=None):
        """ load specific io engine
        :param io_engine : <IoEngine> the underlying io engine object
        :return          : <None>
        """
        assert isinstance(io_engine, IoEngine), "Error: Parameter 'io_engine' is required as IoEngine object"
        self._engine = io_engine

    def add_host(self, io_host=None):
        """ add io host 
        :param io_host : <IoHost> the underlying io host object to issue I/O
        :return        : <None>
        """
        assert io_host is not None, "Error: Parameter 'io_engine' is required as IoEngine object"
        self._hosts.add(io_host)
        
    def start_io(self, workers=1, async=False):
        """ io executor
        :param workers : <Number> the underlying io host object to issue I/O
        :param async   : <Bool> If asynchronously execute the io
        :return        : <IoTask> IoTask object to track the IO jobs running on remote hosts
        """
        pass




# a class wrappers underlying io tools to drive the IO  purposely

class IoEngine:
    """ IoEngine class
    """

    __slots__ = (
        'io_size',
        'seek',
        'data_pattern',
    )

    def __init__(self, engine='fio'):
        """ io engine initializer
        """
        pass
    
    def configure(self, io_params=None):
        pass


class BlockEngine(IoEngine):
    """ IO engine for block
    """

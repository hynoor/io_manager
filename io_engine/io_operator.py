# a class wrappers underlying io tools to drive the IO  purposely

class IoOperator:
    """ IoOperator class
    """

    __slots__ = (
        'io_size',
        'seek',
        'data_pattern',
        'direct_io',
        'verify',
        'engine',
        'scenario'
    )

    def __init__(self, engine='fio'):
        """ io engine initializer
        :param tool : underlying I/O tools to be used
        """
        pass

    def configure(self, scenario='baseline', io_params=None):
        """
        Configure engine too specific scenario or highly customized one
        :param io_params: Feature centric I/O scenario to be used, should be one of following:
                          baseline | compress | dedupe | pattern-detect
        :param io_params: highly customizable I/O scenarios
        :return:
        """
        pass

    def compress_io(self, io_size='4k', compress_ration=80):
        """
        Set compress I/O scenario with user given parameters
        :param io_size         : Size of each I/O to be issued
        :param compress_ration : Compressible ratio of given data
        :return                : *none*
        """
        pass

    def dedup_io(self, io_size='4k', dedup_count=1000):
        """
        Set dedupe I/O scenario with user given parameters
        :param io_size         : Size of each I/O to be issued
        :param compress_ration : Compressible ratio of given data
        :return                : *none*
        """
        pass

    def baseline_io(self, io_size='4k', data_pattern='random', workers=1, execution_mode='process'):
        """
        set a base line io scenarios to exercise the staroge target in steady and continuese flux
        :param io_size        : Size of each I/O to be issued
        :param data_pattern   : Data pattern to be used in each IO
        :param workers        : The scale of concurrency or parallelism
        :param execution_mode : The mode of each work to be executed, thread or process

        :return               : A dictionary stored every required parameter-value pairs
        """
        commands = dict() 
        # implemetation of the baseline io scenario
        return commands













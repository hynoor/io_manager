import time
from io_manager import IoManager


user = 'root'
passwd = 'hynoor'
ip = '172.16.21.131'


def test():
    io_mgr = IoManager()
    io_mgr.add_host(host_ip=ip)
    task = io_mgr.start_io(workers=10, async=True)
    while task.status == 'running':
        print("OUTPUT: %s" % task.stdout)
        print("still running")
        time.sleep(1)
    print("OUTPUT: %s" % task.stdout)


if __name__ == '__main__':
    test()
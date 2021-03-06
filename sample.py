import time
from io_manager import IoManager


user = 'root'
passwd = 'Password123!'
ip1 = '10.207.84.35'
ip2 = '10.207.80.31'


def test():
    io_mgr = IoManager()
    io_mgr.add_host(host_ip=ip1)
    io_mgr.add_host(host_ip=ip2)
    hosts = io_mgr.get_hosts()
    for h in hosts:
        h.add_disk("/dev/sda")
    task = io_mgr.start_io(workers=20, output=True, async=True)
    while task.status == 'running':
        print("OUTPUT: %s" % task.stdout)
        print("still running")
        time.sleep(1)
    print("OUTPUT: %s" % task.stdout)


if __name__ == '__main__':
    test()

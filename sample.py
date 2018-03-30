import time
from io_manager import IoManager


user = 'root'
passwd = 'hynoor'
ip = '172.16.21.131'


def test():
    io_mgr = IoManager()
    io_mgr.add_host(host_ip=ip)
    task = io_mgr.start_io(workers=4, async=True)
    while task.status == 'running':
        print("STATUS: %s" % task.status)
        print("OUTPUT: %s" % task.output)
        print("RUNNING: %d" % task.running_job)
        time.sleep(1)
    print("STATUS: %s" % task.status)
    print("OUTPUT: %s" % task.output)
    print("RUNNING: %d" % task.running_job)


if __name__ == '__main__':
    test()
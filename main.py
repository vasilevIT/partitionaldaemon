"""
 Created by PyCharm Community Edition.
 User: Anton Vasiliev <bysslaev@gmail.com>
 Date: 31/03/2018
 Time: 04:31

"""

from daemon import *

from dbhelper import dbhelper


class PartitionDaemon(Daemon):
    def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        super().__init__(pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null')
        self.db = dbhelper()
        self.db.connect()

    def run(self):
        i = 0
        self.db.clearDb()
        while True:
            self.db.insertItem()
            i += 1
            if (i % 1000) == 0:
                logger.info(str(i) + " rows inserted.")

    def stop(self):
        super().stop()
        self.db.createView()


if __name__ == "__main__":
    daemon = PartitionDaemon('/tmp/python-partition_daemon.pid')
    if len(sys.argv) == 2:
        logger.info('{} {}'.format(sys.argv[0], sys.argv[1]))

        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        elif 'status' == sys.argv[1]:
            daemon.status()
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        logger.warning('show cmd deamon usage')
        print("Usage: {} start|stop|restart".format(sys.argv[0]))
        sys.exit(2)

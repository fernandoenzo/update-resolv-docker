# encoding:utf-8
from argparse import ArgumentParser

from update import UpdateDaemon, UserStatics


class UpdateParser:
    def __init__(self):
        self.parser = ArgumentParser(description="Keeps the docker's resolv.conf file updated with the host's one.")
        self.parser.add_argument('--start', action='store_true', default=False)
        self.parser.add_argument('--stop', action='store_true', default=False)
        self.parser.add_argument('--restart', action='store_true', default=False)
        self.args = vars(self.parser.parse_args())


if __name__ == "__main__":
    daemon = UpdateDaemon(UserStatics.PID_FILE)

    parser = UpdateParser()
    start = parser.args['start']
    stop = parser.args['stop']
    restart = parser.args['restart']

    if start:
        daemon.start()
    elif stop:
        daemon.stop()
    elif restart:
        daemon.restart()
    else:
        daemon.start()

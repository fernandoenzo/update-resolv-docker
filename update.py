# encoding:utf-8

import os
import subprocess
from pathlib import Path
from time import sleep

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from daemon import Daemon


class UserStatics:
    RESOLV_HOST_DIR = '/tmp/host/'
    RESOLV_FILE = None
    PID_FILE = '/tmp/update-resolv.pid'

    @classmethod
    def set_resolv_file(cls):
        ruta = Path('/tmp/docker-openvpn/name')
        resolv = [archivo for archivo in ruta.iterdir()][0]
        cls.RESOLV_FILE = resolv.name


class UpdateDaemon(Daemon):
    def run(self):
        UserStatics.set_resolv_file()
        observer = Observer()
        observer.schedule(EventModifyReload(), UserStatics.RESOLV_HOST_DIR)
        observer.start()
        while True:
            sleep(100)


class EventModifyReload(FileSystemEventHandler):
    def __init__(self):
        self.resolv_path = os.path.join(UserStatics.RESOLV_HOST_DIR, UserStatics.RESOLV_FILE)

    def update_resolv(self):
        subprocess.run('cat {0} > {1}'.format(self.resolv_path, '/etc/resolv.conf'), shell=True)

    def on_modified(self, event):
        if event.src_path == self.resolv_path:
            self.update_resolv()

    def on_moved(self, event):
        if event.dest_path == self.resolv_path:
            self.update_resolv()

#!/usr/bin/env python
import os
import json
import time
import configparser
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class FileEventHandler(FileSystemEventHandler):
    def __init__(self, src, dst):
        FileSystemEventHandler.__init__(self)
        self.src = src
        self.dst = dst


    def on_modified(self, event):
        for filename in os.listdir(self.src):
            src = self.src + '/' + filename
            dst = self.dst + '/' + filename
            print("File has been modified or added at " + src)
            os.rename(src, dst)
            print("File has been moved to " + dst)


def main():
    print("Initializing py-file-mover service by D3PSI...")
    try:

        print("Loading and parsing configuration file...")
        config = configparser.ConfigParser()
        config.read('py-file-mover.conf')
        for section in config.sections():
            src = section['SourceDir']
            dst = section['DestinationDir']
            print(src)
            print(dst)
            handler = FileEventHandler(src, dst)
            observer = Observer()
            observer.schedule(handler, src, recursive=True)
            observer.start()
            while True:
                time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    except OSError:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()

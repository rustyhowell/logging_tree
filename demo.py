#!/usr/bin/env python3

import threading
import time
import logging
from logging import LogRecord

thread = None
run = True
loggers = []


class MyFilter(logging.Filter):
    def filter(self, record):
        assert isinstance(record, LogRecord)
        if 'foobar' in record.msg:
            return True


        return False

def start():
    global thread, run
    run = True
    thread = threading.Thread(target=__worker)
    thread.start()


def stop():
    global thread, run
    run = False
    if thread:
        thread.join()
    thread = None

def __worker():
    print("starting worker")
    while run:
        for lvl in range(10, 60, 10):
            for logger in loggers:
                logger.log(lvl, logger.name)
            time.sleep(0.2)
        time.sleep(1)


def setup():
    global loggers
    logging.basicConfig(filename='demo.log', format='%(name)s %(levelname)s %(message)s')

    for n in ['a.b','a.b.c.d','a.b.e','a.f','x.y']:
        loggers.append(logging.getLogger(n))



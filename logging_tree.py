#!/usr/bin/env python3

import logging
import asciitree
from collections import OrderedDict as OD


colors = {
          'red': (1, 31),
          'green': (1, 32),
          'yellow': (0, 33),
          'blue': (1, 34),
          'magenta': (1, 35),
          'cyan': (1, 36),
          'white': (0, 37),
          }

def _color(txt, color):
    bold, idx = colors[color]
    return '\033[{};{}m{}\033[0m;'.format(bold, idx, txt)


def _getHandlers(logger):
    d = OD()
    if isinstance(logger, logging.Logger):
        for h in logger.handlers:
            name = type(h).__name__
            d[_color('<{}, level={}>'.format(name, h.level), 'blue')] = {}

    return  d


def _make_tree_label(logger):
    level = { 0  : 'notset',
              10 : 'debug',
              20 : 'info',
              30 : 'warning',
              40 : 'error',
              50 : 'critical',
              }
    label = _color('<Logger {}, level={},{} >'.format(logger.name, logger.level, level[logger.level]), 'green')

    return label

def print_logging_tree(handlers=True):
    root = _getHandlers(logging.root) if handlers else {}
    tree = OD()
    tree[_make_tree_label(logging.root)] = root
    loggers = {'root': root}

    keys = sorted(logging.Logger.manager.loggerDict.keys())
    for loggername in keys:
        parent = '.'.join(loggername.split('.')[:-1])
        if parent == '':
            parent = 'root'

        parentlogger = loggers[parent]
        logger = logging.Logger.manager.loggerDict[loggername]
        if isinstance(logger, logging.Logger):
            cur_colorname = _make_tree_label(logger)
        elif isinstance(logger, logging.PlaceHolder):
            cur_colorname = _color('<Logger {}>'.format(loggername), 'white')
        else:
            assert False

        cur_logger = _getHandlers(logger) if handlers else {}
        parentlogger[cur_colorname] = cur_logger
        loggers[loggername] = cur_logger

    LA = asciitree.LeftAligned()
    print('')
    print(LA(tree))
    print('')

if __name__ == '__main__':

    logging.basicConfig()

    logging.getLogger('a.b')
    logging.getLogger('a.b.c.d').addHandler(logging.FileHandler('/tmp/my.log'))
    logging.getLogger('a.b').addHandler(logging.StreamHandler())
    logging.getLogger('a.f')

    import logging.handlers  # More handlers are in here
    logging.getLogger('x.y').addHandler(logging.handlers.DatagramHandler('192.168.1.3', 9999))

    print_logging_tree(handlers=True)

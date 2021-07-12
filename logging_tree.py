#!/usr/bin/env python3

import logging
import asciitree
from collections import OrderedDict as OD


__colors = {
          'red': (1, 31),
          'green': (1, 32),
          'yellow': (0, 33),
          'blue': (1, 34),
          'magenta': (1, 35),
          'cyan': (1, 36),
          'white': (0, 37),
          }

def __color(txt, color):
    bold, idx = __colors[color]
    return '\033[{};{}m{}\033[0m'.format(bold, idx, txt)


def __getFilters(obj):
    d = OD()
    for o in obj.filters:
        d[__color('<Filter {} >'.format(o), 'yellow')] = {}
    return d

def __getHandlers(logger):
    d = OD()

    if isinstance(logger, logging.Logger):
        for f in logger.filters:
            d[__color('<Filter {} >'.format(f), 'yellow')] = {}

        for h in logger.handlers:
            name = type(h).__name__
            filters = __getFilters(h)
            d[__color('<{}, level={}>'.format(name, h.level), 'blue')] = filters

    return  d


def __make_tree_label(logger):
    level = { 0  : 'notset',
              10 : 'debug',
              20 : 'info',
              30 : 'warning',
              40 : 'error',
              50 : 'critical',
              }
    label = __color('<Logger {}, level={},{} >'.format(logger.name, logger.level, level[logger.level]), 'green')

    return label

def print_logging_tree(include_handlers=True):
    """ Prints the hierarchy of loggers, handlers, and filters

    Args:
        include_handlers:  Include logging handlers and filters in the output

    """
    root = __getHandlers(logging.root) if include_handlers else {}
    tree = OD()
    tree[__make_tree_label(logging.root)] = root
    loggers = {'root': root}

    keys = sorted(logging.Logger.manager.loggerDict.keys())
    for loggername in keys:
        parent = '.'.join(loggername.split('.')[:-1])
        if parent == '':
            parent = 'root'

        parentlogger = loggers[parent]
        logger = logging.Logger.manager.loggerDict[loggername]
        if isinstance(logger, logging.Logger):
            cur_colorname = __make_tree_label(logger)
        elif isinstance(logger, logging.PlaceHolder):
            cur_colorname = __color('<Logger {}>'.format(loggername), 'white')
        else:
            assert False

        cur_logger = __getHandlers(logger) if include_handlers else {}
        parentlogger[cur_colorname] = cur_logger
        loggers[loggername] = cur_logger

    LA = asciitree.LeftAligned()
    print('\n{}\n'.format(LA(tree)))


if __name__ == '__main__':

    logging.basicConfig()

    logging.getLogger('a.b')
    logging.getLogger('a.b.c.d').addHandler(logging.FileHandler('/tmp/my.log'))
    logging.getLogger('a.b.c.d').handlers[0].addFilter(logging.Filter())

    logging.getLogger('a.b').addHandler(logging.StreamHandler())
    logging.getLogger('a.f')

    import logging.handlers  # More handlers are in here
    logging.getLogger('x.y').addHandler(logging.handlers.DatagramHandler('192.168.1.3', 9999))
    logging.root.addFilter('a.b.c')

    print_logging_tree(include_handlers=True)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 46elks AB <hello@46elks.com>
# Developed in 2016 by Emil Tullstedt <emil@46elks.com>
# Licensed under the MIT License
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import math

def bytes_to_human(size):
    si_bytes = ('B', 'kB', 'MB', 'GB', 'TB', 'PB', 'ZB', 'YB')
    si_magnitude = int(math.floor(math.log10(size)) // 3)
    return '%.2f %s' % (size / pow(10, si_magnitude*3), si_bytes[si_magnitude])

def duration_to_human(length):
    seconds = length % 60
    minutes = length // 60
    hours = minutes // 60
    if hours:
        return '%dh%dm%ds' % (hours, minutes, seconds)
    elif minutes:
        return '%dm%ds' % (minutes, seconds)
    else:
        return '%ds' % (seconds)

def credits_to_currency(credits, currency):
    value = credits / 10000.
    return '%s %.4f' % (currency, value)

def kv_print(key, value, indentlevel = 1, show_empty = False):
    if not show_empty and value == None:
        return
    tabular = '\t' * indentlevel
    print('%s%-15s %-20s' % (tabular, key, value))


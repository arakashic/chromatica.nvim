# ============================================================================
# FILE: util.py
# AUTHOR: Yanfei Guo <yanf.guo at gmail.com>
# License: MIT license
# based on original version by Shougo Matsushita <Shougo.Matsu at gmail.com>
# ============================================================================

import json
import re
import os
import sys
import unicodedata
import glob

def set_default(vim, var, val):
    return vim.call('chromatica#util#set_default', var, val)

def globruntime(runtimepath, path):
    ret = []
    for rtp in re.split(',', runtimepath):
        ret += glob.glob(rtp + '/' + path)
    return ret

def debug(vim, expr):
    if hasattr(vim, 'out_write'):
        string = (expr if isinstance(expr, str) else str(expr))
        return vim.out_write('[chromatica] ' + string + '\n')
    else:
        vim.call('chromatica#util#print_debug', expr)


def error(vim, expr):
    if hasattr(vim, 'err_write'):
        string = (expr if isinstance(expr, str) else str(expr))
        return vim.err_write('[chromatica] ' + string + '\n')
    else:
        vim.call('chromatica#util#print_error', expr)


def error_tb(vim, msg):
    for line in traceback.format_exc().splitlines():
        error(vim, str(line))
    error(vim, '%s.  Use :messages for error details.' % msg)


def error_vim(vim, msg):
    throwpoint = vim.eval('v:throwpoint')
    if throwpoint != '':
        error(vim, 'v:throwpoint = ' + throwpoint)
    exception = vim.eval('v:exception')
    if exception != '':
        error(vim, 'v:exception = ' + exception)
    error_tb(vim, msg)

def load_external_module(file, module):
    current = os.path.dirname(os.path.abspath(file))
    module_dir = os.path.join(os.path.dirname(current), module)
    if module_dir not in sys.path:
        sys.path.insert(0, module_dir)


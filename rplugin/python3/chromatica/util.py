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
    if vim.vars['chromatica#enable_log']:
        try:
            json_data = json.dumps(str(expr).strip())
        except Exception:
            vim.command('echomsg string(\'' + str(expr).strip() + '\')')
        else:
            vim.command('echomsg string(\'' + escape(json_data) + '\')')

    else:
        error(vim, "not in debug mode, but debug called")


def error(vim, msg):
    vim.call('chromatica#util#print_error', msg)

def load_external_module(file, module):
    current = os.path.dirname(os.path.abspath(file))
    module_dir = os.path.join(os.path.dirname(current), module)
    sys.path.insert(0, module_dir)


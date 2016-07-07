# ============================================================================
# FILE: neovim_helper.py
# AUTHOR: Yanfei Guo <yanf.guo at gmail.com>
# License: MIT license
# ============================================================================

import neovim

class NvimHelper(object):
    """neovim help class for easy access to neovim functionalities"""

    def __init__(self, vim):
        self.__vim = vim

    def echo(self, s):
        """echo command"""
        self.__vim.command("echo '%s'" % s)

    def echomsg(self, s):
        """echom[sg] command"""
        self.__vim.command("echomsg '%s'" % s)

    def line(self, p):
        """line function"""
        return self.__vim.call("line", p)

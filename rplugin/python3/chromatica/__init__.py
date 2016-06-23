# ============================================================================
# FILE: chromatica.py
# AUTHOR: Yanfei Guo <yanf.guo at gmail.com>
# License: MIT license
# ============================================================================

import neovim

from chromatica import logger
from chromatica.chromatica import Chromatica

@neovim.plugin
class ChromaticaPlugin(object):
    def __init__(self, vim):
        self.__vim = vim

    @neovim.function("_chromatica", sync=True)
    def init_chromatica(self, args):
        self.__chromatica = Chromatica(self.__vim)
        self.__vim.vars["chromatica#_channel_id"] = self.__vim.channel_id

    @neovim.rpc_export('chromatica_enable_logging', sync=True)
    def enable_logging(self, level, logfile):
        logger.setup(self.__vim, level, logfile)
        self.__chromatica.debug_enabled = True

    @neovim.rpc_export("chromatica_highlight", sync=False)
    def highlight(self, context):
        context["rpc"] = "chromatica_highlight"
        self.__chromatica.highlight(context)

    @neovim.rpc_export("chromatica_parse", sync=False)
    def parse(self, context):
        context["rpc"] = "chromatica_parse"
        self.__chromatica.parse(context)

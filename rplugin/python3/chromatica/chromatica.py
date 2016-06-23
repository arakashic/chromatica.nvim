# ============================================================================
# FILE: chromatica.py
# AUTHOR: Yanfei Guo <yanf.guo at gmail.com>
# License: MIT license
# based on original version by BB Chung <afafaf4 at gmail.com>
# ============================================================================

from chromatica import logger
from chromatica import syntax
from chromatica.util import load_external_module
from chromatica.compile_args_database import CompileArgsDatabase

current = __file__

load_external_module(current, "")
from clang import cindex

import os
import re

class Chromatica(logger.LoggingMixin):

    """Chromatica Core """

    def __init__(self, vim):
        self.__vim = vim
        self.__runtimepath = ""
        self.name = "core"
        self.mark = "[Chromatica Core]"
        self.library_path = self.__vim.vars["chromatica#libclang_path"]
        self.occurrence_pri = self.__vim.vars["chromatica#occurrence_priority"]
        self.syntax_pri = self.__vim.vars["chromatica#syntax_priority"]
        self.global_args = self.__vim.vars["chromatica#global_args"]
        self.ctx = {}

        if not cindex.Config.loaded:
            if os.path.isdir(os.path.abspath(self.library_path)):
                cindex.Config.set_library_path(self.library_path)
            else:
                cindex.Config.set_library_file(self.library_path)
            cindex.Config.set_compatibility_check(False)

        self.args_db = CompileArgsDatabase(self.__vim.current.buffer.name,\
                self.global_args)
        self.idx = cindex.Index.create()

    def get_unsaved_buffer(self, filename):
        buf_idx = self.ctx[filename]["bufnr"] - 1
        return [(self.__vim.buffers[buf_idx].name, "\n".join(self.__vim.buffers[buf_idx]))]

    def get_buf(self, filename):
        buf_idx = self.ctx[filename]["bufnr"] - 1
        return self.__vim.buffers[buf_idx]

    def get_bufname(self, filename):
        return self.get_buf(filename).name

    def parse(self, context):
        ret = False
        self.debug("parse context: %s" % context)
        # check if context is already in ctx db
        filename = context["filename"]
        if filename not in self.ctx:
            self.ctx[filename] = context
            # check if context is has the right filetype
            filetype = self.get_buf(filename).options["filetype"].strip(".")[0]
            if filetype not in ["c", "cpp"]:
                del(self.ctx[filename])
                return ret

            self.ctx[filename]["args"] = \
                self.args_db.get_args_filename(context["filename"])
            self.debug("file: %s, args: %s" % (filename, self.ctx[filename]["args"]))
            self.ctx[filename]["tu"] = self.idx.parse(self.get_bufname(filename), \
                self.ctx[filename]["args"], \
                self.get_unsaved_buffer(filename), \
                options=cindex.TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD)
            ret = True
        elif self.ctx[filename]["changedtick"] != context["changedtick"]:
            self.ctx[filename]["tu"].reparse(\
                self.get_unsaved_buffer(filename), \
                options=cindex.TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD)
            self.ctx[filename]["changedtick"] = context["changedtick"]
            ret = True

        if ret:
            self.highlight(context)

        return ret

    def highlight(self, context):
        """backend of highlight event"""
        self.debug("highlight context: %s" % context)
        filename = context["filename"]
        lbegin, lend = context["range"]
        row, col = context["position"]
        highlight_tick = context["highlight_tick"]

        if highlight_tick != self.__vim.current.buffer.vars["highlight_tick"]:
            return

        if filename not in self.ctx:
            self.parse(context)

        tu = self.ctx[filename]['tu']

        symbol = syntax.get_symbol_from_loc(tu, self.get_bufname(filename), row, col)
        syn_group, occurrence = syntax.get_highlight(tu, self.get_bufname(filename), \
                lbegin, lend, symbol)
        self.debug(syn_group)
        self.debug(occurrence)

        for hl_group in syn_group:
            for pos in syn_group[hl_group]:
                row = pos[0] - 1
                col_start = pos[1] - 1
                col_end = col_start + pos[2]
                self.get_buf(filename).add_highlight(hl_group, row, col_start, col_end,\
                        self.syntax_pri)

        # self.__vim.current.buffer.add_highlight()

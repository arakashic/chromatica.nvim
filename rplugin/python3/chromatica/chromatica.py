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
import time

class Chromatica(logger.LoggingMixin):

    """Chromatica Core """

    def __init__(self, vim):
        self.__vim = vim
        self.__runtimepath = ""
        self.name = "core"
        self.mark = "[Chromatica Core]"
        self.library_path = self.__vim.vars["chromatica#libclang_path"]
        self.syntax_src_id = self.__vim.vars["chromatica#syntax_src_id"]
        self.global_args = self.__vim.vars["chromatica#global_args"]
        self.delay_time = self.__vim.vars["chromatica#delay_ms"] / 1000.0
        self.ctx = {}
        self.parse_options = cindex.TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD \
                           + cindex.TranslationUnit.PARSE_INCOMPLETE
        if self.__vim.vars["chromatica#use_pch"]:
            self.parse_options += cindex.TranslationUnit.PARSE_PRECOMPILED_PREAMBLE \
                               + cindex.TranslationUnit.CREATE_PREAMBLE_ON_FIRST_PARSE

        if not cindex.Config.loaded:
            if os.path.isdir(os.path.abspath(self.library_path)):
                cindex.Config.set_library_path(self.library_path)
            else:
                cindex.Config.set_library_file(self.library_path)
            cindex.Config.set_compatibility_check(False)

        self.args_db = CompileArgsDatabase(self.__vim.current.buffer.name,\
                self.global_args)
        self.idx = cindex.Index.create()

    def vim_print(self, s):
        self.__vim.command("echo '%s'" % s)

    @classmethod
    def is_supported_filetype(self, filetype):
        if len(filetype) > 0 and filetype.split(".")[0] in ["c", "cpp", "objc", "objcpp"]:
            return True
        return False

    def get_unsaved_buffer(self, filename):
        return [(self.__vim.current.buffer.name, "\n".join(self.__vim.current.buffer))]

    def parse(self, context):
        ret = False
        # check if context is already in ctx db
        filename = context["filename"]
        if filename not in self.ctx:
            self.ctx[filename] = context
            # check if context is has the right filetype
            buffer = self.__vim.current.buffer
            if not Chromatica.is_supported_filetype(buffer.options["filetype"]):
                del(self.ctx[filename])
                return ret
            self.ctx[filename]["buffer"] = buffer

            self.ctx[filename]["args"] = \
                self.args_db.get_args_filename(filename)
            self.info("filename: %s, args: %s" % (filename, self.ctx[filename]["args"]))
            t_start = time.clock()
            tu = self.idx.parse(buffer.name, \
                self.ctx[filename]["args"], \
                self.get_unsaved_buffer(filename), \
                options=self.parse_options)

            t_elapse = time.clock() - t_start
            self.debug("[profile] idx.parse: %2.10f" % t_elapse)
            if not tu:
                del(self.ctx[filename])
                return ret

            self.ctx[filename]["tu"] = tu
            ret = True
        elif context["changedtick"] != self.ctx[filename]["changedtick"]:
            t_start = time.clock()
            self.ctx[filename]["tu"].reparse(\
                self.get_unsaved_buffer(filename), \
                options=self.parse_options)
            t_elapse = time.clock() - t_start
            self.debug("[profile] idx.reparse: %2.10f" % t_elapse)
            self.ctx[filename]["changedtick"] = context["changedtick"]
            ret = True

        if ret:
            self.highlight(context)

        return ret

    def delayed_parse(self, context):
        """delayed parse for responsive mode"""
        filename = context["filename"]
        # context must already in self.ctx
        buffer = self.__vim.current.buffer
        if filename not in self.ctx \
                or "tu" not in self.ctx[filename] \
                or not Chromatica.is_supported_filetype(buffer.options["filetype"]):
            return

        time.sleep(self.delay_time)

        if context["changedtick"] < self.__vim.eval("b:changedtick"):
            return
        else:
            t_start = time.clock()
            self.ctx[filename]["tu"].reparse(\
                self.get_unsaved_buffer(filename), \
                options=self.parse_options)
            t_elapse = time.clock() - t_start
            self.debug("[profile] parse_delayed idx.reparse: %2.10f" % t_elapse)
            self.ctx[filename]["changedtick"] = context["changedtick"]

            self.highlight(context)

    def highlight(self, context):
        """backend of highlight event"""
        filename = context["filename"]
        lbegin, lend = context["range"]
        row, col = context["position"]
        highlight_tick = context["highlight_tick"]

        buffer = self.__vim.current.buffer
        if not Chromatica.is_supported_filetype(buffer.options["filetype"]): return

        if highlight_tick != buffer.vars["highlight_tick"]:
            return

        if filename not in self.ctx:
            return self.parse(context)

        if "tu" not in self.ctx[filename]: return

        tu = self.ctx[filename]["tu"]

        symbol = syntax.get_symbol_from_loc(tu, buffer.name, row, col)
        syn_group = syntax.get_highlight(tu, buffer.name, \
                lbegin, lend, symbol)

        buffer.clear_highlight(self.syntax_src_id, row)
        for hl_group in syn_group:
            for pos in syn_group[hl_group]:
                row = pos[0] - 1
                col_start = pos[1] - 1
                col_end = col_start + pos[2]
                buffer.add_highlight(hl_group, row, col_start, col_end,\
                        self.syntax_src_id, async=True)

    def print_highlight(self, context):
        """print highlight info"""
        filename = context["filename"]
        lbegin, lend = context["range"]
        row, col = context["position"]
        highlight_tick = context["highlight_tick"]

        buffer = self.__vim.current.buffer
        if not Chromatica.is_supported_filetype(buffer.options["filetype"]): return

        if "tu" not in self.ctx[filename]: return

        tu = self.ctx[filename]["tu"]

        syntax.get_highlight2(tu, buffer.name, \
                lbegin, lend)

    def clear_highlight(self):
        """clear highlight on all buffers"""
        for filename in self.ctx:
            buffer = self.ctx[filename]["buffer"]
            buffer.clear_highlight(self.syntax_src_id)

        self.ctx.clear()

    def show_info(self, context):
        self.vim_print("libclang file: %s" % cindex.conf.get_filename())
        self.vim_print("Filename: %s" % context["filename"])
        self.vim_print("Filetype: %s" % self.__vim.current.buffer.options["filetype"])
        self.vim_print(".clang file: %s" % self.args_db.clang_file)
        self.vim_print("Compilation Database: %s" % self.args_db.cdb_file)
        self.vim_print("Compile Flags: %s" % " ".join(self.args_db.get_args_filename(context["filename"])))

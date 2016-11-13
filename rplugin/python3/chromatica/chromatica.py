# ============================================================================
# FILE: chromatica.py
# AUTHOR: Yanfei Guo <yanf.guo at gmail.com>
# License: MIT license
# based on original version by BB Chung <afafaf4 at gmail.com>
# ============================================================================

from chromatica.neovim_helper import NvimHelper
from chromatica.profiler import Profiler

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
        self.vimh = NvimHelper(vim)
        self.__runtimepath = ""
        self.name = "core"
        self.mark = "[Chromatica Core]"
        self.profiler = Profiler(output_fn=self.debug)
        self.library_path = self.__vim.vars["chromatica#libclang_path"]
        self.syntax_src_id = self.__vim.vars["chromatica#syntax_src_id"]
        self.global_args = self.__vim.vars["chromatica#global_args"]
        self.delay_time = self.__vim.vars["chromatica#delay_ms"] / 1000.0
        self.ctx = {}
        self.parse_options = cindex.TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD \
                           + cindex.TranslationUnit.PARSE_INCOMPLETE
        if self.__vim.vars["chromatica#use_pch"]:
            self.parse_options += cindex.TranslationUnit.PARSE_PRECOMPILED_PREAMBLE
            # self.parse_options += cindex.TranslationUnit.PARSE_PRECOMPILED_PREAMBLE \
            #                    + cindex.TranslationUnit.CREATE_PREAMBLE_ON_FIRST_PARSE
        self.highlight_feature_level = self.__vim.vars["chromatica#highlight_feature_level"]
        syntax.HIGHLIGHT_FEATURE_LEVEL = self.highlight_feature_level

        if not cindex.Config.loaded:
            if os.path.isdir(os.path.abspath(self.library_path)):
                cindex.Config.set_library_path(self.library_path)
            else:
                cindex.Config.set_library_file(self.library_path)
            cindex.Config.set_compatibility_check(False)

        self.args_db = CompileArgsDatabase(self.__vim.current.buffer.name,\
                self.global_args)
        self.idx = cindex.Index.create()

    @classmethod
    def is_supported_filetype(self, filetype):
        if len(filetype) > 0 and filetype.split(".")[0] in ["c", "cpp", "objc", "objcpp"]:
            return True
        return False

    def get_unsaved_buffer(self, filename):
        return [(self.__vim.current.buffer.name, "\n".join(self.__vim.current.buffer))]

    def _init_context(self, context):
        filename = context["filename"]
        # check if context is has the right filetype
        buffer = self.__vim.current.buffer
        filetype = buffer.options["filetype"]
        if not Chromatica.is_supported_filetype(filetype): return False

        args = self.args_db.get_args_filename_ft(filename, filetype)
        self.info("args: %s" % args)

        self.ctx[filename] = context
        self.ctx[filename]["filetype"] = filetype
        self.ctx[filename]["buffer"] = buffer
        self.ctx[filename]["args"] = args

        return True

    def parse(self, context):
        ret = False
        # check if context is already in ctx db
        filename = context["filename"]
        self.debug("filename: %s" % filename)
        if filename not in self.ctx:
            if not self._init_context(context): return ret

            self.profiler.start("parse index.parse")
            tu = self.idx.parse(self.ctx[filename]["buffer"].name,
                                self.ctx[filename]["args"], \
                                self.get_unsaved_buffer(filename), \
                                options=self.parse_options)
            self.profiler.stop()

            if not tu:
                self.error("Cannot generate Translation Unit for %s" % context)
                return ret

            self.ctx[filename]["tu"] = tu

            ret = True

        else:
            ret = self._reparse(context)

        if ret:
            self.highlight(context) # update highlight on entire file

        return ret

    def _reparse(self, context):
        filename = context["filename"]
        if context["changedtick"] <= self.ctx[filename]["changedtick"]: return False
        self.profiler.start("_reparse")
        self.ctx[filename]["tu"].reparse(\
            self.get_unsaved_buffer(filename), \
            options=self.parse_options)
        self.profiler.stop()
        self.ctx[filename]["changedtick"] = context["changedtick"]
        return True

    def delayed_parse(self, context):
        """delayed parse for responsive mode"""
        filename = context["filename"]
        buffer = self.__vim.current.buffer
        if filename not in self.ctx \
                or "tu" not in self.ctx[filename] \
                or not Chromatica.is_supported_filetype(buffer.options["filetype"]):
            return

        time.sleep(self.delay_time)

        if context["changedtick"] < self.__vim.eval("b:changedtick"):
            return
        else:
            if self._reparse(context):
                self._clear_highlight(context)
                self.highlight(context) # update highlight on visible range

    def _highlight(self, filename, lbegin=1, lend=-1):
        """internal highlight function"""
        _lbegin = lbegin
        _lend = self.vimh.line("$") if lend == -1 else lend

        buffer = self.__vim.current.buffer
        tu = self.ctx[filename]["tu"]

        self.profiler.start("_highlight")
        syn_group = syntax.get_highlight(tu, buffer.name, _lbegin, _lend)

        for hl_group in syn_group:
            for pos in syn_group[hl_group]:
                _row = pos[0] - 1
                col_start = pos[1] - 1
                hl_size = pos[2]
                col_end = col_start + hl_size
                n_moreline = pos[3]
                buffer.add_highlight(hl_group, _row, col_start, col_end,\
                        self.syntax_src_id, async=True)
                if n_moreline:
                    next_row = _row + 1
                    bytes_left = hl_size - len(buffer[_row][col_start:])
                    while bytes_left > 0:
                        buffer.add_highlight(hl_group, next_row, 0, bytes_left,\
                                self.syntax_src_id, async=True)
                        bytes_left = bytes_left - len(buffer[next_row]) - 1 # no trailing "\n"
                        next_row = next_row + 1

        self.profiler.stop()

    def _clear_highlight(self, context, syn_src_id=None):
        row, col = context["position"]
        _syn_src_id = syn_src_id if syn_src_id else self.syntax_src_id
        self.debug("clear old highlight from line %d" % row)
        self.__vim.current.buffer.clear_highlight(_syn_src_id, row)

    def highlight(self, context):
        """backend of highlight event"""
        filename = context["filename"]
        lbegin, lend = context["range"]
        row, col = context["position"]
        highlight_tick = context["highlight_tick"]

        buffer = self.__vim.current.buffer
        filetype = buffer.options["filetype"]
        if not Chromatica.is_supported_filetype(filetype): return

        if highlight_tick != buffer.vars["highlight_tick"]: return

        if filename not in self.ctx: return self.parse(context)

        if "tu" not in self.ctx[filename]: return

        self._highlight(filename, lbegin, lend)

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

        syntax.dump_ast_info(tu, buffer.name, lbegin, lend)

    def clear_highlight(self):
        """clear highlight on all buffers"""
        for filename in self.ctx:
            buffer = self.ctx[filename]["buffer"]
            buffer.clear_highlight(self.syntax_src_id)

        self.ctx.clear()

    def show_info(self, context):
        self.vimh.echo("libclang file: %s" % cindex.conf.get_filename())
        self.vimh.echo("Filename: %s" % context["filename"])
        self.vimh.echo("Filetype: %s" % self.__vim.current.buffer.options["filetype"])
        self.vimh.echo(".clang file: %s" % self.args_db.clang_file)
        self.vimh.echo("Compilation Database: %s" % self.args_db.cdb_file)
        self.vimh.echo("Compile Flags: %s" % " ".join( \
                self.args_db.get_args_filename_ft(context["filename"], \
                self.__vim.current.buffer.options["filetype"])))

from chromatica.util import load_external_module

load_external_module(__file__, "")
from clang import cindex

import os
import re

def path_is_root(path):
    if path == "/":
        return True

    return False

class CompileArgsDatabase(object):

    def __init__(self, path, global_args=None):
        self.__path = path
        self.compile_args = []
        self.cdb = None
        self.clang_file = None
        self.cdb_path = None

        if global_args != None:
            self.compile_args = global_args

        self.__find_clang_file()
        self.__find_cdb_file()

        self.__parse_compile_args()
        self.__try_init_cdb()

    def __find_clang_file(self):
        clang_file_path = self.__path
        while not path_is_root(clang_file_path):
            self.clang_file = os.path.join(clang_file_path, ".clang")
            if os.path.exists(self.clang_file):
                return
            clang_file_path = os.path.dirname(clang_file_path)

        self.clang_file = None

    def __find_cdb_file(self):
        cdb_file_path = self.__path
        while not path_is_root(cdb_file_path):
            cdb_file = os.path.join(cdb_file_path, "compile_commands.json")
            if os.path.exists(cdb_file):
                self.cdb_path = cdb_file_path
                return
            cdb_file_path = os.path.dirname(cdb_file_path)

        self.cdb_file = None

    def __parse_compile_args(self):
        if self.clang_file == None:
            return
        # read .clang file
        fp = open(self.clang_file)
        flags = fp.read()
        fp.close()
        m = re.match(r"^flags\s*=\s*", flags)
        if m != None:
            self.compile_args += flags[m.end():].split()

        m = re.match(r"^compilation_database\s*=\s*", flags)
        if m != None:
            cdb_rel_path = flags[m.end():].strip("\"")
            cdb_path = os.path.join(os.path.dirname(self.clang_file), cdb_rel_path)
            if cdb_path and os.path.isdir(cdb_path):
                self.cdb_path = cdb_path

    def __try_init_cdb(self):
        if self.cdb_path != None:
            self.cdb = cindex.CompilationDatabase.fromDirectory(self.cdb_path)

    def get_args_filename(self, filename):
        args = []
        if self.cdb != None:
            args = self.cdb.getCompileCommands(filename)

        return self.compile_args + args


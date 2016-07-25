from chromatica import logger
from chromatica.util import load_external_module

load_external_module(__file__, "")
from clang import cindex

import os
import re

log = logger.logging.getLogger("chromatica.compile_args")

DEFAULT_STD={"c"   : ["-std=c11"], \
             "cpp" : ["-std=c++14"]}

def set_default_std(stds):
    DEFAULT_STD = stds
    return True

class CompileArgsDatabase(object):

    def __init__(self, path, global_args=None):
        if path:
            self.__path = path
        else:
            self.__path = os.getcwd()
        self.compile_args = []
        self.cdb = None
        self.__clang_file = None
        self.__cdb_path = None

        if global_args != None:
            self.compile_args = global_args

        self.__find_clang_file()
        self.__find_cdb_file()

        self.__parse_compile_args()
        self.__try_init_cdb()

    def __find_clang_file(self):
        clang_file_path = self.__path
        while os.path.dirname(clang_file_path) != clang_file_path:
            self.__clang_file = os.path.join(clang_file_path, ".clang")
            if os.path.exists(self.__clang_file):
                return
            clang_file_path = os.path.dirname(clang_file_path)

        self.__clang_file = None

    def __find_cdb_file(self):
        cdb_file_path = self.__path
        while os.path.dirname(cdb_file_path) != cdb_file_path:
            cdb_file = os.path.join(cdb_file_path, "compile_commands.json")
            if os.path.exists(cdb_file):
                self.__cdb_path = cdb_file_path
                return
            cdb_file_path = os.path.dirname(cdb_file_path)

    def __parse_compile_args(self):
        if self.__clang_file == None:
            return
        # read .clang file
        fp = open(self.__clang_file)
        flags = fp.read()
        fp.close()
        m = re.match(r"^flags\s*=\s*", flags)
        if m != None:
            self.compile_args += flags[m.end():].split()

        m = re.match(r"^compilation_database\s*=\s*", flags)
        if m != None:
            cdb_rel_path = flags[m.end():].strip("\"")
            cdb_path = os.path.join(os.path.dirname(self.__clang_file), cdb_rel_path)
            if cdb_path and os.path.isdir(cdb_path):
                self.__cdb_path = cdb_path

    def __try_init_cdb(self):
        if self.__cdb_path != None:
            self.cdb = cindex.CompilationDatabase.fromDirectory(self.__cdb_path)

    def get_args_filename(self, filename):
        ret = None
        if self.cdb != None:
            ret = self.cdb.getCompileCommands(filename)

        if ret:
            res = []
            for cmds in ret:
                cwd = cmds.directory
                skip = 1
                for arg in cmds.arguments:
                    if skip or arg == '-c':
                        skip = 0
                        continue
                    elif os.path.realpath(os.path.join(cwd, arg)) == cmds.filename:
                        skip = 0
                        continue
                    elif arg == '-o':
                        skip = 1
                        continue
                    elif arg.startswith('-I'):
                        include_path = arg[2:]
                        if not os.path.isabs(include_path):
                            include_path = os.path.normpath(
                                os.path.join(cwd, include_path))
                        res.append('-I' + include_path)
                        continue
                    res.append(arg)
            return self.compile_args + res
        else:
            return self.compile_args

    def get_args_filename_ft(self, filename, filetype):
        if self.cdb != None or filetype not in DEFAULT_STD:
            return self.get_args_filename(filename)

        ret = DEFAULT_STD[filetype]
        return ret + self.compile_args

    @property
    def clang_file(self):
        return self.__clang_file

    @property
    def cdb_file(self):
        if self.__cdb_path:
            return os.path.join(self.__cdb_path, "compile_commands.json")
        else:
            return ""


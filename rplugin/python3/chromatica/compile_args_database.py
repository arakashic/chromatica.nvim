from chromatica import logger
from chromatica.util import load_external_module

import chromatica.util as util

load_external_module(__file__, "")
from clang import cindex

import os
import re

log = logger.logging.getLogger("chromatica.compile_args")

DEFAULT_STD={"c"   : ["-std=c11"], \
             "cpp" : ["-std=c++14"]}

SOURCE_EXTS=[".c", ".cc", ".cpp", ".cxx"]
compile_args_files = ['.color_coded', '.clang', 'compile_flags.txt', '.cquery', '.ccls', '.chromatica', 'compile_commands.json']

def set_default_std(stds):
    DEFAULT_STD = stds
    return True

class CompileArgsDatabase(object):

    def __init__(self, global_path, global_args=None):
        if global_path:
            self.__global_path = global_path

        self.__paths = []
        self.__args_file = None
        self.__cdb_file = None
        self.cdb = None

        self.global_args = global_args
        self.compile_args = []
        self.ft_compile_args = { "c" : [], "cpp" : [] , "objc" : [], "objcpp" : [] }

        self.find_per_project_file()

        if len(self.__paths) > 0:
            self.__args_file = self.__paths[0]

        self.parse_args_file()

    def find_per_project_file(self):
        search_path = os.getcwd()
        found_project_root = False
        while not found_project_root and os.path.dirname(search_path) != search_path:
            for args_file in compile_args_files:
                args_file_path = os.path.join(search_path, args_file)
                if os.path.exists(args_file_path):
                    self.__paths.append(args_file_path)
                    found_project_root = True
            search_path = os.path.dirname(search_path)

    def parse_args_file(self):
        if not self.__args_file:
            return

        filename = os.path.basename(self.__args_file)
        if filename == ".chromatica":
            self.parse_chromatica_file()
        elif filename == ".color_coded" or filename == ".clang" or filename == "compile_flags.txt":
            self.parse_simple_file()
        elif filename == ".cquery":
            self.parse_ccls_file()
        elif filename == ".ccls":
            self.parse_ccls_file()
        elif filename == ".ycm_extra_flags":
            self.parse_ycm_file()
        else:
            self.init_cdb(os.path.dirname(self.__args_file))

    def parse_simple_file(self):
        if self.__args_file == None:
            return
        fp = open(self.__args_file, "r")
        lines = fp.readlines()
        fp.close()

        for line in lines:
            if len(line) == 0:
                continue
            self.compile_args.extend(line.strip().split())

    def parse_chromatica_file(self):
        assert len(self.compile_args) == 0
        if self.__args_file == None:
            return
        fp = open(self.__args_file, "r")
        lines = fp.readlines()
        fp.close()

        funcs = {"flags" : lambda s, value: s.compile_args.extend(value.split()),
                 "c" : lambda s, value: s.ft_compile_args["c"].extend(value.split()),
                 "cpp" : lambda s, value: s.ft_compile_args["cpp"].extend(value.split()),
                 "compilation_database" : lambda s, value: s.init_cdb(value), }

        for line in lines:
            if len(line) == 0 :
                continue
            line = line.strip()
            if line.startswith("#"):
                continue
            pos = line.find("=")
            if pos != -1:
                key = line[:pos]
                try:
                    funcs[key](self, line[pos+1:])
                except:
                    log.error("Invalid configuration key: ", key)
            else:
                self.compile_args.extend(line.split())

    def parse_ccls_file(self):
        if self.__args_file == None:
            return
        fp = open(self.__args_file, "r")
        lines = fp.readlines()
        fp.close()

        for line in lines:
            if len(line) == 0 :
                continue
            line = line.strip()
            if line.startswith("clang"):
                continue
            if line.startswith("#"):
                continue
            elif line.startswith("%"):
                keys = [key for key in line.split(" ") if len(key) > 0]
                for key in keys:
                    if key == "%compile_commands.json":
                        self.init_cdb("compile_commands.json")
                    elif key == "%c" or key == "%h":
                        self.ft_compile_args["c"].append(keys[-1])
                    elif key == "%cpp" or key == "%hpp":
                        self.ft_compile_args["c"].append(keys[-1])
                    elif key == "%objective-c":
                        self.ft_compile_args["objc"].append(keys[-1])
                    elif key == "%objective-cpp":
                        self.ft_compile_args["objcpp"].append(keys[-1])
            else:
                self.compile_args.append(line)

    def init_cdb(self, value):
        log.info("cdb: %s" % value)
        cdb_rel_path = value.strip("\"")
        if os.path.isabs(cdb_rel_path):
            cdb_path = cdb_rel_path
        else:
            cdb_path = os.path.join(os.path.dirname(self.__args_file), cdb_rel_path)
        if cdb_path and os.path.isdir(cdb_path):
            self.__cdb_path = cdb_path
            # self.try_init_cdb()
            try:
                self.cdb = cindex.CompilationDatabase.fromDirectory(self.__cdb_path)
            except:
                log.error("Invalid compilation database file %s" % self.__cdb_path)
                self.__cdb_path = None

    def get_cdb_args(self, filename):
        res = []
        ret = self.cdb.getCompileCommands(filename)
        _basename = os.path.basename(filename)
        log.info("Read cdb for: %s" % filename)
        if ret:
            for cmds in ret:
                cwd = cmds.directory
                skip = 0
                last = ''
                for arg in cmds.arguments:
                    if skip and (len(arg) == 0 or arg[0] != "-"):
                        skip = 0
                        continue
                    if arg == "-o" or arg == "-c":
                        skip = 1
                        continue

                    if arg != '-I' and arg.startswith('-I'):
                        include_path = arg[2:]
                        if not os.path.isabs(include_path):
                            include_path = os.path.normpath(
                                os.path.join(cwd, include_path))
                        res.append('-I' + include_path)
                    if arg != '-isystem' and arg.startswith('-isystem'):
                        include_path = arg[8:]
                        if not os.path.isabs(include_path):
                            include_path = os.path.normpath(
                                os.path.join(cwd, include_path))
                        res.append('-isystem' + include_path)
                    if _basename in arg:
                        continue;
                    else:
                        # if last added switch was standalone include then we need to append path to it
                        if last == '-I' or last == '-isystem':
                            include_path = arg
                            if not os.path.isabs(include_path):
                                include_path = os.path.normpath(os.path.join(cwd, include_path))
                            res[len(res) - 1] += include_path
                            last = ''
                        else:
                            res.append(arg)
                            last = arg
        else:
            print("Cannot find compile flags for %s in compilation database" % filename)
        return res

    def get_args_filename(self, filename, search_source_args=False):
        ret = []
        if self.global_args != None:
            ret = self.global_args

        ret += self.compile_args

        if self.cdb != None:
            cdb_ret = self.get_cdb_args(filename)
            if not cdb_ret and search_source_args:
                filename_base = os.path.splitext(filename)[0]
                for source_ext in SOURCE_EXTS:
                    cdb_ret = self.get_cdb_args(filename_base + source_ext)
                    if cdb_ret:
                        break
            ret += cdb_ret

        return ret

    def get_args_filename_ft(self, filename, filetype, search_source_args=False):
        ret = self.get_args_filename(filename, search_source_args)
        return ret + self.ft_compile_args[filetype]

    def get_available_args_files(self):
        return self.__paths

    @property
    def args_file(self):
        return self.__args_file

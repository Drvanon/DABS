#! /usr/bin/env python3

import os
import sys
import fnmatch
import yaml


__doc__ = """Build configurator.
Usage:
    configure.py [options] [-D var[=val]]...
    configure.py [options] [-D var[=val]]... compiler ( cc | gcc | clang )

Options:
  --native          Enable native optimizations.
  -d, --debug       Compile with debug.
  -D var=val        Define variable.
  -o file           Output ninja file [default: build.ninja].
  -h, --help        Show this screen.
  -c file           Configure file [default: configure.yaml]
  -l library_name   Build as a library
  -s source_dir     Build from source dir (default: src)
  -b build_file     Build to this file (not compatible with -l) (default: bin/main)
"""


def build_files(n, args):
    print("Setting up build files")
    exe_ext = ".exe" if os.name == "nt" else ""
    obj_ext = ".o"

    # # Precompiled header.
    # n.build("src/precompile.h.gch", "cxx", "src/precompile.h",
    #         variables={"xtype": "-x c++-header"})
    # precompiled_header = "src/precompile.h.gch"

    objects = []

    source_folder = args["-s"] if args["-s"] else  conf.get("source", "src")
    build_file = args["-b"] if args["-b"] else conf.get("build_file", "bin/main")

    # C
    for root, dirnames, filenames in os.walk(source_folder):
        for filename in fnmatch.filter(filenames, "*.c"):
            src = os.path.join(root, filename)
            obj = os.path.join("obj", os.path.splitext(src)[0] + obj_ext)
            print("Found file: {} ".format(src))
            n.build(obj, "cc", src)
            # n.build(obj, "cxx", src, precompiled_header)
            objects.append(obj)

    # C++
    for root, dirnames, filenames in os.walk(source_folder):
        for filename in fnmatch.filter(filenames, "*.cpp"):
            src = os.path.join(root, filename)
            obj = os.path.join("obj", os.path.splitext(src)[0] + obj_ext)
            print("Found file: {} ".format(src))
            n.build(obj, "cxx", src)
            # n.build(obj, "cxx", src, precompiled_header)
            objects.append(obj)

    if args["-l"]:
        path_name = "lib/lib" + args["-l"] + ".a"
        n.build(path_name, "liblink", objects)
        n.default(path_name)
    else:
        n.build(build_file + exe_ext, "cxxlink", objects)
        n.default(build_file + exe_ext)


def build_rules(n, args, conf):
    print("Setting up rules")
    n.variable("cc", conf.get("cc", "gcc"))
    n.variable("cxx", conf.get("cxx", "g++"))

    native_flag = " -march=native" if args["--native"] else ""

    if args["--debug"]:
        n.variable("dbgflags", "-ggdb")
        debug_flag = "-g"
        n.variable("optflags", native_flag + debug_flag)
    else:
        n.variable("dbgflags", "")
        debug_flag = " -DNDEBUG"
        n.variable("optflags", "-O2" + native_flag + debug_flag)

    defines = [" -D" + d for d in args["-D"]]
    includes = [" -I" + i for i in conf.get("includes", [])]
    search_directories = [" -L" + L for L in conf.get("search_directories", [])]
    libraries = [" -l" + l for l in conf.get("libraries", [])]

    libflags = ""
    libflags += "".join(defines)
    libflags += "".join(includes)

    cflags = "-std=c99 -Wall -pedantic -fwrapv"
    cflags += "".join(defines)
    cflags += "".join(includes)

    cxxflags = "-std=c++11 -Wall -pedantic -fwrapv"
    cxxflags += "".join(defines)
    cxxflags += "".join(includes)

    cxxlinkflags = ""
    cxxlinkflags += "".join(search_directories)
    cxxlinkflags += "".join(libraries)

    n.variable("cflags", cflags)
    n.variable("cxxflags", cxxflags)
    n.variable("cxxlinkflags", cxxlinkflags)

    n.rule("cc",
           "$cc $xtype -MMD -MF $out.d $optflags $dbgflags $cflags -c $in -o $out",
           depfile="$out.d")

    n.rule("cxx",
           "$cxx $xtype -MMD -MF $out.d $optflags $dbgflags $cxxflags -c $in -o $out",
           depfile="$out.d")

    n.rule("cxxlink", "$cxx $optflags $dbgflags $in $cxxlinkflags -o $out")

    n.rule("liblink", "ar rs $out $libflags $in")


# Everything below this line is dependency boilerplate.
if __name__=="__main__":
    try:
        from docopt import docopt
        import ninja_syntax
    except ImportError:
        msg = """You are missing one or more dependencies, install using:
        {} -m pip install --user docopt ninja-syntax pyyaml
If you are using an old version of Python, and don't have pip,
download https://bootstrap.pypa.io/get-pip.py and run it."""

        print(msg.format(os.path.basename(sys.executable)))
        sys.exit(1)


    args = docopt(__doc__)

    # Check if we're likely running for the first time.
    first_time = not os.path.isfile(args["-o"])

    # Write ninja build file.
    with open(args["-o"], "w") as ninja_file, open(args["-c"], "r") as conf_file:
        conf = yaml.load(conf_file)
        n = ninja_syntax.Writer(ninja_file)
        build_rules(n, args, conf)
        build_files(n, args)

    # Check if we have ninja in path.
    path = os.environ.get("PATH", os.defpath).split(os.pathsep)
    if sys.platform == "win32":
        path.insert(0, os.curdir)
        pathext = os.environ.get("PATHEXT", "").split(os.pathsep)
        files = ["ninja" + ext for ext in pathext]
    else:
        files = ["ninja"]


    def is_exe(path):
        return os.path.exists(path) and os.access(
            path, os.F_OK | os.X_OK) and not os.path.isdir(path)

    has_ninja = any(is_exe(os.path.join(d, f)) for d in path for f in files)

    if first_time and not has_ninja:
        msg = """It appears you're running configure.py for the first time, but do not have
    ninja in your path. On Windows we recommend simply downloading the binary:
        https://github.com/ninja-build/ninja/releases/download/v1.6.0/ninja-win.zip
    Extract anywhere in your path, or even inside this directory.
    On linux it's easiest to compile from source:
        wget https://github.com/ninja-build/ninja/archive/v1.6.0.tar.gz
        tar xf v1.6.0.tar.gz && rm v1.6.0.tar.gz && cd ninja-1.6.0
        {} configure.py --bootstrap
        sudo cp ninja /usr/local/bin
    This should only take half a minute or so."""
        print(msg.format(os.path.basename(sys.executable)))

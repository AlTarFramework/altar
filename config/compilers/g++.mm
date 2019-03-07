# -*- Makefile -*-
#
# michael a.g. aïvázis
# parasim
# (c) 1998-2019 all rights reserved
#

# the name of the compiler
compiler.c++ := g++

# prefices for specific categories
g++.prefix.flags :=
g++.prefix.defines := -D
g++.prefix.incpath := -I$(space)

g++.prefix.ldflags :=
g++.prefix.libpath := -L$(space)
g++.prefix.libraries := -l

# compile time flags
g++.compile.only := -c
g++.compile.output := -o
g++.compile.generate-dependencies := -MMD

# symbols and optimization
g++.debug := -g
g++.opt := -O3
g++.cov := --coverage
g++.prof := -pg

# relocatable code
g++.compile.shared := -fPIC

# language level
g++.std.c++98 := -std=c++98
g++.std.c++11 := -std=c++11
g++.std.c++14 := -std=c++14
g++.std.c++17 := -std=c++17

# link time flags
g++.link.output := -o
g++.link.shared :=
# link a dynamically loadable library
g++.link.dll := -shared

# end of file

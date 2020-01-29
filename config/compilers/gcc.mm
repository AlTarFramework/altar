# -*- Makefile -*-
#
# michael a.g. aïvázis
# parasim
# (c) 1998-2020 all rights reserved
#

# the name of the compiler
compiler.c := gcc

# prefices for specific categories
gcc.prefix.flags :=
gcc.prefix.defines := -D
gcc.prefix.incpath := -I

gcc.prefix.ldflags :=
gcc.prefix.libpath := -L
gcc.prefix.libraries := -l

# compile time flags
gcc.compile.only := -c
gcc.compile.output := -o
gcc.compile.generate-dependencies := -MMD

# symbols and optimization
gcc.debug := -g
gcc.opt := -O3
gcc.cov := --coverage
gcc.prof := -pg

# relocatable code
gcc.compile.shared := -fPIC

# language level
gcc.std.ansi := -ansi
gcc.std.c90 := -std=c90
gcc.std.c99 := -std=c99
gcc.std.c11 := -std=c11

# link time flags
gcc.link.output := -o
gcc.link.shared :=
# link a dynamically loadable library
gcc.link.dll := -shared

# end of file

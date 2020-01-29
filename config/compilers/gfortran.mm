# -*- Makefile -*-
#
# michael a.g. aïvázis
# parasim
# (c) 1998-2020 all rights reserved
#

# the name of the compiler
compiler.fortran := gfortran

# prefices for specific categories
gfortran.prefix.flags :=
gfortran.prefix.defines := -D
gfortran.prefix.incpath := -I

gfortran.prefix.ldflags := -
gfortran.prefix.libpath := -L
gfortran.prefix.libraries := -l

# compile time flags
gfortran.compile.only := -c
gfortran.compile.output := -o
gfortran.compile.generate-dependencies :=

# symbols and optimization
gfortran.debug := -g
gfortran.opt := -O3
gfortran.cov := -coverage
gfortran.prof := -pg

# relocatable code
gfortran.compile.shared := -fPIC

# language level
gfortran.std.f77 :=

# link time flags
gfortran.link.output := -o
gfortran.link.shared :=
# link a dynamically loadable library
gfortran.link.dll := -shared

# end of file

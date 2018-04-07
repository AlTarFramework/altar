# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2018 parasim inc
# (c) 2010-2018 california institute of technology
# all rights reserved
#

# the default compiler
c++ ?= g++

# include support for the c++ copiler
include make/compilers/$(c++).mm

# command line options fall into two borad categories
c++.compile.categories = flags defines incpath
c++.link.categories = ldflags libpath libraries

# build the complete compiler command line
# usage c++.compile {library} {obj} {src}
c++.compile = \
  $(c++) \
  $($(c++).compile.only) $(3) \
  $($(c++).compile.output) $(2) \
  $($(c++).compile.generate-dependencies) \
  ${call c++.compile.options,$($(1).externals)} \

# end of file

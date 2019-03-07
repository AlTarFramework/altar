# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2019 parasim inc
# (c) 2010-2019 california institute of technology
# all rights reserved
#

# the default compiler
c++ ?= g++

# include support for the c++ copiler
include config/compilers/$(c++).mm

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
  -fPIC \
  ${call c++.compile.options,$($(1).packages)} \


# build the complete link command line
# usage c++.link {executable} {source-file} {dependencies}
c++.link = \
  $(c++) \
  $(2) \
  $($(c++).link.output) $(1) \
  ${call c++.compile.options,$(3)} \
  ${call c++.link.options,$(3)} \

c++.so = \
  $(c++) \
  -shared -fPIC \
  $(2) \
  $($(c++).link.output) $(1) \
  ${call c++.compile.options,$(3)} \
  ${call c++.link.options,$(3)} \


# assemble the contributions to the compiler command line
# usage: c++.compile.options {dependencies}
c++.compile.options = \
  ${call packages.compile.options,$(1)} \
  ${call mm.compile.options}


# assemble the contrinutios to the linker command line
# usage: c++.link.options {dependencies}
c++.link.options = \
  ${call packages.link.options,$(1)} \
  ${call mm.link.options}


# end of file

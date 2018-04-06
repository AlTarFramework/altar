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


# there are three potential libraries to build:
# the base library, a library with the cuda code, and a library with mpi code

# first, the base library
library.base.name = lib$(project)
# the source directory
library.base.src = $(src.lib)/$(library.base.name)
# the destination directory
library.base.dest = $(dest.lib)
# the temporary staging area
library.base.staging = $(dest.staging)/$(library.base.name)

# the sources
library.base.sources = ${shell find $(library.base.src) -name \*.cc}
# the headers
library.base.sources = ${shell find $(library.base.src) -name \*.h -name \*.icc}
# the archive
library.base.archive = $(library.base.dest)/$(library.base.name)


# recipes
project.libraries:


# info and makefile debugging
log.c++.sources:
	echo $(c++.sources)

log.c++.headers:
	echo $(c++.headers)

log.c++.objects:
	echo $(c++.objects)

# end of file

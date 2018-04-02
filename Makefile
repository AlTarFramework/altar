# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2010-2018 california institute of technology
# (c) 2013-2018 parasim inc
# all rights reserved
#

# get the master makefile
include make/master.mm

# metadata
altar.major := 2
altar.minor := 0
altar.revision := ${strip ${shell $(bzr.revno) || echo 0}}
now.year := ${strip ${shell $(date.year)}}
now.date := ${strip ${shell $(date.stamp)}}

# compilers
c ?= gcc
c++ ?= g++
python ?= python3
cython ?= cython -3

# directories
blddir = build
# c++
c++.src.root := lib

# sources
c++.sources := ${shell find $(c++.src.root) -name \*.cc}
c++.headers := ${shell find $(c++.src.root) -name \*.h -name \*.icc}

# python packages
include make/python.mm

# recipes
all: python.pkg

tidy:
	find . -name \*~ -delete

clean: tidy
	$(rm.force-recurse) $(blddir)

# general
$(blddir):
	${call log.action,mkdir,$(blddir)}
	$(mkdirp) $(blddir)

# info and makefile debugging
log.c++.sources:
	echo $(c++.sources)

log.c++.headers:
	echo $(c++.headers)

log.c++.objects:
	echo $(c++.objects)

log.python.sources:
	echo $(python.sources)

log.python.pyc:
	echo $(python.pkg.pyc)

# end of file

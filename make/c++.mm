# -*- Makefile -*-
#
# michael a.g. aïvázis
# parasim
# (c) 1998-2018 all rights reserved
#

# the default compiler
c++ ?= g++

# c++
c++.src.root := lib
# sources
c++.sources := ${shell find $(c++.src.root) -name \*.cc}
c++.headers := ${shell find $(c++.src.root) -name \*.h -name \*.icc}

# info and makefile debugging
log.c++.sources:
	echo $(c++.sources)

log.c++.headers:
	echo $(c++.headers)

log.c++.objects:
	echo $(c++.objects)

# end of file

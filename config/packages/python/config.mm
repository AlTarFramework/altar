# -*- Makefile -*-
#
# michael a.g. aïvázis
# parasim
# (c) 1998-2020 all rights reserved
#

# add me to the pile
packages += python

# the version
python.version ?=
# the model
python.model ?= m
# the interpreter id
python.interpreter ?= python$(python.version)$(python.model)

# compiler flags
python.flags ?=
# enable {python} aware code
python.defines := WITH_PYTHON
# the canonical form of the include directory
python.incpath ?= $(python.dir)/include/$(python.interpreter)

# linker flags
python.ldflags ?=
# the canonical form of the lib directory
python.libpath ?= $(python.dir)/lib
# the names of the libraries
python.libraries ?= $(python.interpreter)

# now include some platform specific settings
# include packages/python/$(platform).mm

# end of file

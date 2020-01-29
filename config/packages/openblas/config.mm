# -*- Makefile -*-
#
# michael a.g. aïvázis
# parasim
# (c) 1998-2020 all rights reserved
#

# add me to the pile
packages += openblas

# compiler flags
openblas.flags ?=
# enable {openblas} aware code
openblas.defines := WITH_OPENBLAS
# the canonical form of the include directory
openblas.incpath ?= $(openblas.dir)/include

# linker flags
openblas.ldflags ?=
# the canonical form of the lib directory
openblas.libpath ?= $(openblas.dir)/lib
# the name of the library
openblas.libraries := openblas

# end of file

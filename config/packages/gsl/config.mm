# -*- Makefile -*-
#
# michael a.g. aïvázis
# parasim
# (c) 1998-2019 all rights reserved
#

# add me to the pile
packages += gsl

# compiler flags
gsl.flags ?=
# enable {gsl} aware code
gsl.defines := WITH_GSL HAVE_INLINE
# the canonical form of the include directory
gsl.incpath ?= $(gsl.dir)/include

# linker flags
gsl.ldflags ?=
# the canonical form of the lib directory
gsl.libpath ?= $(gsl.dir)/lib
# the name of the library
gsl.libraries := gsl

# initialize the list of my dependencies
gsl.dependencies =

# set to specify the blas implementation
gsl.blas ?=
# if it exists, add it to my dependencies, otherwise add my blas implementation to my libraries
${if \
    ${call package.exists,$(gsl.blas)}, \
    ${eval gsl.dependencies = $(gsl.blas)}, \
    ${eval gsl.libraries += gslcblas} \
}

# end of file

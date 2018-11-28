# -*- Makefile -*-
#
# Lijun Zhu
# Caltech
# (c) 1998-2018 all rights reserved
#

# add me to the pile
packages += cuda

# users set this variable to communicate which libraries they want
cuda.required ?=

# compiler flags
cuda.flags ?=
# enable {cuda} aware code
cuda.defines := \
    WITH_CUDA \
    ${if ${findstring cuda,$(cuda.flavor)}, WITH_CUDA,} \
# the canonical form of the include directory
cuda.incpath ?= $(cuda.dir)/include

# linker flags
cuda.ldflags ?=
# the canonical form of the lib directory
cuda.libpath ?= $(mpi.dir)/lib64
# the names of the libraries are flavor dependent
cuda.libraries := \
    ${if ${findstring cuda,$(cuda.flavor)},cuda cublas curand cu $(cuda.required),}

# end of file

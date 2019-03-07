# -*- Makefile -*-
#
# michael a.g. aïvázis
# parasim
# (c) 1998-2019 all rights reserved
#

# mm info
mm =
mm.version =
mm.home = .mm
mm.master =
mm.compilers =

# contributions to the build
# only {incpath} and {libpath} seem to be useful
mm.incpath ?= ${realpath .}/config/include
mm.libpath ?=

# influence the build
# add an include path to the build to facilitate compiling products against specific targets
#   usage: mm.compile.options
mm.compile.options = \
    ${addprefix $($(c++).prefix.incpath),$(mm.incpath)}

# add an library search path to the build to facilitate linking products against specific targets
#   usage: mm.link.options
mm.link.options = \
    ${addprefix $($(c++).prefix.libpath),$(mm.libpath)}

# end of file

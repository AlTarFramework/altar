# -*- Makefile -*-
#
# michael a.g. aïvázis
# parasim
# (c) 1998-2019 all rights reserved
#

# assemble the list of compilers
#    order: defaults from the platform, then user configuration files, then mm command line
compilers := \
    $(platform.compilers) $(target.compilers) \
    $($(developer).compilers) \
    $(mm.compilers)

# include the compiler specific configuration files
include ${foreach compiler,$(compilers),compilers/$(compiler).mm}

# end of file

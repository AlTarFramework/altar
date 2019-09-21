# -*- Makefile -*-
#
# michael a.g. aïvázis
# parasim
# (c) 1998-2019 all rights reserved
#

# project meta-data
altar.major := 2
altar.minor := 0

# altar consists of a python package
altar.packages := altar.pkg
# libraries
altar.libraries := altar.lib
# python extensions
altar.extensions := altar.ext
# and some tests
altar.tests := altar.pkg.tests

# the altar package meta-data
altar.pkg.stem := altar
altar.pkg.root := altar/
altar.pkg.drivers := altar

# libaltar meta-data
altar.lib.stem := altar
altar.lib.extern := gsl pyre
altar.lib.c++.flags += $($(compiler.c++).std.c++17)

# the altar extension meta-data
altar.ext.stem := altar
altar.ext.root := ext/
altar.ext.pkg := altar.pkg
altar.ext.wraps := altar.lib
altar.ext.extern := altar.lib gsl pyre python
# compile options for the sources
altar.ext.lib.c++.flags += $($(compiler.c++).std.c++17)

# the altar test suite
altar.pkg.tests.stem := altar
altar.pkg.tests.prerequisites := altar.pkg altar.ext
# individual test cases
tests.altar.application_run.clean = \
    ${addprefix $(altar.pkg.tests.prefix),llk.txt sigma.txt theta.txt}

# models
include emhp.def gaussian.def mogi.def cdm.def linear.def

# end of file

# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2018 parasim inc
# (c) 2010-2018 california institute of technology
# all rights reserved
#


# the package
import altar


# publish the protocol for probability distributions
from .Distribution import Distribution as distribution


# implementations
@altar.foundry(implements=distribution, tip="the uniform probability distribution")
def uniform():
    # grab the factory
    from .Uniform import Uniform as uniform
    # attach its docstring
    __doc__ = uniform.__doc__
    # and return it
    return uniform


# end of file

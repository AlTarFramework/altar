# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2019 parasim inc
# (c) 2010-2019 california institute of technology
# all rights reserved
#

# the package
import altar


# implementations
@altar.foundry(implements=altar.models.model, tip="a linear model")
def linear():
    # grab the factory
    from .Linear import Linear as linear
    # attach its docstring
    __doc__ = linear.__doc__
    # and return it
    return linear


# end of file

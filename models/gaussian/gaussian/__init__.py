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
@altar.foundry(implements=altar.models.model, tip="a multi-parameter Gaussian model")
def gaussian():
    # grab the factory
    from .Gaussian import Gaussian as gaussian
    # attach its docstring
    __doc__ = gaussian.__doc__
    # and return it
    return gaussian


# end of file

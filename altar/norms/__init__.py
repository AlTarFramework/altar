# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2020 parasim inc
# (c) 2010-2020 california institute of technology
# all rights reserved
#


# the package
import altar


# publish the protocol for norms
from .Norm import Norm as norm


# implementations
@altar.foundry(implements=norm, tip="the L2 norm")
def l2():
    # grab the factory
    from .L2 import L2 as l2
    # attach its docstring
    __doc__ = l2.__doc__
    # and return it
    return l2


# end of file

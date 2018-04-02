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
# and the protocols
from .Controller import Controller as controller


# implementations
@altar.foundry(implements=controller, tip="a Bayesian controller")
def annealer():
    # grab the factory
    from .Annealer import Annealer as annealer
    # attach its docstring
    __doc__ = annealer.__doc__
    # and return it
    return annealer


# end of file

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


# implementations
@altar.foundry(implements=altar.models.model, tip="a diagnostic tool")
def emhp():
    # grab the factory
    from .EMHP import EMHP as emhp
    # attach its docstring
    __doc__ = emhp.__doc__
    # and return it
    return emhp


# end of file

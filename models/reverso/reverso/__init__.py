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

# access to the reverso source
from .Source import Source as source
# and the layout of the input file
from .Data import Data as data

# implementations
@altar.foundry(implements=altar.models.model, tip="a multi-parameter reverso model")
def reverso():
    # grab the factory
    from .Reverso import Reverso as reverso
    # attach its docstring
    __doc__ = reverso.__doc__
    # and return it
    return reverso


# end of file

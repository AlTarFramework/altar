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

# access to the CDM source
from .Source import Source as source
# and the layout of the input file
from .Data import Data as data

# implementations
@altar.foundry(implements=altar.models.model, tip="a multi-parameter CDM model")
def cdm():
    # grab the factory
    from .CDM import CDM as cdm
    # attach its docstring
    __doc__ = cdm.__doc__
    # and return it
    return cdm


# end of file

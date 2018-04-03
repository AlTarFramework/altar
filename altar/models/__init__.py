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
# the protocol
from .Model import Model as model


# implementations
@altar.foundry(implements=model, tip="a trivial AlTar model")
def null():
    # grab the factory
    from .Null import Null as null
    # attach its docstring
    __doc__ = null.__doc__
    # and return it
    return null


@altar.foundry(implements=model, tip="a collection of models that comprise an AlTar model")
def ensemble():
    # grab the factory
    from .Ensemble import Ensemble as ensemble
    # attach its docstring
    __doc__ = ensemble.__doc__
    # and return it
    return ensemble


# end of file

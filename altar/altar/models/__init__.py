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


# the protocols
from .Model import Model as model
from .ParameterSet import ParameterSet as parameters


# the model base class
from .Bayesian import Bayesian as bayesian


# implementations
@altar.foundry(implements=model, tip="a trivial AlTar model")
def null():
    # grab the factory
    from .Null import Null as null
    # attach its docstring
    __doc__ = null.__doc__
    # and publish it
    return null


@altar.foundry(implements=model, tip="a collection of models that comprise an AlTar model")
def ensemble():
    # grab the factory
    from .Ensemble import Ensemble as ensemble
    # attach its docstring
    __doc__ = ensemble.__doc__
    # and publish it
    return ensemble


@altar.foundry(implements=parameters, tip="a contiguous parameter set")
def contiguous():
    # grab the factory
    from .Contiguous import Contiguous as contiguous
    # attach its docstring
    __doc__ = contiguous.__doc__
    # and publish it
    return contiguous


# end of file

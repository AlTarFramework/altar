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


@altar.foundry(implements=distribution, tip="the gaussian probability distribution")
def gaussian():
    # grab the factory
    from .Gaussian import Gaussian as gaussian
    # attach its docstring
    __doc__ = gaussian.__doc__
    # and return it
    return gaussian


@altar.foundry(implements=distribution, tip="the unit gaussian probability distribution")
def ugaussian():
    # grab the factory
    from .UnitGaussian import UnitGaussian as ugaussian
    # attach its docstring
    __doc__ = ugaussian.__doc__
    # and return it
    return ugaussian


# end of file

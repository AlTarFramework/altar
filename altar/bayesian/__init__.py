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
# and the protocols
from .Controller import Controller as controller
from .Sampler import Sampler as sampler
from .Scheduler import Scheduler as scheduler
from .Solver import Solver as solver


# implementations
@altar.foundry(
    implements=controller,
    tip="a Bayesian controller that implements simulated annealing")
def annealer():
    # grab the factory
    from .Annealer import Annealer
    # attach its docstring
    __doc__ = Annealer.__doc__
    # and return it
    return Annealer


@altar.foundry(
    implements=scheduler,
    tip="a Bayesian scheduler based on the COV algorithm")
def cov():
    # grab the factory
    from .COV import COV
    # attach its docstring
    __doc__ = COV.__doc__
    # and return it
    return COV


@altar.foundry(
    implements=solver,
    tip="a solver for δβ based on a Brent minimizer from gsl")
def brent():
    # grab the factory
    from .Brent import Brent
    # attach its docstring
    __doc__ = Brent.__doc__
    # and return it
    return Brent


@altar.foundry(
    implements=solver,
    tip="a solver for δβ based on a naive grid search")
def grid():
    # grab the factory
    from .Grid import Grid
    # attach its docstring
    __doc__ = Grid.__doc__
    # and return it
    return Grid


@altar.foundry(
    implements=sampler,
    tip="a Bayesian sampler based on the Metropolis algorithm")
def metropolis():
    # grab the factory
    from .Metropolis import Metropolis
    # attach its docstring
    __doc__ = Metropolis.__doc__
    # and return it
    return Metropolis


@altar.foundry(
    implements=altar.simulations.monitor,
    tip="a monitor that times the various simulation phases")
def profiler():
    # grab the factory
    from .Profiler import Profiler
    # attach its docstring
    __doc__ = Profiler.__doc__
    # and return it
    return Profiler


# end of file

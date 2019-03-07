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


# implementations
@altar.foundry(
    implements=controller,
    tip="a Bayesian controller that implements simulated annealing")
def annealer():
    # grab the factory
    from .Annealer import Annealer as annealer
    # attach its docstring
    __doc__ = annealer.__doc__
    # and return it
    return annealer


@altar.foundry(implements=scheduler, tip="the COV algorithm as a Bayesian scheduler")
def cov():
    # grab the factory
    from .COV import COV as cov
    # attach its docstring
    __doc__ = cov.__doc__
    # and return it
    return cov


@altar.foundry(implements=sampler, tip="the Metropolis algorithm as a Bayesian sampler")
def metropolis():
    # grab the factory
    from .Metropolis import Metropolis as metropolis
    # attach its docstring
    __doc__ = metropolis.__doc__
    # and return it
    return metropolis


@altar.foundry(implements=sampler, tip="a monitor that times the various simulation phases")
def profiler():
    # grab the factory
    from .Profiler import Profiler as profiler
    # attach its docstring
    __doc__ = profiler.__doc__
    # and return it
    return profiler


# end of file

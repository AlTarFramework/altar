# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2018 parasim inc
# (c) 2010-2018 california institute of technology
# all rights reserved
#


# superclass
from .AnnealingMethod import AnnealingMethod


# declaration
class MPIAnnealing(AnnealingMethod):
    """
    A distributed implementation of the annealing method that uses MPI
    """


# end of file

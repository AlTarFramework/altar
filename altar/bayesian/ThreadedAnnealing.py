# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2019 parasim inc
# (c) 2010-2019 california institute of technology
# all rights reserved
#


# superclass
from .AnnealingMethod import AnnealingMethod


# declaration
class ThreadedAnnealing(AnnealingMethod):
    """
    Annealing method that uses threads on the local machine
    """


# end of file

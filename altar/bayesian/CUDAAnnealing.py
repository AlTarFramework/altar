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
class CUDAAnnealing(AnnealingMethod):
    """
    Implementation that takes advantage of CUDA on gpus to accelerate the computation
    """


# end of file

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
# my protocol
from .Sampler import Sampler as sampler


# declaration
class Metropolis(altar.component, family="altar.samplers.metropolis", implements=sampler):
    """
    The Metropolis algorithm as a sampler of the posterior distribution
    """

    # protocol obligations
    @altar.export
    def initialize(self, model):
        """
        Initialize me and my parts given a {model}
        """
        # all done
        return self


    @altar.export
    def sample(self, model):
        """
        Sample the posterior distribution
        """
        # all done; indicate success
        return 0


    @altar.provides
    def equilibrate(self, statistics):
        """
        Update my statistics based on the results of walking my Markov chains
        """
        # all done
        return


# end of file

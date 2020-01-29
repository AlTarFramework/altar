# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2020 parasim inc
# (c) 2010-2020 california institute of technology
# all rights reserved
#

# get the package
import altar

# the sampler protocol
class Sampler(altar.protocol, family="altar.samplers"):
    """
    The protocol that all AlTar samplers must implement
    """

    # required behavior
    @altar.provides
    def initialize(self, application):
        """
        Initialize me and my parts given an {application} context
        """

    @altar.provides
    def samplePosterior(self, controller, step):
        """
        Sample the posterior distribution
        """

    @altar.provides
    def resample(self, controller, statistics):
        """
        Update my statistics based on the results of walking my Markov chains
        """

    # framework hooks
    @classmethod
    def pyre_default(cls, **kwds):
        """
        Supply a default implementation
        """
        # by default, use {Metropolis}
        from .Metropolis import Metropolis as default
        # and return it
        return default

# end of file

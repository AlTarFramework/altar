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


# the random number generator
class RNG(altar.protocol, family="altar.simulations.rng"):
    """
    The protocol for random number generators
    """

    # required behavior
    @altar.provides
    def initialize(self, **kwds):
        """
        Initialize the random number generator
        """

    # framework hooks
    @classmethod
    def pyre_default(cls, **kwds):
        """
        Supply a default implementation
        """
        # pull the GSL random number generator component
        from .GSLRNG import GSLRNG as default
        # and return it
        return default


# end of file

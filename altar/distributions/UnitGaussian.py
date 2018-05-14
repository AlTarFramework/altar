# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2018 parasim inc
# (c) 2010-2018 california institute of technology
# all rights reserved
#

# get the package
import altar

# get the protocol
from . import distribution
# and my base class
from .Base import Base as base


# the declaration
class UnitGaussian(base, family="altar.distributions.ugaussian"):
    """
    Special case of the Gaussian probability distribution with σ = 1
    """


    # protocol obligations
    @altar.export
    def initialize(self, rng):
        """
        Initialize with the given runtime {context}
        """
        # set up my pdf
        self.pdf = altar.pdf.ugaussian(rng=rng.rng)
        # all done
        return self


# end of file

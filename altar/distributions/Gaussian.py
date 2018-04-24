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
class Gaussian(base, family="altar.distributions.gaussian"):
    """
    The Gaussian probability distribution
    """


    # user configurable state
    sigma = altar.properties.float(default=1)
    sigma.doc = "the support interval of the prior distribution"


    # protocol obligations
    @altar.provides
    def initialize(self, rng):
        """
        Initialize with the given runtime {context}
        """
        # set up my pdf
        self.pdf = altar.pdf.gaussian(rng=rng.rng, sigma=self.sigma)
        # all done
        return self


# end of file

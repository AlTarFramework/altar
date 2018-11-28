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
class Dirichlet(base, family="altar.distributions.dirichlet"):
    """
    The Dirichlet probability distribution
    """

    # user configurable state
    order = altar.properties.int(default=2)
    order.doc = "number of parameters, K" 
    alpha = altar.properties.array(default=(1,1))
    alpha.doc = "concentration parameters alpha_1, alpha_2, ... alpha_K"
    

    # protocol obligations
    @altar.export
    def initialize(self, rng):
        """
        Initialize with the given random number generator
        """
        # 
        self.array_vec = altar.vector(shape = self.parameters)
        for index, value in enumerate(self.alpha) : self.array_vec[index] = value
        # set up my pdf
        self.pdf = altar.pdf.dirichlet(rng=rng.rng, alpha=self.array_vec)
        # all done
        return self



    @altar.export
    def verify(self, theta, mask):
        """
        Check whether my portion of the samples in {theta} are consistent with my constraints, and
        update {mask}, a vector with zeroes for valid samples and non-zero for invalid ones
        """
        # A uniform distribution is used for verfifying, so there is nothing to do here
        return mask

    array_vec = None

# end of file

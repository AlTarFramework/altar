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
class DistributionSet(base, family="altar.distributions.distributionset"):
    """
    A set of distributions
    """

    # the distribution set
    distset = altar.properties.dict(schema=altar.distributions.distribution())


    # protocol obligations
    @altar.export
    def initialize(self, rng):
        """
        Initialize with the given random number generator
        """
        # initialize all distributions in the set
        distset = self.distset
        count = 0
        for name, dist in distset.items():
            # print("count", count, name, dist)
            count+=dist.parameters
            dist.initialize(rng=rng)
        
        self.parameters = count
        
        # all done
        return self

    @altar.export
    def initializeSample(self, theta):
        """
        Fill my portion of {theta} with initial random values from my distribution.
        """
        distset = self.distset
        # iterate through all distributions in the set
        for dist in distset.values():
            dist.initializeSample(theta=theta)
        # all done
        return self
        

    @altar.export
    def computePrior(self, theta, density):
        """
        Fill my portion of {likelihood} with the densities of the samples in {theta}
        """
        distset = self.distset
        # iterate through all distributions in the set
        for dist in distset.values():
            dist.computePrior(theta=theta, density=density)

        # all done
        return self

    @altar.export
    def verify(self, theta, mask):
        """
        Check whether my portion of the samples in {theta} are consistent with my constraints, and
        update {mask}, a vector with zeroes for valid samples and non-zero for invalid ones
        """

        distset = self.distset
        # iterate through all distributions in the set
        for dist in distset.values():
            dist.verify(theta=theta, mask=mask)

        # all done; return the rejection map
        return mask


# end of file

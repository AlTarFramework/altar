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

# get the protocol
from . import distribution
# and my base class
from .Base import Base as base


# the declaration
class Uniform(base, family="altar.distributions.uniform"):
    """
    The uniform probability distribution
    """


    # user configurable state
    support = altar.properties.array(default=(0,1))
    support.doc = "the support interval of the prior distribution"


    # protocol obligations
    @altar.export
    def initialize(self, rng):
        """
        Initialize with the given random number generator
        """
        # set up my pdf
        self.pdf = altar.pdf.uniform(rng=rng.rng, support=self.support)
        # all done
        return self


    @altar.export
    def verify(self, theta, mask):
        """
        Check whether my portion of the samples in {theta} are consistent with my constraints, and
        update {mask}, a vector with zeroes for valid samples and non-zero for invalid ones
        """
        # unpack my support
        low, high = self.support
        # grab the portion of the sample that's mine
        θ = self.restrict(theta=theta)

        # find out how many samples in the set
        samples = θ.rows
        # and how many parameters belong to me
        parameters = θ.columns

        # go through the samples in θ
        for sample in range(samples):
            # and the parameters in this sample
            for parameter in range(parameters):
                # if the parameter lies outside my support
                if not (low <= θ[sample,parameter] <= high):
                    # mark the entire sample as invalid
                    mask[sample] += 1
                    # and skip checking the rest of the parameters
                    break

        # all done; return the rejection map
        return mask


# end of file

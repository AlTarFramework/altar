# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# Lijun Zhu <ljzhu@caltech.edu>
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
        # keep a local reference to rng
        self.rng = rng.rng
        # all done
        return self

    @altar.export
    def initializeSample(self, theta):
        """
        Fill my portion of {theta} with initial random values from my distribution.
        """
        # grab the portion of the sample that's mine
        θ = self.restrict(theta=theta)
        # fill it with random numbers from my initializer
        # note that θ is a MatrixView object, pass its capsule (not data) to CPython
        altar.libaltar.uniform_sample(self.support, θ.capsule, self.rng.rng)
        # and return
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

        # check the range
        altar.libaltar.uniform_verify(self.support, θ.capsule, mask.data)

        # all done; return the rejection map
        return mask
        
    @altar.export
    def computePrior(self, theta, density):
        """
        Fill my portion of {likelihood} with the densities of the samples in {theta}
        """
        # get my pdf implementation
        pdf = self.pdf
        # grab the portion of the sample that's mine
        θ = self.restrict(theta=theta)
        # find out how may samples there are
        samples = θ.rows
        
        # initialize logPDF (local) 
        log_density = self.log_density
        if log_density is None:
            log_density = altar.vector(shape=samples)
        # compute logPDF for given  
        altar.libaltar.uniform_logpdf(self.support, θ.capsule, log_density.data)
        # add it to global priorPDF 
        density += log_density

        # all done
        return self
        
    
    #local members
    log_density = None
    rng=None

# end of file

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
    mean = altar.properties.float(default=0)
    mean.doc = "the mean value of the distribution"

    sigma = altar.properties.float(default=1)
    sigma.doc = "the standard deviation of the distribution"


    # protocol obligations
    @altar.export
    def initialize(self, rng):
        """
        Initialize with the given random number generator
        """
        # set up my pdf
        self.pdf = altar.pdf.gaussian(rng=rng.rng, mean=self.mean, sigma=self.sigma)
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
        altar.libaltar.gaussian_sample(self.mean, self.sigma, θ.capsule, self.rng.rng)
        # and return
        return self

    @altar.export
    def verify(self, theta, mask):
        """
        Check whether my portion of the samples in {theta} are consistent with my constraints, and
        update {mask}, a vector with zeroes for valid samples and non-zero for invalid ones
        """
        # all samples are valid, so there is nothing to do
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
        altar.libaltar.gaussian_logpdf(self.mean, self.sigma, θ.capsule, log_density.data)
        # add it to global priorPDF 
        density += log_density

        # all done
        return self
        
    log_density = None
    rng = None

# end of file

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


# the protocol
class Distribution(altar.protocol, family="altar.distributions"):
    """
    The protocol that all AlTar probability distributions must satisfy
    """


    # requirements
    # user configurable state
    parameters = altar.properties.int()
    parameters.doc = "the number of model parameters that i take care of"

    offset = altar.properties.int(default=0)
    offset.doc = "the starting point of my parameters in the overall model state"


    # configuration
    @altar.provides
    def initialize(self, **kwds):
        """
        Initialize with the given random number generator
        """


    # model support
    @altar.provides
    def initializeSample(self, theta):
        """
        Fill my portion of {theta} with initial random values from my distribution.
        """

    @altar.provides
    def priorLikelihood(self, theta, prior):
        """
        Fill my portion of {prior} with the likelihoods of the samples in {theta}
        """

    @altar.provides
    def verify(self, theta, mask):
        """
        Check whether my portion of the samples in {theta} are consistent with my constraints, and
        update {mask}, a vector with zeroes for valid samples and non-zero for invalid ones
        """

    # wrappers over the interface of the underlying support
    @altar.provides
    def sample(self):
        """
        Sample the distribution using a random number generator
        """

    @altar.provides
    def density(self, x):
        """
        Compute the probability density of the distribution at {x}
        """

    @altar.provides
    def vector(self, vector):
        """
        Fill {vector} with random values
        """

    @altar.provides
    def matrix(self, matrix):
        """
        Fill {matrix} with random values
        """

    # framework hooks
    @classmethod
    def pyre_default(cls):
        """
        Supply a default implementation
        """
        # use the uniform distribution
        from .Uniform import Uniform as default
        # and return it
        return default


# end of file

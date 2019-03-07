# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2019 parasim inc
# (c) 2010-2019 california institute of technology
# all rights reserved
#


# the package
import altar


# the parameter set protocol
class ParameterSet(altar.protocol, family="altar.models.parameters"):
    """
    The protocol that all AlTar parameter sets must implement
    """


    # required state
    count = altar.properties.int(default=1)
    count.doc = "the number of parameters in this set"

    prior = altar.distributions.distribution()
    prior.doc = "the prior distribution"

    prep = altar.distributions.distribution()
    prep.doc = "the distribution to use to initialize this parameter set"


    # required behavior
    @altar.provides
    def initialize(self, model, offset):
        """
        Initialize the parameter set given the {model} that owns it
        """

    @altar.provides
    def initializeSample(self, theta):
        """
        Fill {theta} with an initial random sample from my prior distribution.
        """

    @altar.provides
    def priorLikelihood(self, theta, priorLLK):
        """
        Fill {priorLLK} with the likelihoods of the samples in {theta} in my prior distribution
        """

    @altar.provides
    def verify(self, theta, mask):
        """
        Check whether the samples in {theta} are consistent with the model requirements and update
        the {mask}, a vector with zeroes for valid samples and non-zero for invalid ones
        """

    # framework hooks
    @classmethod
    def pyre_default(cls, **kwds):
        """
        Supply a default implementation
        """
        # there is currently only one option...
        from .Contiguous import Contiguous as contiguous
        # so publish it
        return contiguous


# end of file

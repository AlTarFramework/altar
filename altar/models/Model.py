# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2018 parasim inc
# (c) 2010-2018 california institute of technology
# all rights reserved
#

# the package
import altar


# the model protocol
class Model(altar.protocol, family="altar.models"):
    """
    The protocol that all AlTar models must implement
    """


    # required behavior
    # high level interface
    @altar.provides
    def posterior(self, application):
        """
        Sample my posterior distribution
        """

    # services for the simulation controller
    @altar.provides
    def initialize(self, application):
        """
        Initialize the state of the model given a {problem} specification
        """

    @altar.provides
    def initializeSample(self, step):
        """
        Fill {step.theta} with an initial random sample from my prior distribution.
        """

    @altar.provides
    def computePrior(self, step):
        """
        Fill {step.prior} with the densities of the samples in {step.theta} in the prior
        distribution
        """

    @altar.provides
    def computeDataLikelihood(self, step):
        """
        Fill {step.data} with the densities of the samples in {step.theta} given the available
        data. This is what is usually referred to as the "forward model"
        """

    @altar.provides
    def computePosterior(self, step):
        """
        Given the {step.prior} and {step.data} densities, compute a generalized posterior using
        {step.beta} and deposit the result in {step.post}
        """

    @altar.provides
    def densities(self, step):
        """
        Convenience function that computes all three densities at once given the current {step}
        of the problem
        """

    @altar.provides
    def verify(self, step, mask):
        """
        Check whether the samples in {step.theta} are consistent with the model requirements and
        update the {mask}, a vector with zeroes for valid samples and non-zero for invalid ones
        """
        
    @altar.provides
    def update(self, annealer):
        """
        Perform any updates to the model 
        """

    # notifications
    @altar.provides
    def top(self, step):
        """
        Notification that a β step is about to start
        """

    @altar.provides
    def bottom(self, step):
        """
        Notification that a β step just ended
        """


    # framework hooks
    @classmethod
    def pyre_default(cls, **kwds):
        """
        Supply a default implementation
        """
        # pull the trivial model
        from .Null import Null as default
        # and return it
        return default


# end of file

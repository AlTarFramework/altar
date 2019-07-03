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
# my base class
from .Bayesian import Bayesian


# declaration
class Null(Bayesian, family="altar.models.null"):
    """
    A trivial model that can be used as a base class for deriving interesting ones
    """


    # user configurable state
    parameters = altar.properties.int(default=1)
    parameters.doc = "the number of model degrees of freedom"


    # protocol obligations
    @altar.export
    def initializeSample(self, step):
        """
        Fill {step.θ} with an initial random sample from my prior distribution
        """
        # the value of all my parameters
        value = 1
        # grab the portion of the sample that's mine
        θ = self.restrict(theta=step.theta)
        # fill it with my value
        θ.fill(value)
        # all done
        return self


    @altar.export
    def priorLikelihood(self, step):
        """
        Fill {step.prior} with the likelihoods of the samples in {step.theta} in the prior
        distribution
        """
        # do nothing
        return self


    @altar.export
    def dataLikelihood(self, step):
        """
        Fill {step.data} with the likelihoods of the samples in {step.theta} given the available
        data. This is what is usually referred to as the "forward model"
        """
        # do nothing
        return self


    @altar.export
    def verify(self, step, mask):
        """
        Check whether the samples in {step.theta} are consistent with the model requirements and
        update the {mask}, a vector with zeroes for valid samples and non-zero for invalid ones
        """
        # do nothing
        return mask


# end of file

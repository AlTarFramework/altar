# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2020 parasim inc
# (c) 2010-2020 california institute of technology
# all rights reserved
#


# my superclass
from .Bayesian import Bayesian


# declaration
class Ensemble(Bayesian, family="altar.models.ensemble"):
    """
    A collection of AlTar models that comprise a single model
    """

    # my collection
    models = altar.properties.list(schema=model())
    models.doc = "the collection of models in this ensemble"


    # protocol obligations
    @altar.export
    def initialize(self, application):
        """
        Initialize the state of the model given an {application} context
        """
        # chain up
        super().initialize(application=application)

        # go through my models
        for model in self.models:
            # and initialize each one
            model.initialize(application=application)

        # all done
        return self


    # services
    @altar.export
    def initializeSample(self, step):
        """
        Fill {step.theta} with an initial random sample from my prior distribution.
        """
        # ask each of my models
        for model in self.models:
            # to initialize their portion of the samples in {step}
            model.initializeSample(step=step)
        # all done
        return self


    @altar.export
    def priorLikelihood(self, step):
        """
        Fill {step.prior} with the likelihoods of the samples in {step.theta} in the prior
        distribution
        """
        # ask each of my models
        for model in self.models:
            # to contribute to the computation of the prior likelihood
            model.priorLikelihood(step=step)
        # all done
        return self


    @altar.export
    def dataLikelihood(self, step):
        """
        Fill {step.data} with the likelihoods of the samples in {step.theta} given the available
        data. This is what is usually referred to as the "forward model"
        """
        # ask each of my models
        for model in self.models:
            # to contribute to the computation of the data likelihood
            model.priorLikelihood(step=step)
        # all done
        return self


    @altar.export
    def verify(self, step, mask):
        """
        Check whether the samples in {step.theta} are consistent with the model requirements and
        update the {mask}, a vector with zeroes for valid samples and non-zero for invalid ones
        """
        # ask each of my models
        for model in self.models:
            # to initialize their portion of the samples in {step}
            model.verify(step=step, mask=mask)
        # all done
        return mask


# end of file

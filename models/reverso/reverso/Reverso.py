# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis (michael.aivazis@para-sim.com)
# grace bato           (mary.grace.p.bato@jpl.nasa.gov)
# eric m. gurrola      (eric.m.gurrola@jpl.nasa.gov)
#
# (c) 2013-2020 parasim inc
# (c) 2010-2020 california institute of technology
# all rights reserved


# framework
import altar


# model declaration
class Reverso(altar.models.bayesian, family="altar.models.reverso"):
    """
    An implementation of the Reverso 2-Magma Chamber Volcano Model, Reverso et al. [2014]
    """


    # user configurable state
    # the workspace name
    case = altar.properties.path(default="synthetic")
    case.doc = "the directory with the input files; output will be placed here as well"

    # the computational strategy to use
    mode = altar.properties.str(default="analytic")
    mode.doc = "the implementation strategy"
    mode.validators = altar.constraints.isMember("ode", "analytic")

    # the norm to use for computing the data log likelihood
    norm = altar.norms.norm()
    norm.default = altar.norms.l2()
    norm.doc = "the norm to use when computing the data log likelihood"

    # the number of observations
    observations = altar.properties.int()
    observations.doc = "the number of data points"

    # model parameters; the layout is dynamic and specified in the configuration file
    psets = altar.properties.dict(schema=altar.models.parameters())
    psets.doc = "the model parameter layout specification"

    # material parameters

    # public data
    parameters = 0  # adjusted during model initialization
    strategy = None # the engine that computes the data log likelihood; based on "mode" above


    # framework obligations
    @altar.export
    def initialize(self, application):
        """
        Initialize the state of the model given a problem specification
        """
        # chain up
        super().initialize(application=application)
        # initialize the parameter sets
        self.initializeParameterSets()

        # all done
        return self


    @altar.export
    def initializeSample(self, step):
        """
        Fill {step.θ} with an initial random sample from my prior distribution.
        """
        # grab the portion of the sample that's mine
        θ = self.restrict(theta=step.theta)
        # go through each parameter set
        for pset in self.psets.values():
            # and ask each one to {prep} the sample
            pset.initializeSample(theta=θ)
        # and return
        return self


    @altar.export
    def priorLikelihood(self, step):
        """
        Fill {step.prior} with the likelihoods of the samples in {step.theta} in the prior
        distribution
        """
        # grab the portion of the sample that's mine
        θ = self.restrict(theta=step.theta)
        # and the storage for the prior likelihoods
        likelihood = step.prior
        # go through each parameter set
        for pset in self.psets.values():
            # and ask each one to compute the prior of the sample
            pset.priorLikelihood(theta=θ, priorLLK=likelihood)
        # all done
        return self


    @altar.export
    def dataLikelihood(self, step):
        """
        Fill {step.data} with the likelihoods of the samples in {step.theta} given the available
        data. This is what is usually referred to as the "forward model"
        """
        # get my strategy
        strategy = self.strategy
        # deploy
        strategy.dataLikelihood(model=self, step=step)
        # all done
        return self


    @altar.export
    def verify(self, step, mask):
        """
        Check whether the samples in {step.theta} are consistent with the model requirements and
        update the {mask}, a vector with zeroes for valid samples and non-zero for invalid ones
        """
        # grab the portion of the sample that's mine
        θ = self.restrict(theta=step.theta)
        # go through each parameter set
        for pset in self.psets.values():
            # and ask each one to verify the sample
            pset.verify(theta=θ, mask=mask)
        # all done; return the rejection map
        return mask


    # implementation details
    def initializeParameterSets(self):
        """
        Initialize my parameter sets
        """
        # compile the parameter layout
        # get the parameter sets
        psets = self.psets
        # initialize the offset
        offset = 0

        # go through my parameter sets
        for name, pset in psets.items():
            # initialize the parameter set
            offset += pset.initialize(model=self, offset=offset)
        # the total number of parameters is now known, so record it
        self.parameters = offset

        # record the layout of the sample vector
        # transfer the offsets of the various slots to members

        # all done
        return


# end of file

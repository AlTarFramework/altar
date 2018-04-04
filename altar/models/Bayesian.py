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
# my protocol
from .Model import Model as model


# declaration
class Bayesian(altar.component, family="altar.models.bayesian", implements=model):
    """
    The base class of AlTar models that are compatible with Bayesian explorations
    """


    # user configurable state
    controller = altar.bayesian.controller()
    controller.doc = "my simulation controller"


    # protocol obligations
    @altar.export
    def posterior(self, application):
        """
        Sample my posterior distribution
        """
        # initialize my parts
        self.initialize(application=application)
        # ask my controller to help me sample my posterior distribution
        return self.controller.posterior(model=self)


    @altar.export
    def parameters(self):
        """
        Return the number of parameters in the model
        """
        # i don't know what to do, so...
        raise NotImplementedError(f"model '{type(self).__name__}' must implement 'parameters'")


    # services
    @altar.export
    def sample(self, step):
        """
        Fill {step.theta} with an initial random sample from my prior distribution.
        """

    @altar.export
    def priorLikelihood(self, step):
        """
        Fill {step.prior} with the likelihoods of the samples in {step.theta} in the prior
        distribution
        """


    @altar.export
    def dataLikelihood(self, step):
        """
        Fill {step.data} with the likelihoods of the samples in {step.theta} given the available
        data. This is what is usually referred to as the "forward model"
        """

    @altar.export
    def posteriorLikelihood(self, step):
        """
        Given the {step.prior} and {step.data} likelihoods, compute a generalized posterior using
        {step.beta} and deposit the result in {step.post}
        """

    @altar.export
    def likelihoods(self, step):
        """
        Convenience function that computes all three likelihoods at once given the current {step}
        of the problem
        """

    @altar.export
    def verify(self, step):
        """
        Check whether the samples in {step.theta} are consistent with the model requirements and
        return a vector with zeroes for valid samples and ones for the invalid ones
        """

    # implementation details
    @altar.export
    def initialize(self, application):
        """
        Initialize the state of the model given a {problem} specification
        """
        # get the job parameters
        self.job = application.job
        # borrow the journal channels
        self.info = application.info
        self.warning = application.warning
        self.error = application.error
        self.debug = application.debug
        self.firewall = application.firewall

        # initialize my controller
        self.controller.initialize(model=self)

        # all done
        return self


    # public data
    # job parameters
    job = None
    # journal channels
    info = None
    warning = None
    error = None
    default = None
    firewall = None


# end of file

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
    rng = altar.simulations.rng()
    rng.doc = "the random number generator"

    controller = altar.bayesian.controller()
    controller.doc = "my simulation controller"

    offset = altar.properties.int(default=0)
    offset.doc = "the starting point of my state in the overall controller state"

    parameters = altar.properties.int(default=2)
    parameters.doc = "the number of model degrees of freedom"


    # protocol obligations
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

        # initialize my parts
        self.rng.initialize()
        self.controller.initialize(model=self)

        # all done
        return self


    @altar.export
    def posterior(self, application):
        """
        Sample my posterior distribution
        """
        # ask my controller to help me sample my posterior distribution
        return self.controller.posterior(model=self)


    # services
    @altar.export
    def initializeSample(self, step):
        """
        Fill {step.theta} with an initial random sample from my prior distribution.
        """
        # i don't know what to do, so...
        raise NotImplementedError(
            f"model '{type(self).__name__}' must implement 'initializeSample'")


    @altar.export
    def priorLikelihood(self, step):
        """
        Fill {step.prior} with the likelihoods of the samples in {step.theta} in the prior
        distribution
        """
        # i don't know what to do, so...
        raise NotImplementedError(
            f"model '{type(self).__name__}' must implement 'priorLikelihood'")


    @altar.export
    def dataLikelihood(self, step):
        """
        Fill {step.data} with the likelihoods of the samples in {step.theta} given the available
        data. This is what is usually referred to as the "forward model"
        """
        # i don't know what to do, so...
        raise NotImplementedError(
            f"model '{type(self).__name__}' must implement 'dataLikelihood'")


    @altar.export
    def posteriorLikelihood(self, step):
        """
        Given the {step.prior} and {step.data} likelihoods, compute a generalized posterior using
        {step.beta} and deposit the result in {step.post}
        """
        # prime the posterior
        step.posterior.copy(step.prior)
        # compute it; this expression reduces to Bayes' theorem for β->1
        altar.blas.daxpy(step.beta, step.data, step.posterior)
        # all done
        return self


    @altar.export
    def likelihoods(self, step):
        """
        Convenience function that computes all three likelihoods at once given the current {step}
        of the problem
        """
        # first the prior
        self.priorLikelihood(step=step)
        # now the likelihood of the prior given the data
        self.dataLikelihood(step=step)
        # finally, the posterior at this temperature
        self.posteriorLikelihood(step=step)
        # bundle them and return them
        return self


    @altar.export
    def verify(self, step):
        """
        Check whether the samples in {step.theta} are consistent with the model requirements and
        return a vector with zeroes for valid samples and ones for the invalid ones
        """
        # i don't know what to do, so...
        raise NotImplementedError(
            f"model '{type(self).__name__}' must implement 'verify'")


    # implementation details
    def restrict(self, step):
        """
        Return the portion of the {sample} matrix in {step} that reflect the state maintained by me
        """
        # find out how many samples in the set
        samples = step.samples
        # get my parameter count
        parameters = self.parameters
        # get my offset in the samples
        offset = self.offset

        # find where my samples live within the overall sample matrix:
        start = 0, self.offset
        # form the shape of the sample matrix that's mine
        shape = step.samples, self.parameters

        # grab the portion of the sample that's mine: i own data in all sample rows, starting
        # in the column indicated by my {offset}, and the width of my block is determined by my
        # parameter count
        θ = step.theta.view(start=(0,offset), shape=(samples,parameters))

        # return it
        return θ


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

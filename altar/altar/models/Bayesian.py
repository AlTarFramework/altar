# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2020 parasim inc
# (c) 2010-2020 california institute of technology
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
    offset = altar.properties.int(default=0)
    offset.doc = "the starting point of my state in the overall controller state"

    parameters = altar.properties.int(default=1)
    parameters.doc = "the number of model degrees of freedom"


    # public data
    rng = None
    controller = None


    # protocol obligations
    @altar.export
    def initialize(self, application):
        """
        Initialize the state of the model given an {application} context
        """
        # get the job parameters
        self.job = application.job
        # borrow the journal channels
        self.info = application.info
        self.warning = application.warning
        self.error = application.error
        self.debug = application.debug
        self.firewall = application.firewall

        # save the random number generator
        self.rng = application.rng
        # and the controller
        self.controller = application.controller

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
    def likelihoods(self, annealer, step):
        """
        Convenience function that computes all three likelihoods at once given the current {step}
        of the problem
        """
        # grab the dispatcher
        dispatcher = annealer.dispatcher

        # notify we are about to compute the prior likelihood
        dispatcher.notify(event=dispatcher.priorStart, controller=annealer)
        # compute the prior likelihood
        self.priorLikelihood(step=step)
        # done
        dispatcher.notify(event=dispatcher.priorFinish, controller=annealer)


        # notify we are about to compute the likelihood of the prior given the data
        dispatcher.notify(event=dispatcher.dataStart, controller=annealer)
        # compute it
        self.dataLikelihood(step=step)
        # done
        dispatcher.notify(event=dispatcher.dataFinish, controller=annealer)

        # finally, notify we are about to put together the posterior at this temperature
        dispatcher.notify(event=dispatcher.posteriorStart, controller=annealer)
        # compute it
        self.posteriorLikelihood(step=step)
        # done
        dispatcher.notify(event=dispatcher.posteriorFinish, controller=annealer)

        # enable chaining
        return self


    @altar.export
    def verify(self, step, mask):
        """
        Check whether the samples in {step.theta} are consistent with the model requirements and
        update the {mask}, a vector with zeroes for valid samples and non-zero for invalid ones
        """
        # i don't know what to do, so...
        raise NotImplementedError(
            f"model '{type(self).__name__}' must implement 'verify'")


    # notifications
    @altar.export
    def top(self, step):
        """
        Notification that a β step is about to start
        """
        # nothing to do
        return self


    @altar.export
    def bottom(self, step):
        """
        Notification that a β step just ended
        """
        # nothing to do
        return self


    # implementation details
    def restrict(self, theta):
        """
        Return my portion of the sample matrix {theta}
        """
        # find out how many samples in the set
        samples = theta.rows
        # get my parameter count
        parameters = self.parameters
        # get my offset in the samples
        offset = self.offset

        # find where my samples live within the overall sample matrix:
        start = 0, offset
        # form the shape of the sample matrix that's mine
        shape = samples, parameters

        # return a view to the portion of the sample that's mine: i own data in all sample
        # rows, starting in the column indicated by my {offset}, and the width of my block is
        # determined by my parameter count
        return theta.view(start=start, shape=shape)


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

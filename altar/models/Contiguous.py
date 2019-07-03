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
# the protocol
from .ParameterSet import ParameterSet as parameters


# component
class Contiguous(altar.component,
                 family="altar.models.parameters.contiguous", implements=parameters):
    """
    A contiguous parameter set
    """


    # user configurable state
    count = altar.properties.int(default=1)
    count.doc = "the number of parameters in this set"

    prior = altar.distributions.distribution()
    prior.doc = "the prior distribution"

    prep = altar.distributions.distribution()
    prep.doc = "the distribution to use to initialize this parameter set"


    # state set by the model
    offset = 0 # adjusted by the model after the full set of parameters is known


    # interface
    @altar.export
    def initialize(self, model, offset):
        """
        Initialize my state given the {model} that owns me
        """
        # set my offset
        self.offset = offset

        # get my count
        count = self.count
        # adjust the number of parameters of my distributions
        self.prep.parameters = self.prior.parameters = count

        # get the random number generator
        rng = model.rng
        # initialize my distributions
        self.prep.initialize(rng=rng)
        self.prior.initialize(rng=rng)

        # return my parameter count so the next set can be initialized properly
        return count


    @altar.export
    def initializeSample(self, theta):
        """
        Fill {theta} with an initial random sample from my prior distribution.
        """
        # grab the portion of the sample that belongs to me
        θ = self.restrict(theta=theta)
        # fill it with random numbers from my {prep} distribution
        self.prep.initializeSample(theta=θ)
        # all done
        return self


    @altar.export
    def priorLikelihood(self, theta, priorLLK):
        """
        Fill {priorLLK} with the log likelihoods of the samples in {theta} in my prior distribution
        """
        # grab the portion of the sample that's mine
        θ = self.restrict(theta=theta)
        # delegate
        self.prior.priorLikelihood(theta=θ, likelihood=priorLLK)
        # all done
        return self


    @altar.export
    def verify(self, theta, mask):
        """
        Check whether the samples in {step.theta} are consistent with the model requirements and
        update the {mask}, a vector with zeroes for valid samples and non-zero for invalid ones
        """
        # grab the portion of the sample that's mine
        θ = self.restrict(theta=theta)
        # grab my prior
        pdf = self.prior
        # ask it to verify my samples
        pdf.verify(theta=θ, mask=mask)
        # all done; return the rejection map
        return mask


    # implementation details
    def restrict(self, theta):
        """
        Return my portion of the sample matrix {theta}
        """
        # find out how many samples in the set
        samples = theta.rows
        # get my parameter count
        parameters = self.count
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


# end of file

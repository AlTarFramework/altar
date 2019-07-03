# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2019 parasim inc
# (c) 2010-2019 california institute of technology
# all rights reserved
#

# externals
import math
# get the package
import altar

# get the protocol
from . import distribution


# the declaration
class Base(altar.component, implements=distribution):
    """
    The base class for probability distributions
    """


    # protocol obligations
    # user configurable state
    parameters = altar.properties.int()
    parameters.doc = "the number of model parameters that belong to me"

    offset = altar.properties.int(default=0)
    offset.doc = "the starting point of my parameters in the overall model state"


    # configuration
    @altar.export
    def initialize(self, rng):
        """
        Initialize with the given random number generator
        """
        # being abstract, i don't know what to do here
        raise NotImplementedError(
            f"class '{type(self).__name__}' must implement 'initialize'")


    @altar.export
    def initializeSample(self, theta):
        """
        Fill my portion of {theta} with initial random values from my distribution.
        """
        # grab the portion of the sample that's mine
        θ = self.restrict(theta=theta)
        # fill it with random numbers from my initializer
        self.pdf.matrix(matrix=θ)
        # and return
        return self


    @altar.export
    def priorLikelihood(self, theta, likelihood):
        """
        Fill my portion of {likelihood} with the likelihoods of the samples in {theta}
        """
        # get my pdf implementation
        pdf = self.pdf
        # grab the portion of the sample that's mine
        θ = self.restrict(theta=theta)
        # find out how may samples there are
        samples = θ.rows

        # for each one
        for sample in range(samples):
            # fill the vector with the log likelihoods
            likelihood[sample] += sum(
                math.log(pdf.density(parameter)) for parameter in θ.getRow(sample))

        # all done
        return self


    @altar.export
    def verify(self, theta, mask):
        """
        Check whether my portion of the samples in {theta} are consistent with my constraints, and
        update {mask}, a vector with zeroes for valid samples and non-zero for invalid ones
        """
        # being abstract, i don't know what to do here
        raise NotImplementedError(
            f"class '{type(self).__name__}' must implement 'verify'")


    # the forwarding interface
    @altar.export
    def sample(self):
        """
        Sample the distribution using a random number generator
        """
        # ask my pdf
        return self.pdf.sample()


    @altar.export
    def density(self, x):
        """
        Compute the probability density of the distribution at {x}
        """
        # ask my pdf
        return self.pdf.density(x)


    @altar.export
    def vector(self, vector):
        """
        Fill {vector} with random values
        """
        # ask my pdf
        return self.pdf.vector(vector)


    @altar.export
    def matrix(self, matrix):
        """
        Fill {matrix} with random values
        """
        # ask my pdf
        return self.pdf.matrix(matrix)


    # implementation details
    def restrict(self, theta):
        """
        Return my portion of the {theta}
        """
        # find out how many samples in the set
        samples = theta.rows
        # get my parameter count
        parameters = self.parameters
        # get my offset in the samples
        offset = self.offset

        # find where my samples live within the overall sample matrix:
        start = 0, self.offset
        # form the shape of the sample matrix that's mine
        shape = samples, parameters

        # return the portion of the sample that's mine: i own data in all sample rows, starting
        # in the column indicated by my {offset}, and the width of my block is determined by my
        # parameter count
        return theta.view(start=start, shape=shape)


    # private data
    pdf = None # the pdf implementation


# end of file

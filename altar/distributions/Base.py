# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2018 parasim inc
# (c) 2010-2018 california institute of technology
# all rights reserved
#

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
    @altar.provides
    def initialize(self, rng):
        """
        Initialize with the given runtime {context}
        """
        # being abstract, i don't know what to do here
        raise NotImplementedError(
            f"class '{type(self).__name__}' must implement 'initialize'")


    @altar.provides
    def sample(self):
        """
        Sample the distribution using a random number generator
        """
        # ask my pdf
        return self.pdf.sample()


    @altar.provides
    def density(self, x):
        """
        Compute the probability density of the distribution at {x}
        """
        # ask my pdf
        return self.pdf.density(x)


    @altar.provides
    def vector(self, vector):
        """
        Fill {vector} with random values
        """
        # ask my pdf
        return self.pdf.vector(vector)


    @altar.provides
    def matrix(self, matrix):
        """
        Fill {matrix} with random values
        """
        # ask my pdf
        return self.pdf.matrix(matrix)


    # private data
    pdf = None # the pdf implementation


# end of file

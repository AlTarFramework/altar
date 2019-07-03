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
# my protocol
from .RNG import RNG as rng


# the random number generator
class GSLRNG(altar.component, family="altar.simulations.rng.gsl", implements=rng):
    """
    The protocol for random number generators
    """


    # user configurable state
    seed = altar.properties.float(default=0)
    seed.doc = 'the number with which to seed the generator'

    algorithm = altar.properties.str(default='ranlxs2')
    algorithm.doc = 'the random number generator algorithm'


    # public data
    rng = None # the handle to the wrapper from the {gsl} package


    # required behavior
    @altar.export
    def initialize(self, **kwds):
        """
        Initialize the random number generator
        """
        # nothing to do
        return self


    # meta-methods
    def __init__(self, **kwds):
        # chain  up
        super().__init__(**kwds)
        # build the random number generator
        self.rng = altar.rng(algorithm=self.algorithm)
        # and seed
        self.rng.seed(seed=self.seed)
        # all done
        return


    # implementation details
    def show(self):
        """
        Display some information about me
        """
        # get the journal
        import journal
        # make a channel
        channel = journal.debug("altar.init")
        # show me
        channel.line(f"{self.pyre_name}:")
        channel.line(f"       seed: {self.seed}")
        channel.line(f"  algorithm: {self.algorithm}")
        channel.log()
        # all done
        return self


# end of file

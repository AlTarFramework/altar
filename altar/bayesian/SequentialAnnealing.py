# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2019 parasim inc
# (c) 2010-2019 california institute of technology
# all rights reserved
#


# superclass
from .AnnealingMethod import AnnealingMethod


# declaration
class SequentialAnnealing(AnnealingMethod):
    """
    Implementation that assumes its state is the global state of the solver, and therefore it
    is able to compute the statistical properties of the sample distribution
    """


    # public data
    wid = 0     # my worker id
    workers = 1 # i don't manage anybody else


    # interface
    def start(self, annealer):
        """
        Start the annealing process
        """
        # chain up
        super().start(annealer=annealer)
        # build a cooling step to hold the state of the problem
        self.step = self.CoolingStep.start(annealer=annealer)
        # all done
        return self


# end of file

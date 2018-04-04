# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2018 parasim inc
# (c) 2010-2018 california institute of technology
# all rights reserved
#


# declaration
class AnnealingMethod:
    """
    Base class for the various annealing implementation strategies
    """


    # types
    from .CoolingStep import CoolingStep


    # public data
    step = None # the current state of the solver
    iteration = 0 # my iteration counter
    workers = None # the total number of chain processors

    @property
    def beta(self):
        """
        Return the temperature of my current step
        """
        # easy enough
        return self.step.beta


    # interface
    def start(self, annealer):
        """
        Start the annealing process from scratch
        """
        # reset my iteration count
        self.iteration = 0
        # all done
        return self


    def restart(self, annealer):
        """
        Start the annealing process from a checkpoint
        """
        # NYI
        raise NotImplementedError()


    def top(self, annealer):
        """
        Notification that we are at the beginning of an update
        """
        # all done
        return self


    def cool(self, annealer):
        """
        Push my state forward along the cooling schedule
        """
        # get the scheduler
        scheduler = annealer.scheduler
        # ask it to update my step
        scheduler.update(step=self.step)
        # update the iteration counter
        self.iteration += 1
        # all done
        return self


    def resample(self, annealer):
        """
        Re-sample the posterior distribution
        """
        # get the sampler
        sampler = annealer.sampler
        # ask it to sample the posterior pdf
        stats = sampler.sample(annealer=annealer, step=self.step)
        # return the acceptance statistics
        return stats


    def equilibrate(self, annealer, statistics):
        """
        Analyze the acceptance statistics and take the problem state to the end of the
        annealing step
        """
        # get the sampler
        sampler = annealer.sampler
        # ask it to adjust the sample statistics
        sampler.equilibrate(annealer=annealer, statistics=statistics)
        # all done
        return self


    def bottom(self, annealer):
        """
        Notification that we are at the bottom of an update
        """
        # all done
        return self


    def finish(self, annealer):
        """
        The annealing process is complete
        """
        # all done
        return self


    # meta-methods
    def __init__(self, annealer, **kwds):
        # chain up; absorb the {annealer}
        super().__init__(**kwds)
        # all done
        return


# end of file

# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2018 parasim inc
# (c) 2010-2018 california institute of technology
# all rights reserved
#


# externals
import mpi
import journal
# the framework
import altar
# superclass
from .AnnealingMethod import AnnealingMethod


# declaration
class MPIAnnealing(AnnealingMethod):
    """
    A distributed implementation of the annealing method that uses MPI
    """


    # interface
    def initialize(self, application):
        """
        Initialize me and my parts given an {application} context
        """
        # ask the application context for the rng component
        rng = application.rng
        # make a rank dependent seed
        seed = rng.seed + 29*(self.rank+1) + 1
        # seed the rng
        rng.rng.seed(seed=seed)

        # chain up
        return super().initialize(application=application)


    def start(self, annealer):
        """
        Start the annealing process
        """
        # chain up
        super().start(annealer=annealer)
        # everybody has to get ready
        self.worker.start(annealer=annealer)
        # collect the global state: at the master task, I get the entire state of the problem;
        # at the other tasks, I just get a reference to the local state so I have uniform
        # access to the annealing temperature
        self.step = self.collect()
        # all done
        return self


    def top(self, annealer):
        """
        Notification that we are at the beginning of an update
        """
        # if i am the manager task
        if self.rank == self.manager:
            # chain up
            return super().top(annealer=annealer)
        # otherwise, do nothing
        return self


    def cool(self, annealer):
        """
        Push my state forward along the cooling schedule
        """
        # am I the boss?
        if self.rank == self.manager:
            # i have the global state; cool it
            super().cool(annealer=annealer)
        # all done
        return self


    def resample(self, annealer):
        """
        Re-sample the posterior pdf
        """
        # partition and synchronize my state
        self.partition()
        # everybody resamples the posterior
        stats = self.worker.resample(annealer=annealer)
        # collect my state
        self.step = self.collect()
        # return the statistics
        return stats


    def equilibrate(self, annealer, statistics):
        """
        Analyze the acceptance statistics and take the problem state to the end of the
        annealing step
        """
        # who is the boss?
        manager = self.manager
        # unpack the acceptance/rejection statistics
        accepted, rejected, unlikely = statistics

        # add up the acceptance/rejection statistics from all the nodes
        accepted = self.communicator.sum(accepted, destination=manager)
        rejected = self.communicator.sum(rejected, destination=manager)
        unlikely = self.communicator.sum(unlikely, destination=manager)

        # if I am the boss
        if self.rank == manager:
            # chain up
            super().equilibrate(annealer=annealer, statistics=(accepted,rejected,unlikely))

        # all done
        return self


    def finish(self, annealer):
        """
        Shut down the annealing process
        """
        # if i am the manager task
        if self.rank == self.manager:
            # chain up
            return super().finish(annealer=annealer)
        # otherwise, do nothing
        return self


        # all done
        return self


    # meta-methods
    def __init__(self, annealer,  worker, communicator=None, **kwds):
        # chain up
        super().__init__(annealer=annealer, **kwds)

        # make sure i have a valid communicator
        comm = communicator or mpi.world
        # attach it
        self.communicator = comm
        # store the number of tasks
        self.tasks = comm.size
        # and my rank
        self.rank = comm.rank

        # save the annealing method for each of my tasks
        self.worker = worker
        # compute the total number workers
        workers = comm.sum(destination=self.manager, item=worker.workers)
        # the result is meaningful only on the manager task
        self.workers = int(workers) if self.rank == self.manager else None

        # make a channel
        self.info = journal.info("altar.mpi")

        # all done
        return


    # implementation details
    def collect(self):
        """
        Assemble my global state
        """
        # get the communicator
        communicator = self.communicator
        # who's the boss?
        manager = self.manager
        # ask my worker for its local state
        step = self.worker.step
        # get the temperature
        β = step.beta
        # assemble the sample set
        θ = altar.matrix.collect(
            matrix=step.theta, communicator=communicator, destination=manager)
        # the prior
        prior = altar.vector.collect(
            vector=step.prior, communicator=communicator, destination=manager)
        # the data
        data = altar.vector.collect(
            vector=step.data, communicator=communicator, destination=manager)
        # the prior
        posterior = altar.vector.collect(
            vector=step.posterior, communicator=communicator, destination=manager)

        # if I am not the manager task, just return the local state
        if self.rank != self.manager: return step

        # everybody has the same covariance matrix
        Σ = step.sigma
        # otherwise, pack the state of the problem and return it
        return self.CoolingStep(beta=β, theta=θ, likelihoods=(prior,data,posterior), sigma=Σ)


    def partition(self):
        """
        Distribute my global state
        """
        # who is the boss
        manager = self.manager
        # am i the boss?
        if self.rank == manager:
            # grab my global state
            step = self.step
            # unpack it
            β = step.beta
            θ = step.theta
            Σ = step.sigma
            prior = step.prior
            data = step.data
            posterior = step.posterior
        # the others
        else:
            # know nothing
            β = θ = Σ = prior = data = posterior = None

        # cache my communicator
        comm = self.communicator
        # the partitioning modifies my local state, which kept on my behalf by the manager of
        # my local workers
        step = self.worker.step

        # everybody gets the temperature
        step.beta = comm.bcast(item=β, source=manager)

        # it is important not to disturb the memory held by the manager: threaded managers have
        # their workers set up views on the local state and we don't want to mess that up

        # grab my portion of the sample set
        step.theta.excerpt(matrix=θ, source=manager, communicator=comm)
        # my portion of the likelihoods
        step.prior.excerpt(vector=prior, source=manager, communicator=comm)
        step.data.excerpt(vector=data, source=manager, communicator=comm)
        step.posterior.excerpt(vector=posterior, source=manager, communicator=comm)

        # finally, the covariance matrix
        step.sigma.copy(altar.matrix.bcast(matrix=Σ, source=manager, communicator=comm))

        # all done
        return step


    # private data
    manager = 0 # the rank responsible for distributing and collecting the workload
    worker = None # the annealing method implementation; deduced at start up time


# end of file

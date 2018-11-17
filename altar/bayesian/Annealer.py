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
from .Controller import Controller as controller
# my event dispatcher
from .Notifier import Notifier


# my declaration
class Annealer(altar.component, family="altar.controllers.annealer", implements=controller):
    """
    A Bayesian controller that uses an annealing schedule and MCMC to approximate the posterior
    distribution of a model
    """


    # user configurable state
    sampler = altar.bayesian.sampler()
    sampler.doc = "the sampler of the posterior distribution"

    scheduler = altar.bayesian.scheduler()
    scheduler.doc = "the generator of the annealing schedule"

    dispatcher = altar.simulations.dispatcher(default=Notifier)
    dispatcher.doc = "the event dispatcher that activates the registered handlers"

    archiver = altar.simulations.archiver()
    archiver.doc = "the archiver of simulation state"


    # protocol obligations
    @altar.export
    def initialize(self, application):
        """
        Initialize me and my parts given an {application} context
        """
        # borrow the canonical journal channels from the application
        self.info = application.info
        self.warning = application.warning
        self.error = application.error
        self.debug = application.debug
        self.firewall = application.firewall

        # initialize the dispatcher
        self.dispatcher.initialize(application=application)

        # initialize my other parts
        self.sampler.initialize(application=application)
        self.scheduler.initialize(application=application)
        self.archiver.initialize(application=application)

        # deduce my annealing method
        self.worker = self.deduceAnnealingMethod(job=application.job)
        # and initialize it
        self.worker.initialize(application=application)

        # go through the registered monitors
        for monitor in application.monitors.values():
            # initialize them
            monitor.initialize(application=application)
            # and register them with the {dispatcher}
            self.dispatcher.register(monitor=monitor)

        # all done
        return self


    @altar.export
    def posterior(self, model):
        """
        Sample the posterior distribution
        """
        # record the model so that everybody has easy access to it
        self.model = model
        # unpack what we need
        tolerance = model.job.tolerance
        # get my worker
        worker = self.worker
        # and my dispatcher
        dispatcher = self.dispatcher

        # notify all interested parties that the simulation is about to start
        dispatcher.notify(event=dispatcher.start, controller=self)
        # start the process
        worker.start(annealer=self)

        # iterate until β is sufficiently close to one
        while worker.beta + tolerance < 1:
            # notify that we are at the top of the current step
            dispatcher.notify(event=dispatcher.betaStart, controller=self)
            # let the worker know
            worker.top(annealer=self)

            # compute a new temperature
            worker.cool(annealer=self)

            # notify we are about to walk the chains
            dispatcher.notify(event=dispatcher.walkChainsStart, controller=self)
            # walk the chains
            statistics = worker.walk(annealer=self)
            # notify we are done walking the chains
            dispatcher.notify(event=dispatcher.walkChainsFinish, controller=self)

            # notify we are about to resample
            dispatcher.notify(event=dispatcher.resampleStart, controller=self)
            # resample
            worker.resample(annealer=self, statistics=statistics)
            # notify we are done resampling
            dispatcher.notify(event=dispatcher.resampleFinish, controller=self)

            # notify the worker we are at the bottom of the current step
            worker.bottom(annealer=self)
            # and dispatch the matching event
            dispatcher.notify(event=dispatcher.betaFinish, controller=self)

        # and finish up
        worker.finish(annealer=self)
        # notify all interested parties that the simulation has finished
        dispatcher.notify(event=dispatcher.finish, controller=self)

        # forget the model
        self.model = None

        # all done; indicate success
        return 0


    # implementation details
    def deduceAnnealingMethod(self, job):
        """
        Instantiate an annealing method compatible the user choices
        """
        # the machine layout part of the {job} parameters has already been vetted; if we get
        # this far, we have what the user asked for; unpack the parameters we use
        mode = job.mode
        hosts = job.hosts
        tasks = job.tasks
        gpus = job.gpus

        # first let's figure out the base worker factory: if the user asked for gpus and we
        # have them, go CUDA, else use plain vanilla sequential

        # N.B.: we don't actually instantiate a worker here; just figure out how to make one;
        # the reason is that the threaded annealing method must be able to instantiate more
        # that one of these guys once we know the thread count
        worker = self.cuda if gpus > 0 else self.sequential

        # if i don't have mpi
        if mode != "mpi":
            # we need threads if either {tasks} or {gpus} is greater than one
            if gpus > 1 or tasks > 1:
                # compute the number  of threads we need
                threads = tasks * gpus or tasks or gpus
                # build the method
                worker = self.threaded(threads=threads, worker=worker)
            # otherwise
            else:
                # ask the factory for a worker instance
                worker = worker()
        # if we are running with mpi
        else:
            # i need threads if the number of {gpus} per task is greater than one
            if gpus > 1:
                # i need as many threads as there are gpus per task
                threads = gpus
                # build the worker
                worker = self.threaded(threads=threads, worker=worker)
            # otherwise
            else:
                # ask the factory for a worker instance
                worker = worker()

            # in any case, use the mpi aware annealing method
            worker = self.mpi(worker=worker)

        # all done
        return worker


    def sequential(self):
        """
        Instantiate the plain sequential annealing method
        """
        # import the sequential annealer
        from .SequentialAnnealing import SequentialAnnealing
        # instantiate it and return it
        return SequentialAnnealing(annealer=self)


    def cuda(self):
        """
        Instantiate a CUDA aware annealing method
        """
        # import the CUDA annealing method
        from .CUDAAnnealing import CUDAAnnealing
        # instantiate it and return it
        return CUDAAnnealing(annealer=self)


    def threaded(self, threads, worker):
        """
        Instantiate the multi-threaded annealing method
        """
        # get the threaded annealer
        from .ThreadedAnnealing import ThreadedAnnealing
        # instantiate it and return it
        return ThreadedAnnealing(annealer=self, threads=threads, worker=worker)


    def mpi(self, worker):
        """
        Instantiate the MPI aware annealing method
        """
        from .MPIAnnealing import MPIAnnealing
        # instantiate it and return it
        return MPIAnnealing(annealer=self, worker=worker)


    # private data
    model = None  # the model i'm sampling
    worker = None # the annealing method
    # journal channels shared with the application
    info = None
    warning = None
    error = None
    debug = None
    firewall = None


# end of file

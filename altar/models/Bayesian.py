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
    controller = altar.bayesian.controller()
    controller.doc = "my simulation controller"


    # protocol obligations
    @altar.export
    def posterior(self, app):
        """
        Sample my posterior distribution
        """
        # initialize my parts
        self.initialize(app=app)
        # ask my controller to help me sample my posterior distribution
        self.controller.posterior(model=self)
        # all done
        return


    # meta-methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # local state
        self.hosts = 1
        self.tasksPerHost = 1
        self.gpusPerTask = 0
        # all done
        return


    # implementation details
    def initialize(self, app):
        """
        Initialize the state of the model given a {problem} specification
        """
        # get the host
        host = self.pyre_executive.host
        # grab the journal channels
        self.info = app.info
        self.warning = app.warning
        self.error = app.error
        self.debug = app.debug
        self.firewall = app.firewall

        # grab the application shell
        shell = app.shell
        # if it's mpi capable
        if shell.model == "mpi":
            # record the machine layout
            self.hosts = shell.hosts
            self.tasksPerHost = shell.tasks

        # the hosts and tasks settings are vetted by the shell; let's figure out the GPU
        # situation; get what the user asked for
        gpus = app.gpus
        # attempt to
        try:
            # get support for cuda
            import cuda
        # if this fails
        except ImportError:
            # if the user asked for GPUs
            if gpus:
                # pick a channel
                channel = self.warning
                # complain
                channel.line(f"no runtime support for CUDA on '{host.hostname}'")
                channel.log(f" -- setting the number of GPUs per task to 0")
            # no GPUs
            self.gpusPerTask = 0
        # if it succeeds
        else:
            # unpack the requested resources
            tasks = self.tasksPerHost
            # get the requested number
            requested = tasks * gpus
            # get the total GPU count on this node
            available = cuda.manager.count
            # if the user asked for more than we have
            if requested > available:
                # be civilized
                avlLabel = "GPU" if requested == 1 else "GPUs"
                reqLabel = "GPU" if requested == 1 else "GPUs"
                gpuLabel = "GPU" if gpus == 1 else "GPUs"
                taskLabel = "task" if tasks == 1 else "tasks"
                # pick the channel
                channel = self.error
                # complain
                channel.line(f"not enough GPUs on '{host.hostname}':")
                channel.line(f" -- available: {available} {avlLabel}")
                channel.line(
                    f" -- requested: {requested} {reqLabel}: "
                    f"{tasks} {taskLabel} x {gpus} {gpuLabel} per task")
                channel.log()
                # and exit
                raise SystemExit(1)
            # otherwise, we are good
            self.gpusPerTask = gpus

        # initialize my controller
        self.controller.initialize(model=self)

        # all done
        return


# end of file

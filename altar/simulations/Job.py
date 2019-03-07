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
from .Run import Run as run


# the run protocol
class Job(altar.component, family="altar.simulations.runs.job", implements=run):
    """
    The set of parameters in an AlTar run
    """

    # user configurable state
    name = altar.properties.str(default="sample")
    name.doc = "the name of the job; used as a stem for making filenames, etc."

    mode = altar.properties.str()
    mode = "the programming model"

    hosts = altar.properties.int(default=1)
    hosts.doc = "the number of hosts to run on"

    tasks = altar.properties.int(default=1)
    tasks.doc = "the number of tasks per host"

    gpus = altar.properties.int(default=0)
    gpus.doc = "the number of gpus per task"

    chains = altar.properties.int(default=1)
    chains.doc = "the number of chains per worker"

    steps = altar.properties.int(default=20)
    steps.doc = 'the length of each Markov chain'

    tolerance = altar.properties.float(default=1.0e-3)
    tolerance.doc = "convergence tolerance for β->1.0"


    # initialize
    @altar.export
    def initialize(self, application):
        """
        Initialize the job parameters with information from the application context
        """
        # validate the machine layout
        self.validateMachineLayout(application=application)
        # all done
        return self


    # implementation details
    def validateMachineLayout(self, application):
        """
        Adjust the machine parameters based on the {application} context and the runtime
        environment
        """
        # get the host info
        host = self.pyre_executive.host
        # and my shell
        shell = application.shell

        # set the programming model
        self.mode = shell.model

        # if the user specified more than one host, we had better be running with mpi
        if self.hosts > 1 and self.mode != 'mpi':
            # otherwise, grab a channel
            channel = application.error
            # complain
            channel.line(f"an MPI runtime is required to run on {self.hosts} hosts")
            channel.line(f" -- please launch using an MPI compatible shell")
            channel.line(f" -- e.g., use '--shell=mpi.mpirun' on the command line")
            channel.log()
            # and exit
            raise SystemExit(1)

        # let's figure out the GPU situation; get the number of GPUs per task the user asked for
        gpus = self.gpus
        # if the user doesn't want GPU support
        if gpus == 0:
            # we are done
            return self
        # otherwise, attempt to
        try:
            # get support for cuda
            import cuda
        # if this fails
        except ImportError:
            # pick a channel
            channel = application.warning
            # complain
            channel.line(f"no runtime support for CUDA on '{host.hostname}'")
            channel.log(f" -- setting the number of GPUs per task to 0")
            # no GPUs
            self.gpus = 0
        # if it succeeds
        else:
            # get the number of tasks per host
            tasks = self.tasks
            # compute the requested number of devices
            requested = tasks * gpus
            # get the total GPU count on this node
            available = cuda.manager.count
            # if the user asked for more than we have
            if requested > available:
                # be civilized
                avlLabel = "GPU" if available == 1 else "GPUs"
                reqLabel = "GPU" if requested == 1 else "GPUs"
                gpuLabel = "GPU" if gpus == 1 else "GPUs"
                taskLabel = "task" if tasks == 1 else "tasks"
                # pick the channel
                channel = application.error
                # complain
                channel.line(f"not enough GPUs on '{host.hostname}':")
                channel.line(f" -- available: {available} {avlLabel}")
                channel.line(
                    f" -- requested: {requested} {reqLabel}: "
                    f"{tasks} {taskLabel} x {gpus} {gpuLabel} per task")
                channel.log()
                # and exit
                raise SystemExit(1)

        # all done
        return self


# end of file

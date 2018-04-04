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

    tolerance = altar.properties.float(default=1.0e-3)
    tolerance.doc = "convergence tolerance for β->1.0"

    model = altar.models.model()
    model.doc = "the AlTar model to sample"


    # initialize
    def initialize(self, app):
        """
        Initialize the job parameters with information from the application context
        """
        # grab my shell
        shell = app.shell
        # set the programming model
        self.mode = shell.model
        # if it is mpi aware
        if shell.model == 'mpi':
            # transfer the host count
            self.hosts = shell.hosts
            # and the tasks per host
            self.tasks = shell.tasks

        # get the host info
        host = self.pyre_executive.host

        # the hosts and tasks settings are vetted by the shell; let's figure out the GPU
        # situation; get what the user asked for
        gpus = self.gpus
        # attempt to
        try:
            # get support for cuda
            import cuda
        # if this fails
        except ImportError:
            # if the user asked for GPUs
            if gpus:
                # pick a channel
                channel = app.warning
                # complain
                channel.line(f"no runtime support for CUDA on '{host.hostname}'")
                channel.log(f" -- setting the number of GPUs per task to 0")
            # no GPUs
            self.gpus = 0
        # if it succeeds
        else:
            # unpack the requested resources
            tasks = job.tasks
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
                channel = app.error
                # complain
                channel.line(f"not enough GPUs on '{host.hostname}':")
                channel.line(f" -- available: {available} {avlLabel}")
                channel.line(
                    f" -- requested: {requested} {reqLabel}: "
                    f"{tasks} {taskLabel} x {gpus} {gpuLabel} per task")
                channel.log()
                # and exit
                raise SystemExit(1)

        # if the user specified more than one host, we had better be running with mpi
        if self.hosts > 1 and self.mode != 'mpi':
            # otherwise, grab a channel
            channel = app.error
            # complain
            channel.line(f"an MPI runtime is required to run on {self.hosts} hosts")
            channel.line(f" -- please launch using an MPI compatible shell")
            channel.line(f" -- e.g., use '--shell=mpi.mpirun' on the command line")
            channel.log()
            # and exit
            raise SystemExit(1)

        # all done
        return self


# end of file

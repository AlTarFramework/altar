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
class Job(altar.component, family="altar.runs.job", implements=run):
    """
    The set of parameters in an AlTar run
    """

    # user configurable state
    name = altar.properties.str(default="sample")
    name.doc = "the name of the job; used as a stem for making filenames, etc."

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
        # if it is mpi aware
        if shell.model == 'mpi':
            # transfer the host count
            self.hosts = shell.hosts
            # and the tasks per host
            self.tasks = shell.tasks
        # all done
        return


# end of file

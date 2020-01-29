# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2020 parasim inc
# (c) 2010-2020 california institute of technology
# all rights reserved
#

# the package
import altar


# the run protocol
class Run(altar.protocol, family="altar.simulations.runs"):
    """
    Protocol that specifies the job parameter set
    """

    # user configurable state
    name = altar.properties.str()
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


    # required behavior
    @altar.provides
    def initialize(self, application):
        """
        Initialize the run components with context from {application}
        """


    # framework hooks
    @classmethod
    def pyre_default(cls, **kwds):
        """
        Supply a default implementation
        """
        # pull the run implementation
        from .Job import Job as default
        # and return it
        return default


# end of file

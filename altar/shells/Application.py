# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2019 parasim inc
# (c) 2010-2019 california institute of technology
# all rights reserved
#

# support
import altar


# the simple application shell
class Application(altar.application, family="altar.shells.application"):
    """
    The base class for simple AlTar applications
    """


    # user configurable state
    job = altar.simulations.run()
    job.doc = "the job input parameters"

    model = altar.models.model()
    model.doc = "the AlTar model to sample"

    rng = altar.simulations.rng()
    rng.doc = "the random number generator"

    controller = altar.bayesian.controller()
    controller.doc = "my simulation controller"

    monitors = altar.properties.dict(schema=altar.simulations.monitor())
    monitors.doc = "a collection of event handlers"


    # protocol obligations
    @altar.export
    def main(self, *args, **kwds):
        """
        The main entry point
        """
        # N.B.: the initialization phase must be respectful of the interdependencies of these
        # components; e.g., both {controller} and {model} expect an initialized {rng}

        # initialize the job parameters
        self.job.initialize(application=self)
        # the random number generator
        self.rng.initialize()
        # the controller
        self.controller.initialize(application=self)
        # and the model; attach whatever the model initialization returns, just in case the
        # model selects an implementation strategy based on my context
        self.model = self.model.initialize(application=self)
        # sample the posterior distribution
        return self.model.posterior(application=self)


    # pyre framework hooks
    # interactive session management
    def pyre_interactiveSessionContext(self, context):
        """
        Go interactive
        """
        # protect against bad context
        if context is None:
            # by initializing an empty one
            context = {}
        # add some symbols
        context["altar"] = altar # my package
        # and chain up
        return super().pyre_interactiveSessionContext(context=context)


    # machine layout adjustments for MPI runs
    def pyre_mpi(self):
        """
        Transfer my {job} settings to the MPI shell
        """
        # get my shell
        shell = self.shell
        # if the programming model is not {MPI}
        if shell.model != "mpi":
            # something really bad has happened
            self.firewall.log(f"the {pyre_mpi} hook with model={shell.model}")

        # get my job parameters
        job = self.job
        # transfer the job settings
        shell.hosts = job.hosts
        shell.tasks = job.tasks

        # all done
        return self


# end of file

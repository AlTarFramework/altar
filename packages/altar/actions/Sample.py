# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2018 parasim inc
# (c) 2010-2018 california institute of technology
# all rights reserved
#

# get the package
import altar


# declaration
class Sample(altar.panel(), family='altar.actions.sample'):
    """
    Sample the posterior distribution of a model
    """


    # user configurable state
    model = altar.properties.str()
    model.tip = "the name of a model to sample"


    # commands
    @altar.export(tip="sample the posterior distribution of a model")
    def default(self, plexus, **kwds):
        """
        Print the name of the app for configuration purposes
        """
        # make a channel
        channel = plexus.info

        # grab the programming model from the shell
        mode = plexus.shell.model
        # and the requested number of gpus per tasks
        gpus = plexus.gpus

        # show me
        channel.line()
        channel.line(f"mode: {mode}")

        if mode == "mpi":
            import mpi
            channel.line(f"requested tasks: {plexus.shell.tasks}")
            channel.line(f"actual tasks: {mpi.world.size}")

        channel.line(f"requested gpus per task: {gpus}")
        # attempt to
        try:
            # get support for cuda
            import cuda
        # if this fails
        except ImportError:
            # let me know
            channel.line(f"available gpus on this node: 0")
        # if it succeeds
        else:
            # show me
            channel.line(f"available gpus on this node: {cuda.manager.count}")

        # flush
        channel.log()

        # all done
        return


# end of file

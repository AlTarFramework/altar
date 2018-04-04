# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2018 parasim inc
# (c) 2010-2018 california institute of technology
# all rights reserved
#

# support
import altar


# the plexus
class AlTar(altar.plexus, family="altar.shells.altar", namespace="altar"):
    """
    The main action dispatcher for the simple AlTar application
    """

    # types
    from .Action import Action as pyre_action

    # user configurable state
    job = altar.simulations.run()
    job.doc = "the job input parameters"

    model = altar.models.model()
    model.doc = "the AlTar model to sample"


    # protocol obligations
    @altar.export
    def main(self, *args, **kwds):
        """
        The main entry point
        """
        # initialize the job parameters
        self.job.initialize(application=self)
        # and the model
        self.model.initialize(application=self)
        # chain up
        return super().main(*args, **kwds)


    # pyre framework hooks
    # support for the help system
    def pyre_banner(self):
        """
        Place the application banner in the {info} channel
        """
        # show the package header
        return altar.meta.header


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


# end of file

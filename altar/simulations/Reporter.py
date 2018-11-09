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
from .Monitor import Monitor as monitor


# an implementation of the monitor protocol
class Reporter(altar.component, family="altar.simulations.monitors.reporter", implements=monitor):
    """
    Reporter reports simulation progress by using application journal channels
    """


    # protocol obligations
    @altar.export
    def initialize(self, application):
        """
        Initialize me given an {application} context
        """
        # nothing to do
        return self


    # implementation details
    def start(self, controller, **kwds):
        """
        Handler invoked when the simulation is about to start
        """
        # grab a channel
        channel = controller.info
        # say something
        channel.log(f"{self.pyre_name}: start")
        # all done
        return


    def finish(self, controller, **kwds):
        """
        Handler invoked when the simulation is about to finish
        """
        # grab a channel
        channel = controller.info
        # say something
        channel.log(f"{self.pyre_name}: finish")
        # all done
        return


# end of file

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

# the monitor protocol
class Monitor(altar.protocol, family="altar.simulations.monitors"):
    """
    The protocol that all AlTar simulation monitors must implement

    Monitors respond to simulation events by generating user diagnostics to report progress
    """

    # protocol obligations
    @altar.provides
    def initialize(self, application):
        """
        Initialize me given an {application} context
        """


    # framework hooks
    @classmethod
    def pyre_default(cls, **kwds):
        """
        Supply a default implementation
        """
        # pull the default monitor
        from .Reporter import Reporter as default
        # and return it
        return default


# end of file

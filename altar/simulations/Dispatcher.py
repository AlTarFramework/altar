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

# the dispatcher
class Dispatcher(altar.protocol, family="altar.simulations.dispatchers"):
    """
    The protocol that all AlTar simulation dispatchers must implement

    Dispatchers associate event handlers with specific aspects of the calculation and invoke
    them when appropriate
    """

    # required behavior
    @altar.provides
    def initialize(self, application):
        """
        Initialize me given an {application} context
        """

# end of file

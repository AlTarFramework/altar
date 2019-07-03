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

# the archiver protocol
class Archiver(altar.protocol, family="altar.simulations.archivers"):
    """
    The protocol that all AlTar simulation archivers must implement

    Archivers persist intermediate simulation state and can be used to restart a simulation
    """

    # required behavior
    @altar.provides
    def initialize(self, application):
        """
        Initialize me given an {application} context
        """

    @altar.provides
    def record(self, step):
        """
        Record the final state of the simulation
        """

    # framework hooks
    @classmethod
    def pyre_default(cls, **kwds):
        """
        Supply a default implementation
        """
        # pull the in-memory archiver
        from .Recorder import Recorder as default
        # and return it
        return default

# end of file

# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2020 parasim inc
# (c) 2010-2020 california institute of technology
# all rights reserved
#

# get the package
import altar


# the controller protocol
class Controller(altar.protocol, family="altar.controllers"):
    """
    The protocol that all AlTar controllers must implement
    """


    # required user configurable state
    dispatcher = altar.simulations.dispatcher()
    dispatcher.doc = "the event dispatcher that activates the registered handlers"

    archiver = altar.simulations.archiver()
    archiver.doc = "the archiver of simulation state"


    # required behavior
    @altar.provides
    def posterior(self, model):
        """
        Sample the posterior distribution of the given {model}
        """


    @altar.provides
    def initialize(self, application):
        """
        Initialize me and my parts given an {application} context
        """


    # framework hooks
    @classmethod
    def pyre_default(cls, **kwds):
        """
        Supply a default implementation
        """
        # by default, we do CATMIP as encapsulated by the {Annealer} class
        from .Annealer import Annealer as default
        # and return it
        return default


# end of file

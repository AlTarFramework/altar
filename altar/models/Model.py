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


# the model protocol
class Model(altar.protocol, family="altar.models"):
    """
    The protocol that all AlTar models must implement
    """


    # required behavior
    @altar.provides
    def posterior(self, app):
        """
        Sample my posterior distribution
        """


    # framework hooks
    @classmethod
    def pyre_default(cls, **kwds):
        """
        Supply a default implementation
        """
        # pull the trivial model
        from .Null import Null as default
        # and return it
        return default


# end of file

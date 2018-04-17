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


# the protocol
class Norm(altar.protocol, family="altar.norms"):
    """
    The protocol that all AlTar norms must satify
    """


    # framework hooks
    @classmethod
    def pyre_default(cls, **kwds):
        """
        Provide a default norm in case the user hasn't selected one
        """
        # the default is {L2}
        from .L2 import L2 as default
        # make it accessible
        return default


# end of file

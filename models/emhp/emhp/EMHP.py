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


# declaration
class EMHP(altar.models.bayesian, family="altar.models.emhp"):
    """
    A diagnostic tool
    """


    # protocol obligations
    @altar.export
    def initialize(self, application):
        """
        Initialize the state of the model given a {problem} specification
        """
        # make a channel
        channel = application.info
        # sign on
        channel.log("initializing emhp")
        # and bail
        raise SystemExit(0)


# end of file

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
        # all done
        return


# end of file

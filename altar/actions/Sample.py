# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2019 parasim inc
# (c) 2010-2019 california institute of technology
# all rights reserved
#

# get the package
import altar


# declaration
class Sample(altar.panel(), family='altar.actions.sample'):
    """
    Sample the posterior distribution of a model
    """


    # commands
    @altar.export(tip="sample the posterior distribution of a model")
    def default(self, plexus, **kwds):
        """
        Sample the model posterior distribution
        """
        # get the model
        model = plexus.model
        # sample its posterior distribution
        return model.posterior(application=plexus)


# end of file

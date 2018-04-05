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
class Gaussian(altar.models.bayesian, family="altar.models.gaussian"):
    """
    A simple multi-parameter Gaussian model that serves as an example
    """


    # user configurable state
    dof = altar.properties.int(default=2)
    dof.doc = "the number of variables"


    @altar.export
    def parameters(self):
        """
        The number of parameters in this model
        """
        # return the number of degrees of freedom
        return self.dof

# end of file

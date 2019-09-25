# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# Lijun Zhu
#
# (c) 2013-2019 parasim inc
# (c) 2010-2019 california institute of technology
# all rights reserved
#


# get the package
import altar


# the scheduler protocol
class Solver(altar.protocol, family="altar.bayesian.solvers"):
    """
    The protocol that all δβ solvers must implement
    """


    # user configurable state
    tolerance = altar.properties.float()
    tolerance.doc = 'the fractional tolerance for achieving convergence'


    # required behavior
    @altar.provides
    def initialize(self, application, scheduler):
        """
        Initialize me and my parts given an {application} context and a {scheduler}
        """


    @altar.provides
    def solve(self, llk, weight):
        """
        Compute the next temperature in the cooling schedule
        """


    # framework hooks
    @classmethod
    def pyre_default(cls, **kwds):
        """
        Provide a default implementation
        """
        # by default, use the naive grid solver
        from .Grid import Grid
        # and return it
        return Grid


# end of file

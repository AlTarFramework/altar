# -*- python -*-
# -*- coding: utf-8 -*-
#
#
# (c) 2013-2019 parasim inc
# (c) 2010-2019 california institute of technology
# all rights reserved
#
# Author(s): Lijun Zhu

# get the package
import altar

# the scheduler protocol
class DbetaSolver(altar.protocol, family="altar.dbetasolver"):
    """
    The protocol that all AlTar δβ solver must implement
    """

    # required behavior
    @altar.provides
    def solve(self, minimizer, llk, weight):
        """
        Solve δβ
        """

    # framework hooks
    @classmethod
    def pyre_default(cls, **kwds):
        """
        Supply a default implementation
        """
        # by default, use grid δβ solver
        from .GridDbetaSolver import GridDbetaSolver as default
        # and return it
        return default

# end of file

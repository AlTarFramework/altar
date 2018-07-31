# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2018 parasim inc
# (c) 2010-2018 california institute of technology
# all rights reserved
#


# framework
import altar


# declaration
class Data(altar.tabular.sheet):
    """
    The layout of the input data file
    """

    # the layout
    oid = altar.tabular.int()
    d = altar.tabular.float()
    x = altar.tabular.float()
    y = altar.tabular.float()
    theta = altar.tabular.float()
    phi = altar.tabular.float()


# end of file

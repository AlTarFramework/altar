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
# my protocol
from .Monitor import Monitor as monitor


# an implementation of the monitor protocol
class Reporter(altar.protocol, family="altar.monitors.reporter", implements=monitor):
    """
    Reporter reports simulation progress by using application journal channels
    """


# end of file

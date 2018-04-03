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
from .Archiver import Archiver as archiver


# an implementation of the archiver protocol
class Recorder(altar.component, family="altar.archivers.recorder", implements=archiver):
    """
    Recorder stores the intermediate simulation state in memory
    """


# end of file

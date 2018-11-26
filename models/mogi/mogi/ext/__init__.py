# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2018 parasim inc
# (c) 2010-2018 california institute of technology
# all rights reserved
#


# attempt
try:
    # to load the extension module
    from . import mogi as libmogi
# if it fails
except ImportError:
    # the build/install must have failed somehow; we still have pure python support, so move on
    pass


# end of file

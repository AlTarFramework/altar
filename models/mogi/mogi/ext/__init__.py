# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2019 parasim inc
# (c) 2010-2019 california institute of technology
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


# attempt
try:
    # to load the extension with the CUDA support
    from . import cudamogi as libcudamogi
# if it fails
except ImportError:
    # no worries
    pass


# end of file

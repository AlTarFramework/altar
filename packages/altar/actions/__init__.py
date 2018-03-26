# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2010-2018 california institute of technology
# (c) 2013-2018 parasim inc
# all rights reserved
#

# get the package
import altar

# administrivia
@altar.foundry(implements=altar.action, tip="display information about this appkication")
def about():
    # get the command panel
    from .About import About
    # attach the docstring
    __doc__ = About.__doc__
    # and  return the panel
    return About

# end of file

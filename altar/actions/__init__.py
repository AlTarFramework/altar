# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2020 parasim inc
# (c) 2010-2020 california institute of technology
# all rights reserved
#

# get the package
import altar

# administrivia
@altar.foundry(implements=altar.action, tip="display information about this application")
def about():
    # get the command panel
    from .About import About
    # attach the docstring
    __doc__ = About.__doc__
    # and  return the panel
    return About


# sample the posterior distribution of a model
@altar.foundry(implements=altar.action, tip="sample the posterior distribution of a model")
def sample():
    # get the command panel
    from .Sample import Sample
    # attach the docstring
    __doc__ = Sample.__doc__
    # and  return the panel
    return Sample

# end of file

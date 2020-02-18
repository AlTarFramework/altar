# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis (michael.aivazis@para-sim.com)
# grace bato           (mary.grace.p.bato@jpl.nasa.gov)
# eric m. gurrola      (eric.m.gurrola@jpl.nasa.gov)
#
# (c) 2013-2020 parasim inc
# (c) 2010-2020 california institute of technology
# all rights reserved



# the framework
import altar


# the model foundry
@altar.foundry(implements=altar.models.model, tip="a multi-parameter reverso model")
def reverso():
    """
    An implementation of the Reverso 2-Magma Chamber Volcano Model, Reverso et al. [2014]
    """
    # grab the factory
    from .Reverso import Reverso as reverso
    # and return it
    return reverso


# end of file

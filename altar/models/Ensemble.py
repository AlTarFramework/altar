# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2018 parasim inc
# (c) 2010-2018 california institute of technology
# all rights reserved
#


# my superclass
from .Bayesian import Bayesian


# declaration
class Ensemble(Bayesian, family="altar.models.ensemble"):
    """
    A collection of AlTar models that comprise a single model
    """

    # my collection
    models = altar.properties.list(schema=model())
    models.doc = "the collection of models in this ensemble"


# end of file

# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2018 parasim inc
# (c) 2010-2018 california institute of technology
# all rights reserved
#

# N.B. there is no python version check here; the assumption is that the altar requirements are
# in sync with the pyre requirements, so the python version check that happens on importing
# pyre is sufficient; the only problem is that the error message complains about pyre, not
# altar; is this worth fixing?

# externals
import os

# pull the framework parts
from pyre import (
    # protocols, components and traits
    schemata, protocol, component, foundry, properties, constraints,
    # decorators
    export, provides,
    # the runtime manager
    executive,
    # support for accessing virtual and local filesystems
    filesystem,
    # miscellaneous packages
    patterns, primitives, records, tabular, timers, tracking, units,
    # support for asynchrony
    nexus,
    # plexus support
    action, command, panel, plexus, application
    )

# grab the journal
import journal

# numerics
from gsl import (
    # matrices
    matrix,
    # vectors
    vector,
    # basic linear algebra
    blas,
    # higher level linear algebra
    linalg as lapack,
    # random number generators
    rng,
    # probability distribution functions
    pdf,
    # histograms
    histogram,
)

# fire up
package = executive.registerPackage(name='altar', file=__file__)
# save the geography
home, prefix, etc = package.layout()
# the directory with my models
modelPrefix = os.path.join(home, "models")

# export my parts
from . import (
    # package meta-data
    meta,
    # simulation support
    simulations,
    # norms
    norms,
    # probability distribution functions
    distributions,
    # support for Bayesian explorations using Markov chain Monte Carlo
    bayesian,
    # models
    models,
    # user interfaces
    shells, actions,
    )

# my extension modules
from .ext import libaltar

# administrative
def copyright():
    """
    Return the altar copyright note
    """
    return print(meta.header)


def license():
    """
    Print the altar license
    """
    # print it
    return print(meta.license)


def version():
    """
    Return the altar version
    """
    return meta.version


def credits():
    """
    Print the acknowledgments
    """
    # print it
    return print(meta.acknowledgments)


# end of file

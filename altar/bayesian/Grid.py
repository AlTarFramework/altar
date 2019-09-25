# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# Lijun Zhu
#
# (c) 2013-2019 parasim inc
# (c) 2010-2019 california institute of technology
# all rights reserved
#

# get the package
import altar
# my protocol
from .Solver import Solver as solver


# declaration
class Grid(altar.component, family="altar.bayesian.solvers.grid", implements=solver):
    """
    A δβ solver based on a naive grid search
    """


    # user configurable state
    tolerance = altar.properties.float(default=.01)
    tolerance.doc = 'the fractional tolerance for achieving convergence'

    maxiter = altar.properties.int(default=10**3)
    maxiter.doc = 'the maximum number of iterations while looking for a δβ'


    # protocol obligations
    @altar.provides
    def initialize(self, application, scheduler):
        """
        Initialize me and my parts given an {application} context and a {scheduler}
        """
        # get the simulation RNG
        rng = application.rng.rng
        # instantiate my COV calculator
        self.cov = altar.libaltar.cov(rng.rng, self.maxiter, self.tolerance, scheduler.target)
        # all done
        return self


    @altar.export
    def solve(self, llk, weight):
        """
        Compute the next temperature in the cooling schedule
        :param llk: data log-likelihood
        :param weight: the normalized weight
        :return: β, cov
        """
        # compute the median data log-likelihood; clone the source vector first, since the
        # sorting happens in place
        median = llk.clone().sort().median()
        # call grid dbeta_solver, return β, cov
        return altar.libaltar.dbeta_grid(self.cov, llk.data, median, weight.data)


    # private data
    cov = None # the COV calculator


# end of file

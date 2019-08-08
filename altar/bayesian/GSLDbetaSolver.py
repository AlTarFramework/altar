# -*- python -*-
# -*- coding: utf-8 -*-
#
#
# (c) 2013-2019 parasim inc
# (c) 2010-2019 california institute of technology
# all rights reserved
#
# Author(s): Lijun Zhu

# get the package
import altar
# my protocol
from .DbetaSolver import DbetaSolver as dbetasolver

# declaration
class GSLDbetaSolver(altar.component, family="altar.dbetasolver.gsldbetasolver", implements=dbetasolver):
    """
    The δβ Solver based on GSL minimizer
    """

    # required behavior
    @altar.provides
    def solve(self, minimizer, llk, weight):
        """
        Solve δβ
        :param minimizer: the calculator for quantity to be minimized
        :param llk: data log-likelihood
        :param weight: the normalized weight, vector (samples)
        :return: β, cov
        """
        # compute the median data log-likelihood; clone the source vector first, since the
        # sorting happens in place
        median = llk.clone().sort().median()
        # call gsl dbeta_solver, return β, cov
        return altar.libaltar.dbeta_gsl(minimizer, llk.data, median, weight.data)

# end of file

# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2020 parasim inc
# (c) 2010-2020 california institute of technology
# all rights reserved
#

# the package
import altar
# my protocol
from .Norm import Norm


# declaration
class L2(altar.component, family="altar.norms.l2", implements=Norm):
    """
    The L2 norm
    """


    # interface
    @altar.export
    def eval(self, v, sigma_inv=None):
        """
        Compute the L2 norm of the given vector, with or without a covariance matrix
        """
        # if we have a covariance matrix
        if sigma_inv is not None:
            # use the specialized implementation
            return self.withCovariance(v=v, sigma_inv=sigma_inv)
        # otherwise, compute the norm and return it
        return altar.blas.dnrm2(v)


    # implementation details
    def withCovariance(self, v, sigma_inv):
        """
        Compute the L2 norm of the given vector using the given Cholesky decomposed inverse
        covariance matrix
        """
        # we assume {sigma_inv} is Cholesky decomposed, so we can pre-multiply the vector by
        # the lower triangle, and then just take the norm

        # use the lower triangle, no transpose, non-unit diagonal
        v = altar.blas.dtrmv(
            sigma_inv.lowerTriangular, sigma_inv.opNoTrans, sigma_inv.nonUnitDiagonal,
            sigma_inv, v)
        # compute the dot product and return it
        return altar.blas.dnrm2(v)


# end of file

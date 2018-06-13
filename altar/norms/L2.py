# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2018 parasim inc
# (c) 2010-2018 california institute of technology
# all rights reserved
#

# the package
import altar
# my protocol
from .Norm import Norm


# declaration
class L2(altar.component, familt="altar.norms.l2", implements=Norm):
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
        Compute the L2 norm of the given vector with a given covariance matrix
        """
        # make a copy of the input vector
        vT = v.clone()
        # pre-multiply {v} by Cd^{-1}: use the upper triangle, no transpose, non-unit diagonal
        v = altar.blas.dtrmv(
            sigma_inv.upperTriangular, sigma_inv.opNoTrans, sigma_inv.nonUnitDiagonal,
            sigma_inv, v)
        # compute the dot product and return it
        return altar.blas.ddot(vT, v)


# end of file

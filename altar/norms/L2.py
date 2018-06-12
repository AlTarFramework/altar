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
    def eval(self, vectors, c_inv=None):
        """
        Compute the L2 norm of the given vectors
        """
        # allocate a vector for the result
        norm = altar.vector(shape=vectors.columns)
        # each column in {vectors} corresponds to a vector whose norm we are to compute
        for column in range(vectors.columns):
            # extract the vector
            v = vectors.getColumn(column)
            # and make a copy
            vT = v.clone()
            # pre-multiply by Cd^{-1}: use the upper triangle, no transpose, non-unit diagonal
            v = altar.blas.dtrmv(
                c_inv.upperTriangular, c_inv.opNoTrans, c_inv.nonUnitDiagonal,
                c_inv, v)
            # compute the dot product
            norm[column] = altar.blas.ddot(vT, v)
        # all done
        return norm



# end of file

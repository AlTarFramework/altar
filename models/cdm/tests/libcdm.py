#!/usr/bin/env python3

# -*- python -*-
# -*- coding: utf-8 -*-
#
# eric m. gurrola <eric.m.gurrola@jpl.nasa.gov>
#
# (c) 2018-2019 jet propulsion laboratory
# (c) 2018-2019 california institute of technology
# (c) 2018-2019 parasim
# all rights reserved
#

"""
Test for CDM: Compound Dislocation Model
"""

import sys
import numpy
from altar.models.cdm.libcdm import CDM

# Matlab test coordinates and displacements in EFCS (East, North, Vertical).
# Sampled from computed output from original Matlab code.
# inputs

# matlab input X coordinates sample
X = numpy.array([-7,    -6.90, -6.88, -6.86,
                 -6.84, -6.82,  0,     0.50,
                  1.10,  6.50,  6.86,  7])
# matlab input Y coordinates sample
Y = numpy.array([-5,    -5,    -5,    -5,
                 -5,    -5,    -4.92, -4.92,
                 -4.92, -4.92,  4.94, 5])

# matlab de corresponding outputs
mde = numpy.array([-4.831270e-06, -4.886526e-06, -4.897588e-06, -4.908654e-06,
                  -4.919721e-06, -4.930791e-06, -1.331881e-06,  9.160793e-08,
                   1.801943e-06,  5.766744e-06,  4.544161e-06,  4.439410e-06])
# matlab dn corresponding outputs
mdn = numpy.array([-2.988161e-06, -3.064582e-06, -3.080126e-06, -3.095757e-06,
                  -3.111477e-06, -3.127285e-06, -1.312579e-05, -1.331642e-05,
                  -1.315063e-05, -4.467011e-06,  3.648027e-06,  3.525858e-06])
# matlab dv corresponding outputs
mdv = numpy.array([ 1.799845e-06,  1.844885e-06,  1.854042e-06,  1.863249e-06,
                    1.872507e-06,  1.881815e-06,  7.624726e-06,  7.706569e-06,
                    7.578237e-06,  2.489978e-06,  1.996341e-06,  1.909694e-06])

def main(X, Y, X0, Y0, depth, omegaX, omegaY, omegaZ, ax, ay, az, opening, nu, verbose=False):
    """
    Test CDM with test input parameters
    X0, Y0, depth: define the position of the dislocation
    omegaX, omegaY, omegaZ: define the orientation (clockwise rotations) of the dislocation
    ax, ay, az: define the semi-axes  of the dislocation in the "body fixed" coordinates
    length of the tensile component of the Burgers Vector (length of the dislocation)
    """

    if verbose:
        print("X = ", X)
        print("Y = ", Y)
        print("X0, Y0, depth = ", X0, Y0, depth)
        print("omegaX, omegaY, omegaZ = ", omegaX, omegaY, omegaZ)
        print("ax, ay, az = ", ax, ay, az)
        print("opening = ", opening)
        print("nu = ", nu)

    # Call CDM with test parameters; return displacements (de, dn, dv) and error status for
    de, dn, dv, ierr = CDM(X, Y, X0, Y0, depth, omegaX, omegaY, omegaZ, ax, ay, az, opening, nu)

    # compare output against the matlab generated output
    # open the matlab generated file
    if verbose:
        print("Differences from reference")
        print(" X      Y     de            dn            dv")

    for idx in range(len(X)):
        m = [mde[idx], mdn[idx], mdv[idx]]
        if verbose:
            print("{0: 5.2f}  {1: 5.2f}  {2:12.6e}  {3:12.6e}  {4:12.6e}".format(
                X[idx], Y[idx], abs((m[0]-de[idx])/m[0]), abs((m[1]-dn[idx])/m[1]),
                abs((m[2]-dv[idx])/m[2])
            ))

        if( (abs((m[0] - de[idx])/m[0]) > 1.e-6) or
            (abs((m[1] - dn[idx])/m[1]) > 1.e-6) or
            (abs((m[2] - dv[idx])/m[2]) > 1.e-6)
          ):
            # if there are any differences print them otherwise be silent
            print(idx, X[idx], Y[idx], m[0]-de[idx], m[1]-dn[idx], m[2]-dv[idx])
            break

    return 0

if __name__ == "__main__":

    verbose = False
    if len(sys.argv) > 1:
        verbose = True

    # Set test parameter values

    # Horizontal coordinates (in EFCS) and depth of the point CDM. The depth must be a positive
    # value. X0, Y0, and depth have the same units as X, Y, Z.
    X0, Y0, depth = 0.5, -0.25, 2.75

    # Rotation angles (clockwise) in degrees defining the orientation of the point CDM.
    omegaX, omegaY, omegaZ = 5., -8., 30.

    # Semi-axes of the CDM along the X, Y, Z axes before applying the rotation
    #  (ax, ay, az have the same units as X and Y.)
    ax, ay, az = 0.4, 0.45, 0.8

    # opening: the tensile component of the Burgers vector of the rectangular dislocation that
    # form the CDM. The unit of opening must be the same as the unit of ax, ay, az
    opening = 0.001

    # Poisson's ratio
    nu = 0.25

    # run the test
    status = main(X, Y, X0, Y0, depth, omegaX, omegaY, omegaZ, ax, ay, az, opening, nu,
                  verbose=verbose)

    # communicate status
    raise SystemExit(status)

# end-of-file

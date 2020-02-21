# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis (michael.aivazis@para-sim.com)
# grace bato           (mary.grace.p.bato@jpl.nasa.gov)
# eric m. gurrola      (eric.m.gurrola@jpl.nasa.gov)
#
# (c) 2013-2020 parasim inc
# (c) 2010-2020 california institute of technology
# all rights reserved


# externals
import math


# the calculator
def REVERSO(locations,
            H_s, H_d, a_s, a_d, a_c,
            Qin,
            G, v, mu, drho, g):
    """
    Calculate the surface displacements for a Reverso model at observation {locations}

    The parameter {locations} is an array of (t, x, y) triplets

    model parameters:
        a_c: the radius of the hydraulic pipe
        a_s: the radius of the shallow reservoir
        a_d: the radius of the deep reservoir
        H_s: the depth of the shallow reservoir
        H_d: the depth of the deep reservoir
    """

    # constants
    pi = math.pi
    # functions
    exp = math.exp

    # initial conditions
    # shallow reservoir overpressure [Pa]
    dPs0 = 0.0
    # deep reservoir overpressure [Pa]
    dPd0 = 0.0

    # ratio of reservoir volumes
    k = (a_d/a_s)**3
    # length of the hydraulic connection
    H_c = H_d - H_s
    gamma_s = 8.0 * (1-v) / (3.0 * pi)
    gamma_d = 8.0 * (1-v) / (3.0 * pi)

    gamma_r = gamma_s + gamma_d*k

    # the analytic solution
    # the characteristic time constant (eq. 10)
    tau = (8.0 * mu * H_c**gamma_s * gamma_d * k * a_s**3) / (G * a_c**4 * gamma_r)

    A  = gamma_d*k / gamma_r
    A *= dPd0 - dPs0 + drho*g*H_c - 8*gamma_s*mu*Qin*H_c / (pi * a_c**4 * gamma_r)

    # generate the displacements
    for t,x,y in locations:
        # compute the pressures
        f0 = A * (1 - exp(-t/tau))
        f1 = G * Qin * t / (pi * a_s**3 * gamma_r)

        dP_s = dPs0 + f1 + f0
        dP_d = dPd0 + f1 - f0 * gamma_s/(gamma_d*k)

        # compute the square of the distance to the reservoirs
        r2 = x**2 + y**2
        # get the H
        H_r, H_z = H(r2=r2,
                     H_s=H_s, H_d=H_d, a_s=a_s, a_d=a_d, gamma_s=gamma_s, gamma_d=gamma_d,
                     G=G, v=v)
        # compute the displacement in the radial direction
        u_r = H_r[0] * dP_s + H_r[1] * dP_d
        # compute the displacement in the vertical direction
        u_z = H_z[0] * dP_s + H_z[1] * dP_d

        # make them available
        yield u_r, u_z

    # all done
    return


# helpers
def H(r2, H_s, H_d, a_s, a_d, gamma_s, gamma_d, G, v):
    """
    """
    pi = math.pi
    sqrt = math.sqrt

    r = sqrt(r2)

    H2_s = H_s**2
    H2_d = H_d**2

    R2_s = r2 + H2_s
    R2_d = r2 + H2_d

    alpha_s = 1.0 if gamma_s == 1.0 else 4 * H2_s / (pi*R2_s)
    alpha_d = 1.0 if gamma_d == 1.0 else 4 * H2_d / (pi*R2_d)

    f_s = a_s**3 * alpha_s * (1-v) / (G * (H2_s+r2)**1.5)
    f_d = a_d**3 * alpha_d * (1-v) / (G * (H2_d+r2)**1.5)

    H = [
        [ r*f_s, r*f_d ],     # the radial H
        [ H_s*f_s, H_d*f_d ]  # the vertical H
        ]

    return H


# end of file

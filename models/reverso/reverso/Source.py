# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis (michael.aivazis@para-sim.com)
# grace bato           (mary.grace.p.bato@jpl.nasa.gov)
# eric m. gurrola      (eric.m.gurrola@jpl.nasa.gov)
#
# (c) 2013-2020 parasim inc
# (c) 2010-2020 california institute of technology
# all rights reserved


# library
from .libreverso import REVERSO


# the source
class Source:
    """
    The source response for a Reverso model
    """


    # public data
    # radius of the shallow magma reservoir
    a_s = 0
    # radius of the deep magma reservoir
    a_d = 0
    # radius of the hydraulic pipe connecting two magma reservoirs
    a_c = 0
    # depth of the shallow reservoir
    H_s = 0
    # depth of the deep reservoir
    H_d = 0

    # physical parameters
    # shear modulus, [Pa, kg-m/s**2]
    G = 20.0E9
    # Poisson's ratio
    v = 0.25
    # viscosity [Pa-s]
    mu = 2000.0
    # density difference (ρ_r-ρ_m), [kg/m**3]
    drho = 300.0
    # gravitational acceleration [m/s**2]
    g = 9.81

    # basal magma inflow rate
    Qin = 0.6


    # interface
    def displacements(self, locations):
        """
        Compute the expected displacements at a set of observation locations and times
        """
        # compute the displacements
        yield from REVERSO(locations=locations,
                           H_s=self.H_s, H_d=self.H_d, a_s=self.a_s, a_d=self.a_d, a_c=self.a_c,
                           Qin=self.Qin,
                           G=self.G, v=self.v, mu=self.mu, drho=self.drho, g=self.g)
        # all done
        return


    # meta-methods
    def __init__(self,
                 H_s=H_s, H_d=H_d, a_s=a_s, a_d=a_d, a_c=a_c,
                 Qin=Qin,
                 G=G, v=v, mu=mu, drho=drho, g=g,
                 **kwds):
        # chain up
        super().__init__(**kwds)

        # store the radii
        self.a_c = a_c
        self.a_s = a_s
        self.a_d = a_d
        # store the chamber locations
        self.H_s = H_s
        self.H_d = H_d

        # store the rest of the parameters
        self.Qin = Qin
        self.G = G
        self.v = v
        self.mu = mu
        self.drho = drho
        self.g = g

        # all done
        return


# end of file

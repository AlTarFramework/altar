# -*- python -*-
# -*- coding: utf-8 -*-
#
# eric m. gurrola
#
# (c) 2018 california institute of technology
# all rights reserved
#
#


# framework
import altar
# externals
import numpy
from math import sqrt, pi as π
# library
from .libreverso import Reverso


# declaration
class Source:
    """
    The source response for a Reverso (Connected Two Magma Chambers Volcano) Model.
    """


    # public data
    # location
    x = 0
    y = 0
    # radius of the shallow magma reservoir
    a_s = 0
    # radius of the hydraulic pipe connecting two magma reservoirs
    a_c = 0
    # radius of the deep magma reservoir
    a_d = 0
    # depth of the shallow reservoir
    h_s = 0
    # depth of the deep reservoir
    h_d = 0
    # basal magma inflow rate from below the deep chamber
    qin = 0

    # material properties
    g  = 9.8 # acceleration due to gravity at sea level (m/sec**2)
    nu = .25 # Poisson ratio (dimensionless)
#    mu =

    # interface
    def displacements(self, locations, los):
        """
        Compute the expected displacements at a set of observation locations from a
        two magma chamber (reverso) volcano model
        """
        # the radius of the shallow reservoir
        a_s_src = self.a_s
        # the radius of the deep reservoir
        a_d_src = self.a_d
        # the radius of the connecting pipe between the two reservoirs
        a_c_src = self.a_c
        # depth of the shallow reservoir
        h_s_src = self.h_s
        # depth of the deep reservoir
        h_d_src = self.h_d
        # the basal magma inflow rate from below the deep reservoir (assumed contant)
        q_in_src  = self.q_in
        # the initial overpressure of the shallow source
        dPs0_src = self.dPs0
        # the initial overpressure of the deep source
        dPd0_src = self.dPd0
        # get the physical/material properties
        # local acceleration due to gravity (m/s**2)
        g = self.g
        # the rigidity (or shear) modulus (kg/m/s**2)
        Gsm = self.Gsm
        # Poisson's ratio (dimensionless)
        nu = self.nu
        # the magma viscosity (kg/m/s**2)
        mu = self.mu
        # the difference in rock density and magma-density (kg/m**3)
        drho = self.drho
        # the shape of the magma chambers ('sill' or 'sphere')
        shape = self.shape

        # from locations, a vector of (x,y) tuples, create the flattened vectors Xf, Yf
        # required by the Reverso model. (The Zf=0 plane is assumed to be the
        Xf = numpy.zeros(len(locations), dtype=float)
        Yf = numpy.zeros(len(locations), dtype=float)
        for i, loc in enumerate(locations):
            Xf[i] = loc[0]
            Yf[i] = loc[1]

        # allocate space for the result
        u = altar.vector(shape=len(locations))
        # compute the displacements
        ue, un, uv =  Reverso(X=Xf, Y=Yf, X0=x_src, Y0=y_src, H_s=h_s_src, H_d=h_d_src,
                          a_s=a_s_src, a_d=a_d_src, a_c=a_c_src, q_c=q_in_src,
                          dPs0=dPs0_src, dPd0=dPd0_src,
                          g=g, Gsm=Gsm, nu=nu, mu=mu, drho=drho, shape=shape)
        # go through each observation location
        for idx, (ux,uy,uz) in enumerate(zip(ue, un, uv)):
            # project the expected displacement along LOS and store
            u[idx] = ux * los[idx,0] + uy * los[idx,1] + uz * los[idx,2]

        # all done
        return u


    # meta-methods
    def __init__(self, x=x, y=y, d=d,
                 ax=ax, ay=ay, az=az, omegaX=omegaX, omegaY=omegaY, omegaZ=omegaZ,
                 opening=opening, v=v, **kwds):
        # chain up
        super().__init__(**kwds)
        # store the location
        self.x = x
        self.y = y
        self.d = d
        # the semi-axes
        self.ax = ax
        self.ay = ay
        self.az = az
        # the rotation angles
        self.omegaX = omegaX
        self.omegaY = omegaY
        self.omegaZ = omegaZ
        # the opening
        self.opening = opening
        # and the Poisson ratio
        self.v = v
        # the strength
        self.dV =  4*(ax*ay + ax*az + ay*az) * opening
        # all done
        return

        ue, un, uv =  Reverso(X=Xf, Y=Yf, X0=x_src, Y0=y_src, H_s=h_s_src, H_d=h_d_src,
                          a_s=a_s_src, a_d=a_d_src, a_c=a_c_src, q_in=q_in_src,
                          dPs0=dPs0_src, dPd0=dPd0_src,
                          g=g, Gsm=Gsm, nu=nu, mu=mu, drho=drho, shape=shape)

# end of file

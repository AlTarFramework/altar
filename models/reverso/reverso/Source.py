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
    # radius of the hydraulic pipe connecting two magma reservoirs
    ac = 0
    # radius of the shallow magma reservoir
    as = 0
    # radius of the deep magma reservoir
    ad = 0
    # depth of the shallow reservoir
    hs = 0
    # depth of the deep reservoir
    hd = 0
    # basal magma inflow rate from below the deep chamber
    q = 0

    # material properties
    v = .25 # Poisson ratio


    # interface
    def displacements(self, locations, los):
        """
        Compute the expected displacements at a set of observation locations from a
        two magma chamber (reverso) volcano model
        """
        # the radius of the shallow reservoir
        as_src = self.as
        # the radius of the deep reservoir
        ad_src = self.ad
        # the radius of the connecting pipe between the two reservoirs
        ac_src = self.ac
        # depth of the shallow reservoir
        hs_src = self.hs
        # depth of the deep reservoir
        hd_src = self.hd
        # the basal magma inflow rate
        q_src  = self.q

        # get the material properties
        v = self.v

        # from locations, a vector of (x,y) tuples, create the flattened vectors Xf, Yf required by
        # CDM
        Xf = numpy.zeros(len(locations), dtype=float)
        Yf = numpy.zeros(len(locations), dtype=float)
        for i, loc in enumerate(locations):
            Xf[i] = loc[0]
            Yf[i] = loc[1]

        # allocate space for the result
        u = altar.vector(shape=len(locations))
        # compute the displacements
        ue, un, uv =  Reverso(X=Xf, Y=Yf, X0=x_src, Y0=y_src, depth=d_src,
                          ax=ax_src, ay=ay_src, az=az_src,
                          omegaX=omegaX_src, omegaY=omegaY_src, omegaZ=omegaZ_src,
                          opening=opening, nu=v)
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


# end of file

# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2018 parasim inc
# (c) 2010-2018 california institute of technology
# all rights reserved
#


# framework
import altar
# externals
import numpy
from math import sqrt, pi as π
# library
from .libcdm import CDM


# declaration
class Source:
    """
    The source response for a Compound Dislocation Model in an elastic half space.
    """


    # public data
    # location
    x = 0
    y = 0
    d = 0
    # semi-axes of the CDM along the X, Y, and Z axes (before applying the rotation)
    ax = 0
    ay = 0
    az = 0
    # clockwise rotation angles about X, Y, Z axes that define the orientation of the CDM
    omegaX = 0
    omegaY = 0
    omegaZ = 0
    # opening (tensile component of the Burgers vector) of the rectangular dislocation
    opening = 0
    # material properties
    v = .25 # Poisson ratio


    # interface
    def displacements(self, locations, los):
        """
        Compute the expected displacements at a set of observation locations from a compound
        (triaxial) dislocation source at depth.
        """
        # the location of the source
        x_src = self.x
        y_src = self.y
        d_src = self.d
        # clockwise rotation angles about x, y, z axes
        omegaX_src = self.omegaX
        omegaY_src = self.omegaY
        omegaZ_src = self.omegaZ
        # semi-lengths
        ax_src = self.ax
        ay_src = self.ay
        az_src = self.az
        # opening
        opening = self.opening
        # get the material properties
        v = self.v

        # from locations, a vector of (x,y) tuples, create the flattened vectors Xf, Yf required by
        # CDM
        Xf = numpy.zeros(len(locations), dtype=float)
        Yf = numpy.zeros(len(locations), dtype=float)
        for i, p in enumerate(locations):
            Xf[i] = p[0]
            Yf[i] = p[1]

        # allocate space for the result
        u = altar.vector(shape=len(locations))
        # go through each observation location
        for index, (x_obs,y_obs) in enumerate(locations):
            # compute the displacements
            ue, un, uv =  CDM(Xf, Yf, x_src, y_src, d_src,
                              omegaX_src, omegaY_src, omegaZ_src,
                              ax_src, ay_src, az_src, opening, v)

            # project the expected displacement along LOS and store
            print("ue,un,uv are not scalars")
            u[index] = ue * los[index,0] + un * los[index,1] + uv * los[index,2]

        # all done
        return u


    # meta-methods
    def __init__(self, x=x, y=y, d=d, omegaX=omegaX, omegaY=omegaY, omegaZ=omegaZ,
                 ax=ax, ay=ay, az=az, opening=opening, v=v, **kwds):
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

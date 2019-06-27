# -*- python -*-
# -*- coding: utf-8 -*-
#
# eric m. gurrola <eric.m.gurrola@jpl.nasa.gov>
#
# (c) 2018-2019 jet propulsion laboratory
# (c) 2018-2019 california institute of technology
# all rights reserved
#
# United States Government Sponsorship acknowledged. Any commercial use must be negotiated with
# the Office of Technology Transfer at the California Institute of Technology.
#
# This software may be subject to U.S. export control laws. By accepting this software, the user
# agrees to comply with all applicable U.S. export laws and regulations. User has the
# responsibility to obtain export licenses, or other export authority as may be required before
# exporting such information to foreign countries or providing access to foreign persons.
#

# externals
import numpy

# utility functions
def cosd(angd):
    # return cosine of angle expressed in degrees
    return numpy.cos(numpy.radians(angd))


def sind(angd):
    # return sine of angle expressed in degrees
    return numpy.sin(numpy.radians(angd))


def norm(v):
    # return 2-norm of a numpy.array
    return numpy.sqrt(v.dot(v))


def CDM(X, Y, X0, Y0, depth, ax, ay, az, omegaX, omegaY, omegaZ, opening, nu):
    """
    CDM
    calculates the surface displacements and potency associated with a CDM
    that is composed of three mutually orthogonal rectangular dislocations in
    a half-space.

    CDM: Compound Dislocation Model
    RD: Rectangular Dislocation
    EFCS: Earth-Fixed Coordinate System
    RDCS: Rectangular Dislocation Coordinate System
    ADCS: Angular Dislocation Coordinate System
    (The origin of the RDCS is the RD centroid. The axes of the RDCS are
    aligned with the strike, dip and normal vectors of the RD, respectively.)

    INPUTS
    X and Y:
    Horizontal coordinates of calculation points in EFCS (East, North, Up).
    X and Y must have the same size.

    X0, Y0 and depth:
    Horizontal coordinates (in EFCS) and depth of the CDM centroid. The depth
    must be a positive value. X0, Y0 and depth have the same unit as X and Y.

    omegaX, omegaY and omegaZ:
    Clockwise rotation angles about X, Y and Z axes, respectively, that
    specify the orientation of the CDM in space. The input values must be in
    degrees.

    ax, ay and az:
    Semi-axes of the CDM along the X, Y and Z axes, respectively, before
    applying the rotations. ax, ay and az have the same unit as X and Y.

    opening:
    The opening (tensile component of the Burgers vector) of the RDs that
    form the CDM. The unit of opening must be the same as the unit of ax, ay
    and az.

    nu:
    Poisson's ratio.

    OUTPUTS
    ue, un and uv:
    Calculated displacement vector components in EFCS. ue, un and uv have the
    same unit as opening and the CDM semi-axes in inputs.

    DV:
    Potency of the CDM. DV has the unit of volume (the unit of displacements,
    opening and CDM semi-axes to the power of 3).

    Example: Calculate and plot the vertical displacements on a regular grid.

    [X,Y] = numpy.meshgrid(-7:.02:7,-5:.02:5);
    X0 = 0.5; Y0 = -0.25; depth = 2.75; omegaX = 5; omegaY = -8; omegaZ = 30;
    ax = 0.4; ay = 0.45; az = 0.8; opening = 1e-3; nu = 0.25;
    import te[ [ue,un,uv,DV] = CDM(X,Y,X0,Y0,depth,omegaX,omegaY,omegaZ,ax,ay,az,...
    opening,nu);
    figure
    surf(X,Y,reshape(uv,size(X)),'edgecolor','none')
    view(2)
    axis equal
    axis tight
    set(gcf,'renderer','painters')

    Reference journal article:
    Nikkhoo, M., Walter, T. R., Lundgren, P. R., Prats-Iraola, P. (2016):
    Compound dislocation models (CDMs) for volcano deformation analyses.
    Submitted to Geophysical Journal International
    Copyright (c) 2016 Mehdi Nikkhoo

    Permission is hereby granted, free of charge, to any person obtaining a
    copy of this software and associated documentation files
    (the "Software"), to deal in the Software without restriction, including
    without limitation the rights to use, copy, modify, merge, publish,
    distribute, sublicense, and/or sell copies of the Software, and to permit
    persons to whom the Software is furnished to do so, subject to the
    following conditions:

    The above copyright notice and this permission notice shall be included
    in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
    OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN
    NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
    DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
    OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE
    USE OR OTHER DEALINGS IN THE SOFTWARE.

    I appreciate any comments or bug reports.

    Mehdi Nikkhoo
    Created: 2015.5.22
    Last modified: 2016.10.18

    Section 2.1, Physics of Earthquakes and Volcanoes
    Department 2, Geophysics
    Helmholtz Centre Potsdam
    German Research Centre for Geosciences (GFZ)

    email:
    mehdi.nikkhoo@gfz-potsdam.de
    mehdi.nikkhoo@gmail.com

    website:
    http://www.volcanodeformation.com

    Converted from Matlab to Python
    April 2018 by Eric Gurrola
    Jet Propulsion Lab/Caltech
    """

    ue=0
    un=0
    uv=0
    DV=0

    # [X, Y] is a meshgrid with X = repeated rows and Y = repeated columns
    # rows = linspace(xmin, xmax, (xmax-xmin)/dx +1)
    # columns = linspace(ymin, ymax, (ymax-ymin)/dy +1)
    # We will use numpy.ndarray for the array objects rather than matrices
    # (see, https://docs.scipy.org/doc/numpy-dev/user/numpy-for-matlab-users.html)
    #
    # this matlab code flattens a matrix in column major order and returns a column vector
    # X = X(:);
    # Y = Y(:);
    # in Python use method 'flatten' to flatten the 2-D array as an ndarray.  We will not
    # reshape ndarrays into column or row vectors until they are used in a matrix operation
    # where it would matter, which is maybe never since the common sense thing is done correctly
    # using the ndarray (shape of ndarray is coerced to make sense in the matrix operation).
    # In the following use of flatten, argument order='F' would create a column vector
    # (see docs.scipy.org/doc/numpy-dev/user/numpy-for-matlab-users.html)
#    X = X.flatten()
#    Y = Y.flatten()

    # convert the semi-axes (lengths) to axes
    ax = 2*ax
    ay = 2*ay
    az = 2*az

    # the axes coordinate rotation matrices
    Rx = numpy.array([
         [1.,  0.,            0.          ],
         [0.,  cosd(omegaX),  sind(omegaX)],
         [0., -sind(omegaX), cosd(omegaX)]
    ])

    Ry = numpy.array([
         [cosd(omegaY), 0., -sind(omegaY)],
         [0.,           1.,  0.          ],
         [sind(omegaY), 0.,  cosd(omegaY)]
    ])

    Rz = numpy.array([
         [ cosd(omegaZ), sind(omegaZ), 0.],
         [-sind(omegaZ), cosd(omegaZ), 0.],
         [ 0.,           0.,           1.]
    ])

    # the coordinate rotation matrix
    R = Rz.dot(Ry.dot(Rx))

    # The centroid
    P0 = numpy.array([X0, Y0, -depth])

    P1 = (P0+ay*R[:,1]/2. + az*R[:,2]/2.)
    P2 = (P1-ay*R[:,1])
    P3 = P2-az*R[:,2]
    P4 = P1-az*R[:,2]

    Q1 = P0-ax*R[:,0]/2. + az*R[:,2]/2.
    Q2 = Q1+ax*R[:,0]
    Q3 = Q2-az*R[:,2]
    Q4 = Q1-az*R[:,2]

    R1 = P0+ax*R[:,0]/2. + ay*R[:,1]/2.
    R2 = R1-ax*R[:,0]
    R3 = R2-ay*R[:,1]
    R4 = R1-ay*R[:,1]

    VertVec = numpy.array([P1[2], P2[2], P3[2], P4[2], Q1[2], Q2[2], Q3[2], Q4[2], R1[2], R2[2],
                           R3[2], R4[2]])

    if numpy.any(VertVec>0):
        # raise ValueError('Half-space solution: The CDM must be under the free surface!' +
        #                  ' VertVec={}'.format(VertVec))
        print('Half-space solution: The CDM must be under the free surface!' +
                         ' VertVec={}'.format(VertVec))

    if ax == 0 and ay == 0 and az == 0:
        ue = numpy.zeros(numpy.shape(X))
        un = numpy.zeros(numpy.shape(X))
        uv = numpy.zeros(numpy.shape(X))
    elif ax == 0 and ay !=0 and az !=0:
        [ue, un, uv] = RDdispSurf(X, Y, P1, P2, P3, P4, opening, nu)
    elif ax != 0 and ay == 0 and az != 0:
        [ue, un, uv] = RDdispSurf(X, Y, Q1, Q2, Q3, Q4, opening, nu)
    elif ax != 0 and ay != 0 and az == 0:
        [ue, un, uv] = RDdispSurf(X, Y, R1, R2, R3, R4, opening, nu)
    else:
        [ue1, un1, uv1] = RDdispSurf(X, Y, P1, P2, P3, P4, opening, nu)
        [ue2, un2, uv2] = RDdispSurf(X, Y, Q1, Q2, Q3, Q4, opening, nu)
        [ue3, un3, uv3] = RDdispSurf(X, Y, R1, R2, R3, R4, opening, nu)
        ue = ue1+ue2+ue3
        un = un1+un2+un3
        uv = uv1+uv2+uv3

    # Calculate the CDM potency (aX, aY and aZ were converted to full axes)
    DV = (ax*ay+ax*az+ay*az)*opening

    return  ue, un, uv


def RDdispSurf(X, Y, P1, P2, P3, P4, opening, nu):
    """
    RDdispSurf calculates surface displacements associated with a rectangular
    dislocation in an elastic half-space.
    """

    bx = opening

    Vnorm = numpy.cross(P2-P1, P4-P1)
    Vnorm = Vnorm/norm(Vnorm)
    bX = bx*Vnorm[0]
    bY = bx*Vnorm[1]
    bZ = bx*Vnorm[2]

    [u1,v1,w1] = AngSetupFSC(X,Y,bX,bY,bZ,P1,P2,nu) # Side P1P2
    [u2,v2,w2] = AngSetupFSC(X,Y,bX,bY,bZ,P2,P3,nu) # Side P2P3
    [u3,v3,w3] = AngSetupFSC(X,Y,bX,bY,bZ,P3,P4,nu) # Side P3P4
    [u4,v4,w4] = AngSetupFSC(X,Y,bX,bY,bZ,P4,P1,nu) # Side P4P1

    ue = u1+u2+u3+u4
    un = v1+v2+v3+v4
    uv = w1+w2+w3+w4

    return  ue, un, uv


def CoordTrans(x1, x2, x3, A):
    """
    CoordTrans transforms the coordinates of the vectors, from
    x1x2x3 coordinate system to X1X2X3 coordinate system. "A" is the
    transformation matrix, whose columns e1,e2 and e3 are the unit base
    vectors of the x1x2x3. The coordinates of e1,e2 and e3 in A must be given
    in X1X2X3. The transpose of A (i.e., A') will transform the coordinates
    from X1X2X3 into x1x2x3.
    """

# In Matlab these three lines ensure that x1, x2, x3 are column vectors, which is assumed in the
# Matlab version of this routine.  There is no need to do this with numpy.array.
#    x1 = x1(:);
#    x2 = x2(:);
#    x3 = x3(:);

    # check that the vectors x1, x2, x3 are of the correct length
#    if not (len(x1)==3 and len(x2)==3 and len(x3)==3):
#        raise ValueError("not all of x1, x2, x3 are of length 3")

    # no need to convert x1, x2, x3 from column vectors into row vectors. They are
    # numpy ndarrays and ready to work properly; the following uses them as rows in an array.
    r = A.dot(numpy.array([x1, x2, x3]))
    if len(r.shape) == 2:
        X1 = r[0,:]
        X2 = r[1,:]
        X3 = r[2,:]
    else:
        X1 = r[0]
        X2 = r[1]
        X3 = r[2]
    return X1, X2, X3


def AngSetupFSC(X, Y, bX, bY, bZ, PA, PB, nu):
    """
    AngSetupSurf calculates the displacements associated with an angular
    dislocation pair on each side of an RD in a half-space.
    """

    SideVec = PB-PA
    eZ = numpy.array([0, 0, 1])
    beta = numpy.arccos(-SideVec.dot(eZ)/norm(SideVec))

    eps = numpy.spacing(1) # distance between 1 and the nearest floating point number
    if numpy.abs(beta)<eps or numpy.abs(numpy.pi-beta)<eps :
        ue = numpy.zeros(numpy.shape(X))
        un = numpy.zeros(numpy.shape(X))
        uv = numpy.zeros(numpy.shape(X))
    else:
        ey1 = numpy.array([*SideVec[0:2],0])
        ey1 = ey1/norm(ey1)
        ey3 = -eZ
        ey2 = numpy.cross(ey3,ey1)
        A = numpy.array([ey1, ey2, ey3]) # Transformation matrix

        # Transform coordinates from EFCS to the first ADCS
        [y1A, y2A, unused] = CoordTrans(X-PA[0], Y-PA[1], numpy.zeros(X.size)-PA[2], A)
        # Transform coordinates from EFCS to the second ADCS
        [y1AB, y2AB, unused] = CoordTrans(SideVec[0], SideVec[1], SideVec[2], A)
        y1B = y1A-y1AB
        y2B = y2A-y2AB

        # Transform slip vector components from EFCS to ADCS
        [b1, b2, b3] = CoordTrans(bX, bY, bZ, A)

        # Determine the best artefact-free configuration for the calculation
        # points near the free surface
        I = (beta*y1A)>=0
        J = numpy.logical_not(I)

        v1A = numpy.zeros(I.shape)
        v2A = numpy.zeros(I.shape)
        v3A = numpy.zeros(I.shape)
        v1B = numpy.zeros(I.shape)
        v2B = numpy.zeros(I.shape)
        v3B = numpy.zeros(I.shape)

        # Configuration I
        v1A[I], v2A[I], v3A[I] = AngDisDispSurf(y1A[I], y2A[I], -numpy.pi+beta, b1, b2, b3, nu,
                                                -PA[2])
        v1B[I], v2B[I], v3B[I] = AngDisDispSurf(y1B[I], y2B[I], -numpy.pi+beta, b1, b2, b3, nu,
                                                -PB[2])

        # Configuration II
        v1A[J], v2A[J], v3A[J] = AngDisDispSurf(y1A[J], y2A[J], beta, b1, b2, b3, nu, -PA[2])
        v1B[J], v2B[J], v3B[J] = AngDisDispSurf(y1B[J], y2B[J], beta, b1, b2, b3, nu, -PB[2])

        # Calculate total displacements in ADCS
        v1 = v1B-v1A
        v2 = v2B-v2A
        v3 = v3B-v3A

        # Transform total displacements from ADCS to EFCS
        [ue, un, uv] = CoordTrans(v1, v2, v3, A.transpose())

    return ue, un, uv


def AngDisDispSurf(y1, y2, beta, b1, b2, b3, nu, a):
    """
    AngDisDispSurf calculates the displacements associated with an angular dislocation
    in a half-space.
    """

    sinB = numpy.sin(beta)
    cosB = numpy.cos(beta)
    cotB = 1.0/numpy.tan(beta)
    z1 = y1*cosB + a*sinB
    z3 = y1*sinB - a*cosB
    r2 = y1**2 + y2**2 + a**2
    r = numpy.sqrt(r2)

    Fi = 2*numpy.arctan2(y2, (r+a)/numpy.tan(beta/2)-y1) # The Burgers function

    v1b1 = b1/2/numpy.pi*(
               (1-(1-2*nu)*cotB**2)*Fi +
               y2/(r+a)*((1-2*nu)*(cotB+y1/2/(r+a))-y1/r) -
               y2*(r*sinB-y1)*cosB/r/(r-z3)
           )
    v2b1 = b1/2/numpy.pi*(
               (1-2*nu)*((.5+cotB**2)*numpy.log(r+a)-cotB/sinB*numpy.log(r-z3)) -
               1./(r+a)*((1-2*nu)*(y1*cotB-a/2-y2**2/2/(r+a))+y2**2/r) +
               y2**2*cosB/r/(r-z3)
           )
    v3b1 = b1/2/numpy.pi*(
               (1-2*nu)*Fi*cotB+y2/(r+a)*(2*nu+a/r) -
               y2*cosB/(r-z3)*(cosB+a/r)
          )

    v1b2 = b2/2/numpy.pi*(
               -(1-2*nu)*((.5-cotB**2)*numpy.log(r+a) + cotB**2*cosB*numpy.log(r-z3) ) -
               1/(r+a)*((1-2*nu)*(y1*cotB+.5*a+y1**2/2/(r+a)) - y1**2/r) +
               z1*(r*sinB-y1)/r/(r-z3)
           )
    v2b2 = b2/2/numpy.pi*(
               (1+(1-2*nu)*cotB**2)*Fi -
               y2/(r+a)*((1-2*nu)*(cotB+y1/2/(r+a))-y1/r) -
               y2*z1/r/(r-z3)
           )
    v3b2 = b2/2/numpy.pi*(
               -(1-2*nu)*cotB*(numpy.log(r+a)-cosB*numpy.log(r-z3)) -
               y1/(r+a)*(2*nu+a/r) +
               z1/(r-z3)*(cosB+a/r)
           )

    v1b3 = b3/2/numpy.pi*(y2*(r*sinB-y1)*sinB/r/(r-z3))
    v2b3 = b3/2/numpy.pi*(-y2**2*sinB/r/(r-z3))
    v3b3 = b3/2/numpy.pi*(Fi + y2*(r*cosB+a)*sinB/r/(r-z3))

    v1 = v1b1 + v1b2 + v1b3
    v2 = v2b1 + v2b2 + v2b3
    v3 = v3b1 + v3b2 + v3b3

    return v1, v2, v3

# end-of-file

#!/usr/bin/env python3

# THIS FILE SHOULD CONTAIN THE ORIGINAL WORKING VERSION IN PLAIN PYTHON.  IT IS THE TEST CASE
# AGAINST WHICH THE REVERSO.PY OUTPUT WILL BE COMPARED.  IT IS NOT THE VERSION THAT IMPORTS
# ALTAR, datasheet, etc.

# The Two-Reservoir Model
# This model assumes an elastic half-space and incompressible magma. The two magma
# reservoirs comprise a deep reservoir connected to a shallow reservoir by an
# hydraulic pipe ["A two-magma chamber model as a source of deformation at Grimvsvotn
# Volcano, Iceland by Reverso etal (2014) Journal of Geophysical Research: Solid Earth

import numpy
from matplotlib import pyplot

class ReversoModel:
    """
    A two-magma chamber model as a source of deformation at Grimsvotn Volcano, Iceland
    Thomas Reverso etal.  Journal of Geophysical Research, AGU, 2014, 119, pp. 4666-4683
    """
    def __init__(self, locations, los, H_s, H_d, a_s, a_d, a_c, Qin, dPs0=0., dPd0=0., g=9.8, G=20.0e9, nu=0.25, mu=2000.0, drho=300.0, shape='sill'):
        # observation locations
        self.locations = locations
        # observation line of sight at each location
        self.los = los

        # the reverso source model geometry and physical parameters:
        # H_s = depth to the shallow resevoir (meters)
        self.H_s = H_s
        # H_d = depth to the deep reservoir (meters)
        self.H_d = H_d
        # a_s = radius of shallow reservoir (meters)
        self.a_s = a_s
        # a_d = radius of deep reservoir (meters)
        self.a_d = a_d
        # a_c = radius of the tube connecting the two reservoirs (meters)
        self.a_c = a_c
        # Qin = constant magma flux input to the deep reservoir (meters**3/sec)
        self.Qin = Qin
        # dPs0, dPd0 = initial overpressures in shallow and deep chambers
        self.dPs0 = dPs0
        self.dPd0 = dPd0
        # acceleration due to gravity (m/s**2)
        self.g = g
        # G   = the rigidity (or shear) modulus (kg/m/s**2)
        self.G = G
        # nu  = the Poisson ratio (dimensionless)
        self.nu = nu
        # mu  = the magma viscosity (kg/m/s**2)
        self.mu = mu
        # drho = the difference in rock-density and magma-density kg/m**3
        self.drho = drho
        # shape of the magma chambers ('sill' or 'sphere')
        if shape == 'sill':
            self.shape = 'sill'
        elif shape == 'sphere':
            self.shape = 'sphere'
        else:
            print("The chamber shapes must be either 'sill' or 'sphere'")
            raise

        # derived quantities
        # ratio of deep/shallow radii cubed
        self.k = (self.a_d/self.a_s)**3
        self.H_c = 0.
        if self.shape == 'sphere':
            # length of tube between the shallow and deep reservoirs
            self.H_c = (self.H_d - self.a_d) - (self.H_s - self.a_s)
            # dimensionless shape factors for "spherical" reservoirs (Reverso, eq. 9)
            self.gamma_s = 1.0
            self.gamma_d = 1.0
        elif self.shape == 'sill':
            # length of tube between the shallow and deep reservoirs
            # the height of the two "sill" (oblate) reservoirs is assumed to be negligible here
            self.H_c = self.H_d - self.H_s
            # dimensionless shape factors for "sill" reservoirs (Reverso, eq. 9)
            self.gamma_s = 8.0*(1.0-self.nu)/(3.*numpy.pi)
            self.gamma_d = 8.0*(1.0-self.nu)/(3.*numpy.pi)
        else:
            print("Unknown magma chamber shape.  Use either 'sill' or 'sphere'")


        return

    def alpha_sd(self, Rs, Rd):
        """
        Compute the [shallow, deep] chamber alpha ratios in Reverso eq. (19).
        """
        if self.shape == 'sphere':
            return [1.0, 1.0]
        elif self.shape == 'sill':
            # alpha = [alpha_s, alpha_d]
            return [4.0*self.H_s**2/(numpy.pi*Rs**2),
                    4.0*self.H_d**2/(numpy.pi*Rd**2)]
        else:
            print("Unkown magma chamber shape.  Use either 'sill' or 'sphere'")

        return

    def Urmat(self, r):
        """
        The horizontal surface displacement at distance r radial to the source
        (i.e., radial in the plane of the observed displacements).
        """
        # distance from the shallow reservoir to the surface displacement observation station
        R_s = numpy.sqrt(r**2 + self.H_s**2)
        # distance from the deep reservoir to the surface displacement observation station
        R_d = numpy.sqrt(r**2 + self.H_d**2)

        alphas, alphad = self.alpha_sd(R_s, R_d)

        # eq. (17) for Ur(t): the horizontal surface displacement of a point at
        # (cylindrical) radius r from the pipe connecting the reservoirs to the
        # observation point.
        # Distance from shallow reservoir = (H_s**2 + r**2)**(0.5)
        # Distance from deep    reservoir = (H_d**2 + r**2)**(0.5)
        H = ([
              [r*self.a_s**3*alphas*(1-self.nu)/(self.G*(self.H_s**2+r**2)**1.5),
               r*self.a_d**3*alphad*(1-self.nu)/(self.G*(self.H_d**2+r**2)**1.5)]
             ])

        return H

    def Uzmat(self, r):
        R_s = numpy.sqrt(r**2 + self.H_s**2)
        R_d = numpy.sqrt(r**2 + self.H_d**2)

        alphas, alphad = self.alpha_sd(R_s, R_d)

        if self.gamma_s == 1.0:
            alphas = 1.0
        else:
            alphas = 4.*self.H_s**2/(numpy.pi*R_s**2)

        if self.gamma_d == 1.0:
            alphad = 1.0
        else:
            alphad = 4.*self.H_d**2/(numpy.pi*R_d**2)

        H = ([
              [self.H_s*self.a_s**3*alphas*(1-self.nu)/(self.G*(self.H_s**2+r**2)**1.5),
               self.H_d*self.a_d**3*alphad*(1-self.nu)/(self.G*(self.H_d**2+r**2)**1.5)]
             ])

        return H

    def losmat(self, x, y):
        r = numpy.sqrt(x**2 + y**2)
        R_s = numpy.sqrt(r**2 + self.H_s**2)
        R_d = numpy.sqrt(r**2 + self.H_d**2)

        if self.gamma_s == 1.0:
            alhpas = 1.0
        else:
            alphas = (4.0*self.H_s**2)/(numpy.pi*R_s**2)

        if self.gamma_d == 1.0:
            alhpad = 1.0
        else:
            alphad = (4.0*self.H_d**2)/(numpy.pi*R_d**2)

        # Constants
        GAMMA = (1.0-self.nu)/self.G
        Ds = alphas * (self.a_s/R_s)**3
        Dd = alphad * (self.a_d/R_d)**3

        H = ([
              [GAMMA*Ds*(numpy.sin(self.theta)*(numpy.sin(self.self.phi)*y -
                  numpy.sin(self.theta)*numpy.cos(self.phi)*x) +
                  numpy.cos(self.theta)*self.H_s),
               GAMMA*Dd*(numpy.sin(self.theta)*(numpy.sin(self.phi)*y -
                  numpy.sin(self.theta)*numpy.cos(self.phi)*x)  +
                  numpy.cos(self.theta)*self.H_d)
               ]
             ]
            )

        return H

    def overpressures(self):
        # Compute the overpressures in the shallow and deep reservoirs
        # Analytic solution equations (10)-(12), Reverso (2014)
        # t = time vector
        # mu = viscosity
        #
        # the exponential time scale: tau = 1/ξ, after eq. (10)
        print("overpressures")
        print("self.mu = {}".format(self.mu))
        print("self.H_c = {}".format(self.H_c))
        print("self.gamma_s = {}".format(self.gamma_s))
        print("self.gamma_d = {}".format(self.gamma_d))
        print("self.k = {}".format(self.k))
        print("self.a_c = {}".format(self.a_c))
        print("self.a_s = {}".format(self.a_s))
        print("self.G = {}".format(self.G))
        tau = ((8.0*self.mu*self.H_c**self.gamma_s*self.gamma_d*self.k*self.a_s**3)/
              (self.G*self.a_c**4*(self.gamma_s+self.gamma_d*self.k)))
        print("tau = {}".format(tau))
        # The A coefficient of the exponential in the solution, eq. (11)
        A =  self.gamma_d*self.k/(self.gamma_s + self.gamma_d*self.k)
        print("A = {}".format(A))
        A *= (self.dPd0 - self.dPs0 +
              self.drho*self.g*self.H_c -
              8.*self.gamma_s*self.mu*self.Qin*self.H_c/(
                  numpy.pi*self.a_c**4*(self.gamma_s+self.gamma_d*self.k))
             )
        print("A = {}".format(A))
        # the exponential in time term in the solution
        f0 = A*(1. - numpy.exp(-self.t/tau))
        # the secular linear in time term
        f1 = self.G*self.Qin*self.t/(numpy.pi*self.a_s**3*(self.gamma_s+self.gamma_d*self.k))

        # dPs = △ Ps eq. (11)
        self.dPs_analytic = f0 + f1 + self.dPs0

        # dPd = △ Pd  eq. (12)
        self.dPd_analytic = -f0*self.gamma_s/(self.gamma_d*self.k) + f1 + self.dPd0

        # return
        return

    def displacements(self):
        print("Number of spacial observations = {}".format(len(self.r)))
        # H-matrix for the radial displacement
        H_Ur = numpy.squeeze([reverso.Urmat(r) for i, r in enumerate(self.r)])
        # H-matrix for the vertical displacement
        H_Uz = numpy.squeeze([reverso.Uzmat(r) for i, r in enumerate(self.r)])

        # Generate the corresponding displacements
        # H-matrix for the radial displacement
        self.Ur = numpy.squeeze([numpy.mat(H_Ur) * numpy.mat([[reverso.dPs_analytic[i]],
                                [reverso.dPd_analytic[i]]]) for i in range(nt)])
        self.Uz = numpy.squeeze([numpy.mat(H_Uz) * numpy.mat([[reverso.dPs_analytic[i]],
                                [reverso.dPd_analytic[i]]]) for i in range(nt)])
        return

def runReverso(plot=False):
    # Physical parameters
    # shear modulus, [Pa, kg-m/s**2]
    G = 20.0E9
    # Poisson's ratio
    nu = 0.25
    # Viscosity [Pa-s]
    mu = 2000.0
    # Density difference (ρ_r-ρ_m), [kg/m**3]
    drho = 300.0
    # Gravitational acceleration [m/s**2]
    g = 9.81

    # Basal conditions
    Qin = 0.6   # Basal magma inflow rate [m**3/s]

    # Initial conditions
    # Shallow reservoir overpressure at t=0 [Pa]
    dPs0 = 0.0
    # Deep reservoir overpressure at t=0 [Pa]
    dPd0 = 0.0

    # Geometry
    # radius of the hydraulic pipe
    a_c = 1.5
    # radius of the shallow reservoir
    a_s = 2.0e3
    # radius of the deep reservoir
    a_d = 2.2e3
    # depth of the deep reservoir
    H_d = 4.0e3
    # depth of the shallow reservoir
    H_s = 3.0e3

    # observation locations (x, y, t)
    # the observation points at radius r = sqrt(x**2+y**2) in the z=0 plane and at time t
    # create meshgrid of observation positions in the z=0 plane
    x = numpy.arange(-5100, 0, 1000)
    x = numpy.append(x, -numpy.flip(x))
    y = x
    # time-step -1 day in seconds
    dt = 86400.0
    # max time
    tmax = dt*365.0
    # the time array in seconds
    t = numpy.arange(0, tmax, dt)
    # the time array as fraction of total duration
    tfrac = t/tmax
    nt = len(tfrac)
    print("Number of time samples = {}".format(nt))

    # meshgrids
    X, Y, T = numpy.meshgrid(x, y, t)
    # flatten
    xx = X.flatten()
    yy = Y.flatten()
    tt = T.flatten()
    # locations of observations at (x,y,t)
    locations = [(xxx, yyy, ttt) for (xxx, yyy, ttt) in zip(xx, yy, tt)]
    # radii of the observation in the z=0 plane
    # r = numpy.sqrt(x**2 + y**2)

    # Synthetic InSAR dataset
    # Incidence angle, theta
    theta = numpy.pi * (41./180.)
    # Azimuth angle, phi
    phi = numpy.pi * (-169./180.)

    # observation los vector (at corresponding index in locations)
    los = []
    # set the observation locations in space and time
    # run the Reverso Model
    reverso = ReversoModel(locations, los, H_s, H_d, a_s, a_d, a_c, Qin, dPs0, dPd0, g, G, nu, mu, drho, shape='sill')

    print("Configuration of the Reverso class object:")
    print("The shape of the magma chambers:   reverso.shape = {}".format(reverso.shape))
    print("The depth to the magma chambers:   reverso.H_s = {},  reverso.H_d = {}".format(reverso.H_s, reverso.H_d))
    print("The radii of the magma chambers:   reverso.a_s = {},  reverso.a_d = {}".format(reverso.a_s, reverso.a_d))
    print("The radius of the connecting tube: reverso.a_c = {}".format(reverso.a_c))
    print("The input magma flow from below:   reverso.Qin = {}".format(reverso.Qin))
    print("The initial overpressures:         reverso.dPs0 = {}, reverso.dPd0 = {}".format(reverso.dPs0, reverso.dPd0))
    print("The physical parameters: ")
    print("The shear modulus:                 reverso.G = {}".format(reverso.G))
    print("The Poisson ratio:                 reverso.nu = {}".format(reverso.nu))
    print("The magma viscocity:               reverso.mu = {}".format(reverso.mu))
    print("The density difference rock-magma: reverso.drho = {}".format(reverso.drho))

    # Analytic solution for overpressures.  Computes members dPs_analytic(r,t), dPd_analytic(r,t)
    reverso.overpressures()

    # The surface displacements in r=sqrt(x**2+y**2), z at point (x,y,z,t) = (x,y,0,t)
    reverso.displacements()

    # Comparing Analytical solution with the differential equation
    if plot:
#        pyplot.plot(tfrac, dPs/1.0e6, label='Differential')
        pyplot.plot(tfrac, reverso.dPs_analytic/1.0e6, ls='--', lw=6, alpha=0.6, label='Analytical')
        pyplot.legend(loc=2, prop={'size':14}, framealpha=0.5)
        pyplot.title('Shallow Overpressure (MPa)')
        pyplot.show()

#        pyplot.plot(tfrac, dPd/1.0e6, label='Differential')
        pyplot.plot(tfrac, reverso.dPd_analytic/1.0e6, ls='--', lw=6, alpha=0.6, label='Analytical')
        pyplot.legend(loc=2, prop={'size':14}, framealpha=0.5)
        pyplot.title('Deep Overpressure (MPa)')
        pyplot.show()

    if plot:
        #Plot radial displacement
        for i, label in enumerate(rr):
            pyplot.plot(tfrac, Ur[:,i], label='r={}'.format(label/1000.)+' km')
        pyplot.legend()
        pyplot.title('Radial Displacement (m)')
        pyplot.show()

        #Plot vertical displacement
        for i, label in enumerate(rr):
            pyplot.plot(tfrac, Uz[:,i], label='r={}'.format(label/1000.)+' km')
        pyplot.legend()
        pyplot.title('Vertical Displacement (m)')
        pyplot.show()

    H_los = [reverso.losmat(x, y)]
    print()
    print("H_los")
    print(H_los)
    # that's all
    return

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        plot = True
    else:
        plot = False
    status = runReverso(plot)
    raise SystemExit(status)

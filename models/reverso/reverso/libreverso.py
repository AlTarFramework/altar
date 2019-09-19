#!/usr/bin/env python3

# The Two-Reservoir Model
# This model assumes an elastic half-space and incompressible magma. The two magma
# reservoirs comprise a deep reservoir connected to a shallow reservoir by an
# hydraulic pipe ["A two-magma chamber model as a source of deformation at Grimvsvotn
# Volcano, Iceland by Reverso etal (2014) Journal of Geophysical Research: Solid Earth

import numpy
from matplotlib import pyplot

def Urmat(Hs, Hd, gammas, gammad, r, G, a_s, a_d, v):
    # distance from the shallow reservoir to the surface displacement observation station
    Rs = numpy.sqrt(r**2 + Hs**2)
    # distance from the deep reservoir to the surface displacement observation station
    Rd = numpy.sqrt(r**2 + Hd**2)

    if gammas == 1.0:
        # setting if shallow reservoir is spherical
        alphas = 1.0
    else:
        # setting if shallow reservoir is sill-like reservoir [Reverso p.9]
        alphas = 4.*Hs**2/(numpy.pi*Rs**2)

    if gammad == 1.0:
        # setting if deep reservoir is spherical
        alphad = 1.0
    else:
        # setting if deep reservoir is sill-like reservoir [Reverso p.9]
        alphad = 4.*Hd**2/(numpy.pi*Rd**2)

    # eq. (17) for Ur(t): the horizontal surface displacement of a point at
    # (cylindrical) radius r from the pipe connecting the reservoirs to the
    # observation point.  R = (Hs**2 + r**2)**(0.5)
    H = ([
          [r*a_s**3*alphas*(1-v)/(G*(Hs**2+r**2)**1.5),
           r*a_d**3*alphad*(1-v)/(G*(Hd**2+r**2)**1.5)]
         ])

    return H

def Uzmat(Hs, Hd, gammas, gammad, r, G, a_s, a_d, v):
    Rs = numpy.sqrt(r**2 + Hs**2)
    Rd = numpy.sqrt(r**2 + Hd**2)

    if gammas == 1.0:
        alphas = 1.0
    else:
        alphas = 4.*Hs**2/(numpy.pi*Rs**2)

    if gammad == 1.0:
        alphad = 1.0
    else:
        alphad = 4.*Hd**2/(numpy.pi*Rd**2)

    H = ([
          [Hs*a_s**3*alphas*(1-v)/(G*(Hs**2+r**2)**1.5),
           Hd*a_d**3*alphad*(1-v)/(G*(Hd**2+r**2)**1.5)]
         ])

    return H

def losmat(Hs, Hd, gammas, gammad, x, y, G, a_s, a_d, v, theta, phi):
    r = numpy.sqrt(x**2 + y**2)
    Rs = numpy.sqrt(r**2 + Hs**2)
    Rd = numpy.sqrt(r**2 + Hd**2)

    if gammas == 1.0:
        alhpas = 1.0
    else:
        alphas = (4.0*Hs**2)/(numpy.pi*Rs**2)

    if gammad == 1.0:
        alhpad = 1.0
    else:
        alphad = (4.0*Hd**2)/(numpy.pi*Rd**2)

    # Constants
    GAMMA = (1.0-v)/G
    Ds = alphas * (a_s/Rs)**3
    Dd = alphad * (a_d/Rd)**3

    H = ([
           [GAMMA*Ds*(numpy.sin(theta)*(numpy.sin(phi)*y -
                      numpy.sin(theta)*numpy.cos(phi)*x) +
                      numpy.cos(theta)*Hs)               ,
            GAMMA*Dd*(numpy.sin(theta)*(numpy.sin(phi)*y -
                     numpy.sin(theta)*numpy.cos(phi)*x)  +
                      numpy.cos(theta)*Hd)
           ]
         ]
        )

    return H

def analytic(t, mu, G, g, Hc, gammas, gammad, k, a_s, ac, dPd0, dPs0, drho, Qin):
    # Analytic solution
    # Calculate the characteristic time constant: tau = 1/ξ eq. (10)
    tau = (8.0*mu*Hc**gammas*gammad*k*a_s**3)/(G*ac**4*(gammas+gammad*k))

    A =  gammad*k/(gammas + gammad*k)
    A *= dPd0 - dPs0 + drho*g*Hc - 8.*gammas*mu*Qin*Hc/(numpy.pi*ac**4*(gammas+gammad*k))

    f0 = A*(1. - numpy.exp(-t/tau))
    f1 = G*Qin*t/(numpy.pi*a_s**3*(gammas+gammad*k))
    dPs_anal = f0 + f1 + dPs0
    dPd_anal = -f0*gammas/(gammad*k) + f1 + dPd0
    return dPs_anal, dPd_anal


def main(plot=False):
    ## Physical parameters
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
    ac = 1.5
    # radius of the shallow reservoir
    a_s = 2.0e3
    # radius of the deep reservoir
    a_d = 2.2e3
    # ratio of the reservoir volumes
    k = (a_d/a_s)**3
    # depth of the deep reservoir
    Hd = 4.0e3
    # depth of the shallow reservoir
    Hs = 3.0e3
    # length of the hydraulic connection (no vertical extensions of the reservoirs? Fig 6.)
    Hc = Hd - Hs
    gammas = 8.0*(1.0-nu)/(3.*numpy.pi)
    gammad = 8.0*(1.0-nu)/(3.*numpy.pi)

    # time-step in seconds (1 day)
    dt = 86400.0
    # max time (1 year) in seconds
    tmax = dt*365.0 *1.0

    ## differential equation
    # the time array in seconds
    t = numpy.arange(0, tmax, dt)
    # the time array as fraction of total duration
    tfrac = t/tmax
    nt = len(t)
    print("Number of time samples = {}".format(nt))
    ## Initialization
    dPs = numpy.zeros(nt)
    dPs[0] = dPs0
    dPd = numpy.zeros(nt)
    dPd[0] = dPd0

    # Simplifying the equations
    # Eq. (10) 1/ξ = *γ_d*k/(γ_s+γ_d*k)
    C1 = (G*ac**4)/(8*mu*Hc*a_s**3*gammas)
    # A in eq (11) modified to incorporate initial overpressures
    A1 = drho*g*Hc + dPd0 - dPs0
    A2 = G*Qin / (gammad*numpy.pi*a_d**3)
    C2 = gammas / (gammad*k)

    for i in range(1, nt):
        dPs[i] = dt*C1*(A1 + dPd[i-1] - dPs[i-1]) + dPs[i-1]
        dPd[i] = A2*dt - C2*(dPs[i] - dPs[i-1])  + dPd[i-1]

    if plot:
        pyplot.plot(tfrac, dPs/1.0e6, label='Differential')
        pyplot.legend(loc=2, prop={'size':14}, framealpha=0.5)
        pyplot.show()

        pyplot.plot(tfrac, dPd/1.e6, label='Differential')
        pyplot.legend(loc=2, prop={'size':14}, framealpha=0.5)
        pyplot.show()

    if 1:
        # Analytic solution
        dPs_anal, dPd_anal = analytic(t, mu, G, g, Hc, gammas, gammad, k, a_s, ac, dPd0, dPs0, drho, Qin)
    else:
        # Calculate the characteristic time constant: tau = 1/ξ eq. (10)
        tau = (8.0*mu*Hc**gammas*gammad*k*a_s**3)/(G*ac**4*(gammas+gammad*k))

        A =  gammad*k/(gammas + gammad*k)
        A *= dPd0 - dPs0 + drho*g*Hc - 8.*gammas*mu*Qin*Hc/(numpy.pi*ac**4*(gammas+gammad*k))

        f0 = A*(1. - numpy.exp(-t/tau))
        f1 = G*Qin*t/(numpy.pi*a_s**3*(gammas+gammad*k))
        dPs_anal = f0 + f1 + dPs0
        dPd_anal = -f0*gammas/(gammad*k) + f1 + dPd0

    # Comparing Analytical solution with the differential equation
    if plot:
        pyplot.plot(tfrac, dPs/1.0e6, label='Differential')
        pyplot.plot(tfrac, dPs_anal/1.0e6, ls='--', lw=6, alpha=0.6, label='Analytical')
        pyplot.legend(loc=2, prop={'size':14}, framealpha=0.5)
        pyplot.title('Shallow Overpressure (MPa)')
        pyplot.show()

        pyplot.plot(tfrac, dPd/1.0e6, label='Differential')
        pyplot.plot(tfrac, dPd_anal/1.0e6, ls='--', lw=6, alpha=0.6, label='Analytical')
        pyplot.legend(loc=2, prop={'size':14}, framealpha=0.5)
        pyplot.title('Deep Overpressure (MPa)')
        pyplot.show()


    # Generate r-array of GNSS stations.
    # r is the distance from the center of the volcano and the GNSS station (or InSAR points)
    rr = numpy.arange(1000, 6000, 1000)

    # Number of observations
    nObs = len(rr)
    print("Number of spacial observations = {}".format(nObs))
    # H-matrix for the radial displacement
    H_Ur = numpy.squeeze([Urmat(Hs, Hd, gammas, gammad, r, G, a_s, a_d, nu) for i, r in enumerate(rr)])
    # H-matrix for the vertical displacement
    H_Uz = numpy.squeeze([Uzmat(Hs, Hd, gammas, gammad, r, G, a_s, a_d, nu) for i, r in enumerate(rr)])

    # Generate the corresponding displacements
    # H-matrix for the radial displacement
    Ur = numpy.squeeze([numpy.mat(H_Ur) * numpy.mat([[dPs[i]], [dPd[i]]]) for i in range(nt)])
    Uz = numpy.squeeze([numpy.mat(H_Uz) * numpy.mat([[dPs[i]], [dPd[i]]]) for i in range(nt)])
    print("Ur = {}".format(Ur))
    print("Uz = {}".format(Uz))

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

    # Synthetic InSAR dataset
    # Incidence angle, theta
    theta = numpy.pi * (41./180.)
    # Azimuth angle, phi
    phi = numpy.pi * (-169./180.)

    # create meshgrid
    x = numpy.arange(-5000, 5100, 1000)
    y = x
    X, Y = numpy.meshgrid(x, y)
    H_los = [losmat(Hs, Hd, gammas, gammad, x, y, G, a_s, a_d, nu, theta, phi)]


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        plot = True
    else:
        plot = False
    status = main(plot)
    raise SystemExit(status)

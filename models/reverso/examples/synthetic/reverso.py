#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2020 parasim inc
# (c) 2010-2020 california institute of technology
# all rights reserved


# externals
import math
# framework
import altar
# my model
import altar.models.reverso


# app
class Reverso(altar.application, family="altar.applications.reverso"):
    """
    A generator of synthetic data for {reverso} sources
    """


    # public data
    H_s = altar.properties.float(default=3.0e3)
    H_s.doc = "depth of the shallow reservoir"

    H_d = altar.properties.float(default=4.0e3)
    H_d.doc = "depth of the deep reservoir"

    a_s = altar.properties.float(default=2.0e3)
    a_s.doc = "radius of the shallow magma reservoir"

    a_d = altar.properties.float(default=2.2e3)
    a_d.doc = "radius of the deep magma reservoir"

    a_c = altar.properties.float(default=1.5)
    a_c.doc = "radius of the hydraulic pipe connecting two magma reservoirs"

    Qin = altar.properties.float(default=0.6)
    Qin.doc = "basal magma inflow rate"

    # physical parameters
    G = altar.properties.float(default=20.0E9)
    G.doc = "shear modulus, [Pa, kg-m/s**2]"

    v = altar.properties.float(default=0.25)
    v.doc = "Poisson's ratio"

    mu = altar.properties.float(default=2000.0)
    mu.doc = "viscosity [Pa-s]"

    drho = altar.properties.float(default=300.0)
    drho.doc = "density difference (ρ_r-ρ_m), [kg/m**3]"

    g = altar.properties.float(default=9.81)
    g.doc = "gravitational acceleration [m/s**2]"


    # obligations
    @altar.export
    def main(self, *args, **kwds):
        """
        The main entry point
        """
        # build the data records
        data = self.reverso()
        # dump the displacements in a CSV file
        data.write(uri="displacements.csv")
        # all done
        return 0


    # meta methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # generate my the observation locations and times
        self.ticks = tuple(self.makeTicks())
        # all done
        return


    # implementation details
    def reverso(self):
        """
        The generator
        """
        # make a source
        source = altar.models.reverso.source(
            H_s=self.H_s, H_d=self.H_d, a_s=self.a_s, a_d=self.a_d, a_c=self.a_c,
            Qin=self.Qin,
            G=self.G, v=self.v, mu=self.mu, drho=self.drho, g=self.g,
            )

        # prep the dataset; the layout is baked in
        # rows: one for each location, time
        # columns: oid, t,x,y,  u.E,u.N,u.U, σ.E,σ.N,σ.U
        #
        # the observation id simulates observations from different sensors
        data = altar.models.reverso.data(name="displacements")

        # get the observation locations and times
        ticks = self.ticks
        # prime the displacement calculator
        displacements = source.displacements(locations=ticks)

        # compute the displacements
        for i,((t,x,y), (u_r, u_Z)) in enumerate(zip(ticks, displacements)):
            # make a new entry in the data sheer
            rec = data.pyre_new()

            # record the observation id
            rec.oid = 0
            # record time and location
            rec.t = t
            rec.x = x
            rec.y = y

            # find the polar angle of the vector to the observation location
            phi = math.atan2(y,x)
            # compute the E and N components
            u_E = u_r * math.sin(phi)
            u_N = u_r * math.cos(phi)

            # record the displacements
            rec.uE = u_E
            rec.uN = u_N
            rec.uZ = u_Z

            # estimate the variance base on a 5% deviation from the mean value
            rec.σE = max(0.05*u_E, .01)**2
            rec.σN = max(0.05*u_N, .01)**2
            rec.σZ = max(0.05*u_Z, .01)**2

        # all done
        return data


    def makeTicks(self):
        """
        Generate times and locations for the observations
        """
        # get time
        year = altar.units.time.year.value
        # max time
        tMax =  1 * year
        # build the time value
        for exponent in range(-6,1):
            # compute the time mark
            t = 10**exponent * tMax
            # build the distance
            for r in range(1000, 6000, 1000):
                # assemble the tick mark
                yield (t, r, 0)
        # all done
        return


# bootstrap
if __name__ == "__main__":
    # instantiate
    app = Reverso(name="reverso")
    # invoke
    status = app.run()
    # share
    raise SystemExit(status)


# end of file

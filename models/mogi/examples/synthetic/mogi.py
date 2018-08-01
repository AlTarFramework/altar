#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2018 parasim inc
# (c) 2010-2018 california institute of technology
# all rights reserved
#


# externals
from math import sin, cos, pi as π
# the framework
import altar
# my model
import altar.models.mogi


# app
class Mogi(altar.application, family="altar.applications.mogi"):
    """
    A generator of synthetic data for Mogi sources
    """

    # user configurable state
    x = altar.properties.float(default=0)
    x.doc = "the x coördinate of the Mogi source"

    y = altar.properties.float(default=0)
    y.doc = "the y coördinate of the Mogi source"

    d = altar.properties.float(default=3000)
    d.doc = "the depth of the Mogi source"

    dV = altar.properties.float(default=10e6)
    dV.doc = "the strength of the Mogi source"

    nu = altar.properties.float(default=.25)
    nu.doc = "the Poisson ratio"


    # protocol obligation
    @altar.export
    def main(self, *args, **kwds):
        """
        The main entry point
        """
        # compute the displacements
        data = self.mogi()
        # dump the displacements in a CSV file
        data.write(uri="displacements.csv")
        # all done
        return 0


    # meta-methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # create my stations
        self.stations = self.makeStations()
        # all done
        return


    # implementation details
    def mogi(self):
        """
        Synthesize displacements for a grid of stations given a specific source location and
        strength
        """
        # get the stations
        stations = self.stations
        # dedcue the number of observations
        observations = len(stations)
        # make a source
        source = altar.models.mogi.source(x=self.x, y=self.y, d=self.d, dV=self.dV, nu=self.nu)

        # observe all displacements from the same angle for now
        theta = π/4 # the azimuthal angle
        phi = π     # the polar angle
        # build the common projection vector
        s = sin(theta)*cos(phi), sin(theta)*sin(phi), cos(theta)

        # allocate a matrix to hold the projections
        los = altar.matrix(shape=(observations,3))
        # go through the observations
        for obs in range(observations):
            # store the LOS vector
            los[obs, 0] = s[0]
            los[obs, 1] = s[1]
            los[obs, 2] = s[2]

        # compute the displacements
        u = source.displacements(locations=stations, los=los)

        # prepare the dataset
        # rows: one for each location
        # columns: observation id, u.s, x, y, theta, phi
        # observation id simulates data that come from different sources and therefore require
        # a different offset
        data = altar.models.mogi.data(name="displacements")

        # go through the observation locations
        for idx, (x,y) in enumerate(stations):
            # make a new entry in the data sheet
            observation = data.pyre_new()
            # western stations
            if x < 0:
                # come from a different data set
                observation.oid = 1
            # than
            else:
                # eastern stations
                observation.oid = 0

            # record the location of this observation
            observation.x = x
            observation.y = y

            # project the displacement
            observation.d = u[idx]
            # save the direction of the projection vector
            observation.theta = theta
            observation.phi = phi

        # all done
        return data


    def makeStations(self):
        """
        Create a set of station coordinate
        """
        # get some help
        import itertools
        # build a set of points on a grid
        stations = itertools.product(range(-5,6), range(-5,6))
        # and return it
        return tuple((x*1000, y*1000) for x,y in stations)


# bootstrap
if __name__ == "__main__":
    # instantiate
    app = Mogi(name="mogi")
    # invoke
    status = app.run()
    # share
    raise SystemExit(status)


# end of file

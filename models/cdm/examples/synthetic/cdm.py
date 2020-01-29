#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2020 parasim inc
# (c) 2010-2020 california institute of technology
# all rights reserved
#


# externals
from math import sin, cos, pi as π
# the framework
import altar
# my model
import altar.models.cdm


# app
class CDM(altar.application, family="altar.applications.cdm"):
    """
    A generator of synthetic data for CDM sources
    """

    # user configurable state
    x = altar.properties.float(default=0)
    x.doc = "the x coördinate of the CDM source"

    y = altar.properties.float(default=0)
    y.doc = "the y coördinate of the CDM source"

    d = altar.properties.float(default=3000)
    d.doc = "the depth of the CDM source"

    aX = altar.properties.float(default=400)
    aX.doc = "the x semi-axis length"

    aY = altar.properties.float(default=450)
    aY.doc = "the y semi-axis length"

    aZ = altar.properties.float(default=800)
    aZ.doc = "the z semi-axis length"

    omegaX = altar.properties.float(default=0)
    omegaX.doc = "the CDM rotation about the x axis"

    omegaY = altar.properties.float(default=-45)
    omegaY.doc = "the CDM rotation about the y axis"

    omegaZ = altar.properties.float(default=0)
    omegaZ.doc = "the CDM rotation about the z axis"

    opening = altar.properties.float(default=1e2)
    opening.doc = "the tensile component of the Burgers vector of the dislocation"

    nu = altar.properties.float(default=.25)
    nu.doc = "the Poisson ratio"


    # protocol obligation
    @altar.export
    def main(self, *args, **kwds):
        """
        The main entry point
        """
        # compute the displacements
        data, covariance = self.cdm()
        # dump the displacements in a CSV file
        data.write(uri="displacements.csv")
        # and the covariance in an ascii file
        covariance.save(filename=altar.primitives.path("cd.txt"))
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
    def cdm(self):
        """
        Synthesize displacements for a grid of stations given a specific source location and
        strength
        """
        # get the stations
        stations = self.stations
        # dedcue the number of observations
        observations = len(stations)
        # make a source
        source = altar.models.cdm.source(
            x=self.x, y=self.y, d=self.d,
            ax=self.aX, ay=self.aY, az=self.aZ,
            omegaX=self.omegaX, omegaY=self.omegaY, omegaZ=self.omegaZ,
            opening=self.opening, v=self.nu)

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
        data = altar.models.cdm.data(name="displacements")

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

        # the length of the data sheet is the number of observations
        observations = len(data)
        # allocate a matrix for the data correlation
        correlation = altar.matrix(shape=[observations]*2).zero()

        # go through the observations
        for idx, observation in enumerate(data):
            # set the covariance to a fraction of the "observed" displacement
            correlation[idx,idx] = 1e-4

        # all done
        return data, correlation


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
    app = CDM(name="cdm")
    # invoke
    status = app.run()
    # share
    raise SystemExit(status)


# end of file

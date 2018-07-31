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
import csv
from math import sin, cos
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
        # open a file
        with open("displacements.txt", "w", newline="") as csvfile:
            # create a writer
            writer = csv.writer(csvfile)
            # go through the data
            for record in data:
                # and save them into a file
                writer.writerow(record)
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
        # make a source
        source = altar.models.mogi.source(x=self.x, y=self.y, d=self.d, dV=self.dV, nu=self.nu)
        # compute the displacements
        u = source.displacements(locations=stations)
        # prepare the dataset
        # rows: one for each location
        # columns: observation id, u.s, x, y, theta, phi
        # observation id simulates data that come from different sources and therefore require
        # a different offset
        data = altar.models.mogi.data(name="displacements")

        # go through the observation locations
        for idx, (x,y) in enumerate(stations):
            # make up a observation id
            oid = 0
            # western stations
            if x < 0:
                # get a different id
                oid = 1
            # observe from directly overhead for now
            theta = 0
            phi = 0
            # build the projection vector
            s = sin(theta)*cos(phi), sin(theta)*sin(phi), cos(theta)
            # project the displacement
            d = u[idx,0]*s[0] + u[idx,1]*s[1] + u[idx,2]*s[2]

            # store the data
            data.pyre_append( (oid, d, x, y, theta, phi) )

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

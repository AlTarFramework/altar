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
from math import sqrt, pi as π
# package
import altar
# get the source
from altar.models.mogi import source as mogi


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
        u = self.mogi()
        # and save them into a file
        u.save(filename=altar.primitives.path("displacements.txt"), format="+16.9e")

        # generate the stations file
        # open the file
        with open("stations.txt", "w") as stations:
            # unpack the coordinates
            for x,y in self.stations:
                # write them to the file
                stations.write(f"{x},{y}\n")

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
        # make a source
        source = mogi(x=self.x, y=self.y, d=self.d, dV=self.dV, nu=self.nu)
        # compute the displacements
        u = source.displacements(locations=self.stations)
        # and return them
        return u


    def makeStations(self):
        """
        Create a set of station coordinate
        """
        # get some help
        import itertools
        # build a set of points on a grid
        stations = itertools.product(range(-5,6), range(-5,6))
        # and return it
        return list((x*1000, y*1000) for x,y in stations)


# bootstrap
if __name__ == "__main__":
    # instantiate
    app = Mogi(name="mogi")
    # invoke
    status = app.run()
    # share
    raise SystemExit(status)


# end of file

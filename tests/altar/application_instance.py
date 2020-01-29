#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2020 parasim inc
# (c) 2010-2020 california institute of technology
# all rights reserved
#


def test():
    # get the class
    from altar.shells import application
    # instantiate
    app = application(name="catmip")
    # and publish it
    return app


# bootstrap
if __name__ == "__main__":
    # run the driver
    test()
    # report success
    raise SystemExit(0)


# end of file

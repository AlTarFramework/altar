#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2018 parasim inc
# (c) 2010-2018 california institute of technology
# all rights reserved
#

# bootstrap
if __name__ == "__main__":
    # get the class
    from altar.shells import application
    # instantiate
    app = application(name="catmip")
    # run it
    status = app.run()
    # and share the exit code
    raise SystemExit(status)

# end of file

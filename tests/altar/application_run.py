#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2020 parasim inc
# (c) 2010-2020 california institute of technology
# all rights reserved
#

# bootstrap
if __name__ == "__main__":
    # get the class
    from altar.shells import application
    # instantiate
    app = application(name="catmip")

    # grab the journal
    import journal
    # silence the info channel off
    journal.info("altar").deactivate()

    # run it
    status = app.run()
    # and share the exit code
    raise SystemExit(status)

# end of file

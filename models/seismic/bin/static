#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis (michael.aivazis@para-sim.com)
#
# (c) 2010-2018 california institute of technology
# (c) 2013-2018 parasim inc
# all rights reserved
#

# get the package
import altar
import altar.models.seismic

# make a specialized app that uses this model by default
class Static(altar.shells.application, family='altar.applications.static'):
    """
    A specialized AlTar application that exercises the Linear model
    """

    # user configurable state
    model = altar.models.model(default='linear')
    model.doc = "the Static inversion model"


# bootstrap
if __name__ == "__main__":
    # build an instance of the default app
    app = Static(name="static")
    # invoke the main entry point
    status = app.run()
    # share
    raise SystemExit(status)


# end of file

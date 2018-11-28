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

# make a specialized app that uses this model by default
class Linear(altar.shells.application, family='altar.applications.linear'):
    """
    A specialized AlTar application that exercises the Linear model
    """

    # user configurable state
    model = altar.models.model(default='linear')
    model.doc = "the AlTar model to sample"


# bootstrap
if __name__ == "__main__":
    # build an instance of the default app
    app = Linear(name="linear")
    # invoke the main entry point
    status = app.run()
    # share
    raise SystemExit(status)


# end of file

# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis (michael.aivazis@para-sim.com)
# grace bato           (mary.grace.p.bato@jpl.nasa.gov)
# eric m. gurrola      (eric.m.gurrola@jpl.nasa.gov)
#
# (c) 2013-2020 parasim inc
# (c) 2010-2020 california institute of technology
# all rights reserved


# framework
import altar


# the dataset
class Data(altar.tabular.sheet):
    """
    The layout of the input file
    """


    # the layout
    oid = altar.tabular.int()
    oid.doc = "an integer identifying the data source"

    t = altar.tabular.float()
    t.doc = "the time of the observation"

    x = altar.tabular.float()
    x.doc = "the EW coordinate of the location of the observation"

    y = altar.tabular.float()
    y.doc = "the NS coordinate of the location of the observation"

    uE = altar.tabular.float()
    uE.doc = "the E component of the displacement"

    uN = altar.tabular.float()
    uN.doc = "the N component of the displacement"

    uZ = altar.tabular.float()
    uZ.doc = "the up component of the displacement"

    σE = altar.tabular.float()
    σE.doc = "the σ^2 of the E component of the displacement"

    σN = altar.tabular.float()
    σN.doc = "the σ^2 of the N component of the displacement"

    σZ = altar.tabular.float()
    σZ.doc = "the σ^2 of the up component of the displacement"


    # load data from a csv file
    def read(self, uri):
        """
        Load a data set from a CSV file
        """
        # make a CSV writer
        csv = altar.records.csv()
        # pull data from the file and populate me with immutable records
        self.pyre_immutable(data = csv.read(layout=self, uri=uri))
        # all done
        return self


    # dump my data into a CSV file
    def write(self, uri):
        """
        Save my data into a CSV file
        """
        # make a CSV writer
        csv = altar.records.csv()
        # ask it to save the data
        csv.write(sheet=self, uri=uri)
        # all done
        return self


# end of file

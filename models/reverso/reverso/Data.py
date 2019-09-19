# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2019 parasim inc
# (c) 2010-2019 california institute of technology
# all rights reserved
#


# framework
import altar


# declaration
class Data(altar.tabular.sheet):
    """
    The layout of the input data file
    """

    # the layout
    oid = altar.tabular.int()
    oid.doc = "an integer identifying the data source"

    x = altar.tabular.float()
    x.doc = "the EW coordinate of the location of the source"

    y = altar.tabular.float()
    y.doc = "the NS coordinate of the location of the source"

    d = altar.tabular.float()
    d.doc = "the displacement projected along the line of sight (LOS)"

    theta = altar.tabular.float()
    theta.doc = "the azimuthal angle of the LOS vector to the observing craft"

    phi = altar.tabular.float()
    phi.doc = "the polar angle of the LOS vector to the observing craft"


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

# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2018 parasim inc
# (c) 2010-2018 california institute of technology
# all rights reserved
#


# the package
import altar


# declaration
class Linear(altar.models.bayesian, family="altar.models.linear"):
    """
    """


    # user configurable state
    parameters = altar.properties.int(default=None)
    parameters.doc = "the number of parameters in the model"

    observations = altar.properties.int(default=None)
    observations.doc = "the number of data samples"

    patch = altar.properties.path(default="patch-9")
    patch.doc = "the directory with the input files"

    green = altar.properties.path(default="green.txt")
    green.doc = "the name of the file with the Green functions"

    data = altar.properties.path(default="data.txt")
    data.doc = "the name of the file with the observations"

    cd = altar.properties.path(default="cd.txt")
    cd.doc = "the name of the file with the data covariance matrix"


    # protocol obligations
    @altar.export
    def initialize(self, application):
        """
        Initialize the state of the model given a {problem} specification
        """
        # chain up
        super().initialize(application=application)

        # mount my input data space
        self.ifs = self.mountInputDataspace(pfs=application.pfs)
        # convert the input filenames into data
        self.G, self.d, self.Cd = self.loadInputs()

        # grab a channel
        channel = self.info
        channel.line("run info:")
        # show me the model
        channel.line(f" -- model: {self}")
        # the contents of the data filesystem
        channel.line(f" -- contents of '{self.patch}':")
        channel.line("\n".join(self.ifs.dump(indent=2)))
        # the loaded data
        channel.line(f" -- inputs in memory:")
        channel.line(f"    green functions: {self.G.shape}")
        channel.line(f"       observations: {self.d.shape}")
        channel.line(f"    data covariance: {self.Cd.shape}")
        # flush
        channel.log()

        # all done
        return self


    @altar.export
    def initializeSample(self, step):
        """
        Fill {step.θ} with an initial random sample from my prior distribution.
        """
        # and return
        return self


    @altar.export
    def priorLikelihood(self, step):
        """
        Fill {step.prior} with the likelihoods of the samples in {step.theta} in the prior
        distribution
        """
        print("Linear.priorLikelihood")
        step.print(channel=self.info)
        raise SystemExit(0)
        # all done
        return self


    @altar.export
    def dataLikelihood(self, step):
        """
        Fill {step.data} with the likelihoods of the samples in {step.theta} given the available
        data. This is what is usually referred to as the "forward model"
        """
        print("Linear.dataLikelihood")
        raise SystemExit(0)
        # all done
        return self


    @altar.export
    def verify(self, step, mask):
        """
        Check whether the samples in {step.theta} are consistent with the model requirements and
        update the {mask}, a vector with zeroes for valid samples and non-zero for invalid ones
        """
        # all done; return the rejection map
        return mask


    # implementation details
    def mountInputDataspace(self, pfs):
        """
        Mount the directory with my input files
        """
        # attempt to
        try:
            # mount the directory with my input data
            ifs = altar.filesystem.local(root=self.patch)
        # if it fails
        except altar.filesystem.MountPointError as error:
            # grab my error channel
            channel = self.error
            # complain
            channel.log(f"bad patch name: '{self.patch}'")
            channel.log(str(error))
            # and bail
            raise SystemExit(1)

        # if all goes well, explore it and mount it
        pfs["inputs"] = ifs.discover()
        # all done
        return ifs


    def loadInputs(self):
        """
        Load the data in the input files into memory
        """
        # grab the input dataspace
        ifs = self.ifs

        # first the green functions
        try:
            # get the path to the file
            gf = ifs[self.green]
        # if the file doesn't exist
        except ifs.NotFoundError:
            # grab my error channel
            channel = self.error
            # complain
            channel.log(f"missing Green functions: no '{self.green}' in '{self.patch}'")
            # and raise the exception again
            raise
        # if all goes well
        else:
            # allocate the matrix
            green = altar.matrix(shape=(self.observations, self.parameters))
            # and load the file contents into memory
            green.load(gf.uri)

        # next, the observations
        try:
            # get the path to the file
            df = ifs[self.data]
        # if the file doesn't exist
        except ifs.NotFoundError:
            # grab my error channel
            channel = self.error
            # complain
            channel.log(f"missing observations: no '{self.data}' in '{self.patch}'")
            # and raise the exception again
            raise
        # if all goes well
        else:
            # allocate the vector
            data = altar.vector(shape=self.observations)
            # and load the file contents into memory
            data.load(df.uri)

        # finally, the data covariance
        try:
            # get the path to the file
            cf = ifs[self.cd]
        # if the file doesn't exist
        except ifs.NotFoundError:
            # grab my error channel
            channel = self.error
            # complain
            channel.log(f"missing data covariance matrix: no '{self.cd}' in '{self.patch}'")
            # and raise the exception again
            raise
        # if all goes well
        else:
            # allocate the matrix
            cd = altar.matrix(shape=(self.observations, self.observations))
            # and load the file contents into memory
            cd.load(cf.uri)

        # all done
        return green, data, cd


    # private data
    ifs = None
    G = None # the Green functions
    d = None # the vector with the observations
    Cd = None # the data covariance matrix


# end of file

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
    A model that emulates the probability density for a single observation of the model
    parameters. The observation is treated as normally distributed around a given mean, with a
    covariance constructed out of its eigenvalues and a rotation in configuration
    space. Currently, only two dimensional parameter spaces are supported.
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
        # mount my data space; if anything goes wrong, {mount} doesn't return, so we can assume
        # all is well safely
        self.dfs = self.mount()

        # allocate a matrix for the Green functions
        green = altar.matrix(shape=(self.observations,self.parameters))
        # load the green functions from the input file
        green.load(self.patch / self.green)

        # allocate a vector for the data
        data = altar.vector(shape=self.observations)
        # load the data from the input file
        data.load(self.patch / self.data)

        # allocate a matrix for the data covariance matrix
        cd = altar.matrix(shape=(self.observations,self.observations))
        # load the covariance matrix from the input file
        cd.load(self.patch / self.cd)


        # grab a channel
        channel = self.info
        channel.line("run info:")
        # show me the model
        channel.line(f" -- model: {self}")
        # and the contents of the data filesystem
        channel.line(f" -- contents of '{self.patch}':")
        channel.line("\n".join(self.dfs.dump(indent=4)))
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
        # all done
        return self


    @altar.export
    def verify(self, step):
        """
        Check whether the samples in {step.θ} are consistent with the model requirements and
        return a vector with zeroes for valid samples and ones for the invalid ones
        """
        # all done; return the rejection map
        return [True]


    # implementation details
    def mount(self, **kwds):
        # attempt to
        try:
            # mount the directory with my input data
            dfs = altar.filesystem.local(root=self.patch)
        # if it fails
        except altar.filesystem.MountPointError as error:
            # grab my error channel
            channel = self.error
            # complain
            channel.log(f"bad patch name: '{self.patch}'")
            channel.log(str(error))
            # and bail
            raise SystemExit(1)

        # if all goes well, explore the filesystem and return it
        return dfs.discover()


    # private data
    dfs = None


# end of file

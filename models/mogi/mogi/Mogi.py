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
# the package
import altar


# declaration
class Mogi(altar.models.bayesian, family="altar.models.mogi"):
    """
    An implementation of Mogi[1958]

    The surface displacement calculation for a point pressure source in an elastic half space.

    Currently, {mogi} is implemented as a four parameter model: x,y,depth locate the point
    source, and {dV} provides the point source strength as the volume change. It can easily
    become a five parameter model by including the Poisson ratio of the elastic material to the
    list of free parameters.
    """


    # user configurable state
    parameters = altar.properties.int(default=4)
    parameters.doc = "the number of model degrees of freedom"

    observations = altar.properties.int(default=3*11*11)
    observations.doc = "the number of model degrees of freedom"

    # distributions
    prep = altar.distributions.distribution()
    prep.doc = "the distribution used to generate the initial sample"

    prior = altar.distributions.distribution()
    prior.doc = "the prior distribution"

    # the norm to use for computing the data log likelihood
    norm = altar.norms.norm()
    norm.default = altar.norms.l2()
    norm.doc = "the norm to use when computing the data log likelihood"

    # model specific parameters
    depth = altar.properties.array(default=[0, 60000]) # in SI
    depth.doc = "the allowed range for the depth parameter"

    # the name of the test case
    case = altar.properties.path(default="synthetic")
    case.doc = "the directory with the input files"

    # the file based inputs
    displacements = altar.properties.path(default="displacements.txt")
    displacements.doc = "the name of the file with the displacements"

    stations = altar.properties.path(default="stations.txt")
    stations.doc = "the name of the file with the locations of the observation points"

    # the material properties
    nu = altar.properties.float(default=.25)
    nu.doc = "the Poisson ratio"


    # protocol obligations
    @altar.export
    def initialize(self, application):
        """
        Initialize the state of the model given a {problem} specification
        """
        # chain up
        super().initialize(application=application)
        # get my random number generator
        rng = self.rng

        #  adjust the number of parameters of my distributions
        self.prep.parameters = self.parameters
        self.prior.parameters = self.parameters

        # initialize my distributions
        self.prep.initialize(rng=rng)
        self.prior.initialize(rng=rng)

        # mount my input data space
        self.ifs = self.mountInputDataspace(pfs=application.pfs)
        # convert the input filenames into data
        self.points, self.d = self.loadInputs()
        # compute the normalization
        self.normalization = self.computeNormalization(observations=self.d.shape)

        # make a channel
        channel = self.info
        # show me
        channel.line("run info:")
        # show me the model
        channel.line(f" -- model: {self}")
        # the model state
        channel.line(f" -- model state:")
        channel.line(f"    parameters: {self.parameters}")
        channel.line(f"    observations: {self.observations}")
        # the distributions
        channel.line(f" -- distributions")
        channel.line(f"    prep: {self.prep}")
        channel.line(f"        support: {self.prep.support}")
        channel.line(f"    prior: {self.prior}")
        channel.line(f"        support: {self.prior.support}")
        # the test case name
        channel.line(f" -- case: {self.case}")
        # the contents of the data filesystem
        channel.line(f" -- contents of '{self.case}':")
        channel.line("\n".join(self.ifs.dump(indent=2)))
        # the loaded data
        # the loaded data
        channel.line(f" -- inputs in memory:")
        channel.line(f"    stations: {len(self.points)} locations")
        channel.line(f"    observations: {len(self.d)} displacements")
        # flush
        channel.log()

        # all done
        return self


    @altar.export
    def initializeSample(self, step):
        """
        Fill {step.θ} with an initial random sample from my prior distribution.
        """
        # grab the portion of the sample that's mine
        θ = self.restrict(theta=step.theta)
        # fill it with random numbers from my initializer
        self.prep.initializeSample(theta=θ)
        # and return
        return self


    @altar.export
    def priorLikelihood(self, step):
        """
        Fill {step.prior} with the likelihoods of the samples in {step.theta} in the prior
        distribution
        """
        # grab my prior pdf
        pdf = self.prior
        # grab the portion of the sample that's mine
        θ = self.restrict(theta=step.theta)
        # and the storage for the prior likelihoods
        likelihood = step.prior

        # delegate
        pdf.priorLikelihood(theta=θ, likelihood=likelihood)

        # all done
        return self


    @altar.export
    def dataLikelihood(self, step):
        """
        Fill {step.data} with the likelihoods of the samples in {step.theta} given the available
        data. This is what is usually referred to as the "forward model"
        """
        # get my norm
        norm = self.norm
        # grab the portion of the sample that's mine
        θ = self.restrict(theta=step.theta)
        # the observed displacements
        displacements = self.d
        # the normalization
        normalization = self.normalization
        # and the storage for the data likelihoods
        dataLLK = step.data

        # find out how many samples in the set
        samples = θ.rows

        # for each sample in the sample set
        for sample in range(samples):
            # extract the parameter vector
            parameters = θ.getRow(sample)
            # compute the expected displacement
            u = self.mogi(parameters=parameters)
            # subtract the observed displacements
            u -= displacements
            # compute its norm, normalize, and store it as the data log likelihood
            dataLLK[sample] = normalization - self.norm.eval(v=u)/2

        # all done
        return self


    @altar.export
    def verify(self, step, mask):
        """
        Check whether the samples in {step.theta} are consistent with the model requirements and
        update the {mask}, a vector with zeroes for valid samples and non-zero for invalid ones
        """
        # grab the portion of the sample that's mine
        θ = self.restrict(theta=step.theta)
        # grab my prior
        pdf = self.prior
        # ask it to verify my samples
        pdf.verify(theta=θ, mask=mask)
        # all done; return the rejection map
        return mask


    # implementation details
    def mogi(self, parameters):
        """
        Compute the expected displacements from a point pressure source at the set of observation
        locations
        """
        # unpack the parameters
        x_src, y_src, d_src, dV = parameters
        # the material properties
        nu = self.nu

        # get the list of locations of interest
        locations = self.points

        # allocate space for the result
        u = altar.vector(shape=3*len(locations))
        # go through each observation location
        for index, (x_obs,y_obs) in enumerate(locations):
            # compute displacements
            x = x_src - x_obs
            y = y_src - y_obs
            d = d_src
            # compute the distance to the point source
            x2 = x**2
            y2 = y**2
            d2 = d**2
            # intermediate values
            C = (nu-1) * dV/π
            R = sqrt(x2 + y2 + d2)
            CR3 = C * R**-3
            # pack the expected displacement into the result vector; the packing is done
            # old-style: by multiplying the {location} index by three to make room for the
            # three displacement components
            u[3*index+0], u[3*index+1], u[3*index+2] = x*CR3, y*CR3, -d*CR3

        # all done
        return u


    def mountInputDataspace(self, pfs):
        """
        Mount the directory with my input files
        """
        # attempt to
        try:
            # mount the directory with my input data
            ifs = altar.filesystem.local(root=self.case)
        # if it fails
        except altar.filesystem.MountPointError as error:
            # grab my error channel
            channel = self.error
            # complain
            channel.log(f"bad case name: '{self.case}'")
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

        # first the stations
        try:
            # get the path to the file
            gf = ifs[self.stations]
        # if the file doesn't exist
        except ifs.NotFoundError:
            # grab my error channel
            channel = self.error
            # complain
            channel.log(f"missing station locations: no '{self.stations}' in '{self.case}'")
            # and raise the exception again
            raise
        # if all goes well
        else:
            # prime the locations pile
            points = []
            # open the file
            with gf.open() as stream:
                # grab each line
                for line in stream:
                    # unpack
                    x, y = map(float, line.strip().split(','))
                    # and store
                    points.append((x,y))

        # next, the displacements
        try:
            # get the path to the file
            df = ifs[self.displacements]
        # if the file doesn't exist
        except ifs.NotFoundError:
            # grab my error channel
            channel = self.error
            # complain
            channel.log(f"missing displacements: no '{self.displacements}' in '{self.case}'")
            # and raise the exception again
            raise
        # if all goes well
        else:
            # allocate the vector
            data = altar.vector(shape=self.observations)
            # and load the file contents into memory
            data.load(df.uri)

        # all done
        return points, data


    def computeNormalization(self, observations):
        """
        Compute the normalization of the L2 norm
        """
        # support
        from math import log, pi as π
        # compute and return
        return - log(2*π)*observations / 2;


    # private data
    ifs = None # filesystem with the input data

    # input
    points = None # the list of observation points
    d = None # the matrix of displacements for each control point

# end of file

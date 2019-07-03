# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2019 parasim inc
# (c) 2010-2019 california institute of technology
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

    # my distributions
    prep = altar.distributions.distribution()
    prep.default = altar.distributions.gaussian()
    prep.doc = "the distribution used to generate the initial sample"

    prior = altar.distributions.distribution()
    prior.default = altar.distributions.gaussian()
    prior.doc = "the prior distribution"

    # the norm to use for computing the data log likelihood
    norm = altar.norms.norm()
    norm.default = altar.norms.l2()
    norm.doc = "the norm to use when computing the data log likelihood"

    # the name of the test case
    case = altar.properties.path(default="patch-9")
    case.doc = "the directory with the input files"

    # the file based inputs
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

        # find out how many samples I will be working with; this equal to the number of chains
        samples = application.job.chains

        # get the random number generator; it gets attached to me by the {initialize} method of
        # my superclass
        rng = self.rng
        # and initialize my distributions
        self.prep.initialize(rng=rng)
        self.prior.initialize(rng=rng)

        # mount my input data space
        self.ifs = self.mountInputDataspace(pfs=application.pfs)
        # convert the input filenames into data
        self.G, self.d, self.Cd = self.loadInputs()
        # compute the normalization
        self.normalization = self.computeNormalization(observations=self.d.shape, cd=self.Cd)
        # compute the inverse of {Cd}
        self.Cd_inv = self.computeCovarianceInverse(self.Cd)
        # prepare the residuals matrix
        self.residuals = self.initializeResiduals(samples=samples, data=self.d)

        # grab a channel
        channel = self.debug
        channel.line("run info:")
        # show me the model
        channel.line(f" -- model: {self}")
        # the model state
        channel.line(f" -- model state:")
        channel.line(f"    parameters: {self.parameters}")
        channel.line(f"    observations: {self.observations}")
        # the test case name
        channel.line(f" -- case: {self.case}")
        # the contents of the data filesystem
        channel.line(f" -- contents of '{self.case}':")
        channel.line("\n".join(self.ifs.dump(indent=2)))
        # the loaded data
        channel.line(f" -- inputs in memory:")
        channel.line(f"    green functions: shape={self.G.shape}")
        channel.line(f"    observations: shape={self.d.shape}")
        channel.line(f"    data covariance: shape={self.Cd.shape}")
        # distributions
        channel.line(f" -- distributions:")
        channel.line(f"    prior: {self.prior}")
        channel.line(f"    initializer: {self.prep}")
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

        # fill my portion of the prior likelihood vector
        pdf.priorLikelihood(theta=θ, likelihood=likelihood)

        # all done
        return self


    @altar.export
    def dataLikelihood(self, step):
        """
        Fill {step.data} with the likelihoods of the samples in {step.theta} given the available
        data. This is what is usually referred to as the "forward model"
        """
        # grab the portion of the sample that's mine
        θ = self.restrict(theta=step.theta)
        # the green functions
        G = self.G
        # the observations
        d = self.d
        # the inverse of the data covariance
        Cd_inv = self.Cd_inv
        # the normalization
        normalization = self.normalization
        # and the storage for the data likelihoods
        dataLLK = step.data

        # clone the residuals since the operations that follow write in-place
        residuals = self.residuals.clone()
        # compute G * transpose(θ) - d
        # we must transpose θ because its shape is (samples x parameters)
        # while the shape of G is (observations x parameters)
        residuals = altar.blas.dgemm(G.opNoTrans, θ.opTrans, 1.0, G, θ, -1.0, residuals)
        
        # go through the residual of each sample
        for idx in range(residuals.columns):
            # extract it
            residual = residuals.getColumn(idx)
          
            # compute its norm, normalize, and store it as the data log likelihood
            dataLLK[idx] = normalization - self.norm.eval(v=residual, sigma_inv=Cd_inv)/2
        
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

        # first the green functions
        try:
            # get the path to the file
            gf = ifs[self.green]
        # if the file doesn't exist
        except ifs.NotFoundError:
            # grab my error channel
            channel = self.error
            # complain
            channel.log(f"missing Green functions: no '{self.green}' in '{self.case}'")
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
            channel.log(f"missing observations: no '{self.data}' in '{self.case}'")
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
            channel.log(f"missing data covariance matrix: no '{self.cd}' in '{self.case}'")
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


    def computeCovarianceInverse(self, cd):
        """
        Compute the inverse of the data covariance matrix
        """
        # make a copy so we don't destroy the original
        cd = cd.clone()
        # perform the LU decomposition
        lu = altar.lapack.LU_decomposition(cd)
        # invert; this creates a new matrix
        inv = altar.lapack.LU_invert(*lu)
        # compute the Cholesky decomposition
        inv = altar.lapack.cholesky_decomposition(inv)
        # and return it
        return inv


    def computeNormalization(self, observations, cd):
        """
        Compute the normalization of the L2 norm
        """
        # support
        from math import log, pi as π
        # make a copy of cd
        cd = cd.clone()
        # compute its LU decomposition
        decomposition = altar.lapack.LU_decomposition(cd)
        # use it to compute the log of its determinant
        logdet = altar.lapack.LU_lndet(*decomposition)
        # all done
        return - (log(2*π)*observations + logdet) / 2;


    def initializeResiduals(self, samples, data):
        """
        Prime the matrix that will hold the residuals (G θ - d) for each sample by duplicating the
        observation vector as many times as there are samples
        """
        # allocate the residual matrix
        r = altar.matrix(shape=(data.shape, samples))
        # for each sample
        for sample in range(samples):
            # make the corresponding column a copy of the data vector
            r.setColumn(sample, data)
        # all done
        return r


    # private data
    ifs = None # the filesystem with the input files

    # inputs
    G = None # the Green functions
    d = None # the vector with the observations
    Cd = None # the data covariance matrix

    # computed
    Cd_inv = None # the inverse of the data covariance matrix
    residuals = None # matrix that holds (G θ - d) for each sample
    normalization = 1 # the normalization of the L2 norm


# end of file

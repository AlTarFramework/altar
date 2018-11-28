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
from .ForwardModel import forwardModel as cpuForwardModel
if altar.cuda.WITH_CUDA:
    from .cudaForwardModel import gpuForwardModel,cudaForwardModel

# declaration
class Linear(altar.models.bayesian, family="altar.models.linear"):
    """
    A linear forward model  d = G theta      
    """

    # user configurable state
    # parameter sets and their prior distributions
    parametersets = altar.properties.dict(schema=altar.models.parameters())
    parametersets.doc = "the set of parameters in the model" 
    
    parameters = altar.properties.int(default=None)
    parameters.doc = "total number of parameters in the model"

    observations = altar.properties.int(default=None)
    observations.doc = "the number of data samples"


    # the norm to use for computing the data log likelihood
    norm = altar.norms.norm()
    norm.default = altar.norms.l2()
    norm.doc = "the norm to use when computing the data log likelihood"

    # the name of the test case
    case = altar.properties.path(default="patch-9")
    case.doc = "the directory with the input files"

    # the file based inputs
    green_file = altar.properties.path(default="green.txt")
    green_file.doc = "the name of the file with the Green functions"

    data_file = altar.properties.path(default="data.txt")
    data_file.doc = "the name of the file with the observations"

    cd_file = altar.properties.path(default="cd.txt")
    cd_file.doc = "the name of the file with the data covariance matrix"

    # output 
    output_path = altar.properties.path(default="results")
    

    # protocol obligations
    @altar.export
    def initialize(self, application):
        """
        Initialize the state of the model given a {problem} specification
        """
        # chain up
        super().initialize(application=application)
        
        if application.job.gpus > 0:
            self.processor = 'gpu'
            
        # find out how many samples I will be working with; this equal to the number of chains
        samples = application.job.chains

        # get the random number generator; it gets attached to me by the {initialize} method of
        # my superclass
        # rng = self.rng
        
        # initialize the parameter sets and their priors 
        self.initializeParameterSets()

        # mount my input data space
        self.ifs = self.mountInputDataspace(pfs=application.pfs)
        
        # convert the input filenames into data
        self.G, self.d, self.Cd = self.loadInputs()
        
        # initialize covariance and merge it to data and green's function
        self.initializeCovariance(samples=samples)

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
        #channel.line(f" -- parametersets:")
        #channel.line(f"    prior: {self.prior}")
        #channel.line(f"    initializer: {self.prep}")
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
        for pset in self.parametersets.values():
            # and ask each one to {prep} the sample
            pset.initializeSample(theta=θ)
        # and return
        return self


    @altar.export
    def computePrior(self, step):
        """
        Fill {step.prior} with the densities of the samples in {step.theta} in the prior
        distribution
        """
        
        # grab the portion of the sample that's mine
        θ = self.restrict(theta=step.theta)
        # and the storage for the prior densities
        prior = step.prior

        # go through each parameter set
        for pset in self.parametersets.values():
            # and ask each one to {prep} the sample
            pset.computePrior(theta=θ, density=prior)

        # all done
        return self


    @altar.export
    def computeDataLikelihood(self, step):
        """
        Fill {step.data} with the densities of the samples in {step.theta} given the available
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
        # and the storage for the data densities
        dataLLK = step.data

        # clone the residuals since the operations that follow write in-place
        residuals = self.residuals.clone()
        # compute G * transpose(θ) - d
        # we must transpose θ because its shape is (samples x parameters)
        # while the shape of G is (observations x parameters)
        
        if self.processor == 'gpu':
            residuals = gpuForwardModel(theta=θ, green=self.G, data_observations=self.residuals) 
        else:
            residuals = cpuForwardModel(theta=θ, green=self.G, data_observations=self.residuals) 

        # go through the residual of each sample
        for idx in range(residuals.columns):
            # extract it
            residual = residuals.getColumn(idx)
            # compute its norm, normalize, and store it as the data log likelihood
            # dataLLK[idx] = normalization - self.norm.eval(v=residual, sigma_inv=Cd_inv)/2
            dataLLK[idx] = normalization - 0.5*self.norm.eval(v=residual)   
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
        # pdf = self.prior
        # ask it to verify my samples
        # pdf.verify(theta=θ, mask=mask)

        # use pset verify instead
        # go through each parameter set
        for pset in self.parametersets.values():
            # and ask each one to verify the sample
            pset.verify(theta=θ, mask=mask)
        # all done; return the rejection map
        return mask

        # all done; return the rejection map
        return mask

    # implementation details
    def initializeParameterSets(self):
        """
        Initialize the parameter set
        """
        # get the parameter sets
        psets = self.parametersets
        # initialize the offset
        parameters = 0
        # go through my parameter sets
        for name, pset in psets.items():
            # initialize the parameter set
            parameters += pset.initialize(model=self, offset=pset.offset)
        # the total number of parameters is now known, so record it
        self.parameters = parameters

        # all done
        return


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
            gf = ifs[self.green_file]
        # if the file doesn't exist
        except ifs.NotFoundError:
            # grab my error channel
            channel = self.error
            # complain
            channel.log(f"missing Green functions: no '{self.green_file}' in '{self.case}'")
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
            df = ifs[self.data_file]
        # if the file doesn't exist
        except ifs.NotFoundError:
            # grab my error channel
            channel = self.error
            # complain
            channel.log(f"missing observations: no '{self.data_file}' in '{self.case}'")
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
            cf = ifs[self.cd_file]
        # if the file doesn't exist
        except ifs.NotFoundError:
            # grab my error channel
            channel = self.error
            # complain
            channel.log(f"missing data covariance matrix: no '{self.cd_file}' in '{self.case}'")
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

    def initializeCovariance(self, samples):
        """
        Compute the Cholesky decomposition of the inverse of the data covariance
        and merge it to data
        """
        # compute the normalization
        self.normalization = self.computeNormalization(observations=self.observations, cd=self.Cd)
        # compute the inverse of {Cd}
        self.Cd_inv = self.computeCovarianceInverse(self.Cd)
        # merge Cd to green and d
        # G = Cd_inv x G; d = Cd_inv x d
        Cd_inv = self.Cd_inv
        self.G = altar.blas.dtrmm(Cd_inv.sideLeft, Cd_inv.upperTriangular, Cd_inv.opNoTrans,
            Cd_inv.nonUnitDiagonal, 1, Cd_inv, self.G)
        self.d = altar.blas.dtrmv( Cd_inv.upperTriangular, Cd_inv.opNoTrans, Cd_inv.nonUnitDiagonal,
            Cd_inv, self.d)
        # prepare the residuals matrix
        self.residuals = self.initializeResiduals(samples=samples, data=self.d)
        # all done 
        return self
        

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

    @altar.export
    def update(self, annealer):
        """
        Model updating at the bottom of each annealing step
        Output step data
        """
        # get current worker
        worker = annealer.worker
        # check master
        if worker.rank == worker.manager:
            altar.utils.save_step(step=worker.step, path=self.output_path)
        # all done    
        return self
    

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

    # forwardModel method
    processor = 'cpu'

# end of file

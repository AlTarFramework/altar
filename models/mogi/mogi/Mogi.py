# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2020 parasim inc
# (c) 2010-2020 california institute of technology
# all rights reserved
#


# externals
import csv
# the package
import altar
# the encapsulation of the layout of the data in a file
from .Data import Data as datasheet


# declaration
class Mogi(altar.models.bayesian, family="altar.models.mogi"):
    """
    An implementation of Mogi[1958]

    The surface displacement calculation for a pressure point source in an elastic half space.

    Currently, {mogi} is implemented as a four parameter model: x,y,depth locate the point
    source, and {dV} provides the point source strength as the volume change. It can easily
    become a five parameter model by including the Poisson ratio of the elastic material to the
    list of free parameters.
    """


    # user configurable state
    # parameters
    psets = altar.properties.dict(schema=altar.models.parameters())
    psets.doc = "the model parameter meta-data"

    # data
    observations = altar.properties.int()
    observations.doc = "the number of model degrees of freedom"

    # the norm to use for computing the data log likelihood
    norm = altar.norms.norm()
    norm.default = altar.norms.l2()
    norm.doc = "the norm to use when computing the data log likelihood"

    # the name of the test case
    case = altar.properties.path(default="synthetic")
    case.doc = "the directory with the input files"

    # the file based inputs
    displacements = altar.properties.path(default="displacements.csv")
    displacements.doc = "the name of the file with the displacements"

    covariance = altar.properties.path(default="cd.txt")
    covariance.doc = "the name of the file with the data covariance"

    # the material properties
    nu = altar.properties.float(default=.25)
    nu.doc = "the Poisson ratio"

    # operating strategies
    mode = altar.properties.str(default="fast")
    mode.doc = "the implementation strategy"
    mode.validators = altar.constraints.isMember("native", "fast")

    # public data
    parameters = 0 # adjusted during model initialization
    strategy = None # the strategy for computing the data log likelihood


    # protocol obligations
    @altar.export
    def initialize(self, application):
        """
        Initialize the state of the model given a {problem} specification
        """
        # externals
        from math import sin, cos

        # chain up
        super().initialize(application=application)

        # initialize my parameter sets
        self.initializeParameterSets()
        # mount the directory with my input data
        self.ifs = self.mountInputDataspace(pfs=application.pfs)

        # load the data from the inputs into memory
        displacements, self.cd = self.loadInputs()

        # compute the normalization
        self.normalization = self.computeNormalization()
        # compute the inverse of the covariance matrix
        self.cd_inv = self.computeCovarianceInverse()

        # build the local representations
        self.points = []
        self.d = altar.vector(shape=self.observations)
        self.los = altar.matrix(shape=(self.observations,3))
        self.oid = []
        # populate them
        for obs, record in enumerate(displacements):
            # extract the observation id
            self.oid.append( record.oid )
            # extract the (x,y) coordinate of the observation point
            self.points.append( (record.x, record.y) )
            # extract the observed displacement
            self.d[obs] = record.d
            # get the LOS angles
            theta = record.theta
            phi = record.phi
            # form the projection vectors and store them
            self.los[obs, 0] = sin(theta) * cos(phi)
            self.los[obs, 1] = sin(theta) * sin(phi)
            self.los[obs, 2] = cos(theta)

        # save the parameter meta data
        self.meta()

        # pick an implementation strategy
        # if the user has asked for CUDA support
        if application.job.gpus > 0:
            # attempt to
            try:
                # use the CUDA implementation
                from .CUDA import CUDA as strategy
            # if this fails
            except ImportError:
                # make a channel
                channel = application.error
                # complain
                raise channel.log("unable to find CUDA support")
        # if the user specified {fast} mode
        elif self.mode == "fast":
            # attempt to
            try:
                # get the fast strategy that involves a Mogi source implemented in C++
                from .Fast import Fast as strategy
            # if this fails
            except ImportError:
                # make channel
                channel = application.error
                # complain
                raise channel.log("unable to find support for <fast> mode")
        # otherwise
        else:
            # get the strategy implemented in pure python
            from .Native import Native as strategy
        # initialize it and save it
        self.strategy = strategy().initialize(application=application, model=self)

        # show me
        # self.show(job=application.job, channel=self.info)

        # all done
        return self


    @altar.export
    def initializeSample(self, step):
        """
        Fill {step.θ} with an initial random sample from my prior distribution.
        """
        # grab the portion of the sample that's mine
        θ = self.restrict(theta=step.theta)
        # go through each parameter set
        for pset in self.psets.values():
            # and ask each one to {prep} the sample
            pset.initializeSample(theta=θ)
        # and return
        return self


    @altar.export
    def priorLikelihood(self, step):
        """
        Fill {step.prior} with the likelihoods of the samples in {step.theta} in the prior
        distribution
        """
        # grab the portion of the sample that's mine
        θ = self.restrict(theta=step.theta)
        # and the storage for the prior likelihoods
        likelihood = step.prior
        # go through each parameter set
        for pset in self.psets.values():
            # and ask each one to {prep} the sample
            pset.priorLikelihood(theta=θ, priorLLK=likelihood)
        # all done
        return self


    @altar.export
    def dataLikelihood(self, step):
        """
        Fill {step.data} with the likelihoods of the samples in {step.theta} given the available
        data. This is what is usually referred to as the "forward model"
        """
        # get my strategy
        strategy = self.strategy
        # deploy
        strategy.dataLikelihood(model=self, step=step)
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
        # go through each parameter set
        for pset in self.psets.values():
            # and ask each one to verify the sample
            pset.verify(theta=θ, mask=mask)
        # all done; return the rejection map
        return mask


    # implementation details
    def initializeParameterSets(self):
        """
        Initialize my parameter sets
        """
        # compile the parameter layout
        # get the parameter sets
        psets = self.psets
        # initialize the offset
        offset = 0
        # go through my parameter sets
        for name, pset in psets.items():
            # initialize the parameter set
            offset += pset.initialize(model=self, offset=offset)
        # the total number of parameters is now known, so record it
        self.parameters = offset

        # record the layout of the sample vector
        self.xIdx = psets["location"].offset
        self.yIdx = self.xIdx + 1
        self.dIdx = psets["depth"].offset
        self.sIdx = psets["source"].offset
        self.offsetIdx = psets["offsets"].offset

        # all done
        return


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

        # get the displacement data
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

        # if all goes well, create a data sheet
        data = datasheet(name="displacements")
        # and populate it
        data.read(uri=df.uri)

        # adjust the number of observations
        self.observations = len(data)

        # finally, try to
        try:
            # get the file node with the data covariance
            node = ifs[self.covariance]
        # if the file doesn't exist
        except ifs.NotFoundError:
            # grab my error channel
            channel = self.error
            # complain
            channel.log(f"missing data covariance matrix: no '{self.covariance}' in '{self.case}'")
            # and re-raise the exception
            raise
        # if all goes well
        else:
            # allocate the matrix
            covariance = altar.matrix(shape=[self.observations]*2)
            # and load the contents into memory
            covariance.load(node.uri)

        # all done
        return data, covariance


    def computeNormalization(self):
        """
        Compute the normalization of the L2 norm
        """
        # support
        from math import log, pi as π
        # make a copy of my data covariance
        cd = self.cd.clone()
        # perform an LU decomposition
        lu = altar.lapack.LU_decomposition(cd)
        # use it to compute the log of its determinant
        lndet = altar.lapack.LU_lndet(*lu)
        # compute and return
        return - 0.5 * (log(2*π)*self.observations + lndet);


    def computeCovarianceInverse(self):
        """
        Compute the inverse of my data covariance
        """
        # make a copy of the covariance matrix
        cd = self.cd.clone()
        # perform an LU decomposition
        lu = altar.lapack.LU_decomposition(cd)
        # invert it
        inverse = altar.lapack.LU_invert(*lu)
        # and compute the Cholesky decomposition of the inverse
        chol = altar.lapack.cholesky_decomposition(inverse)
        # all done
        return chol


    def meta(self):
        """
        Persist the sample layout by recording the parameter set metadata
        """
        # open the output file
        with open("parameters.csv", mode="w", newline='') as stream:
            # make a csv writer
            writer = csv.writer(stream)

            # the headers
            headers = ["name", "count", "offset"]
            # save them
            writer.writerow(headers)

            # go through the parameter sets
            for name, pset in self.psets.items():
                # unpack
                meta = name, pset.count, pset.offset
                # record
                writer.writerow(meta)

        # all done
        return self


    def show(self, job, channel):
        """
        Place model information in the supplied {channel}
        """
        # show me
        channel.line("run info:")
        # job
        channel.line(f" -- job: {job}")
        channel.line(f"    hosts: {job.hosts}")
        channel.line(f"    tasks: {job.tasks}")
        channel.line(f"    gpus: {job.gpus}")
        channel.line(f"    chains: {job.chains}")
        # show me the model
        channel.line(f" -- model: {self}")
        # the model state
        channel.line(f"    observations: {self.observations}")
        # the parameter sets
        channel.line(f"    parameters: {self.parameters} total, in {len(self.psets)} sets")

        # go through the parameter sets
        for name, pset in self.psets.items():
            # and show me what we know about them
            channel.line(f"      {name}:")
            channel.line(f"        offset: {pset.offset}:")
            channel.line(f"         count: {pset.count}:")
            channel.line(f"         prior: {pset.prior}:")
            channel.line(f"          prep: {pset.prep}:")

        # the test case name
        channel.line(f" -- case: {self.case}")
        # the contents of the data filesystem
        channel.line(f" -- contents of '{self.case}':")
        channel.line("\n".join(self.ifs.dump(indent=2)))
        # the loaded data
        # the loaded data
        channel.line(f" -- inputs in memory:")
        channel.line(f"    observations: {len(self.d)} displacements")
        channel.line(f"    covariance: {self.cd.shape}")
        # flush
        channel.log()

        # all done
        return self


    # private data
    ifs = None # filesystem with the input data

    # input
    d = None # the vector of displacements for each control point
    los = None # the list of LOS vectors for each observation
    oid = None # dataset id that each observation belongs to; tied to the {offset} parameter set
    points = None # the list of observation points
    cd = None # the data covariance matrix

    # the sample layout; patched during {initialize}
    xIdx = 0
    yIdx = 0
    dIdx = 0
    sIdx = 0
    offsetIdx = 0

    # computed
    cd_inv = None # the inverse of my data covariance matrix
    normalization = 1 # the normalization of the L2 norm


# end of file

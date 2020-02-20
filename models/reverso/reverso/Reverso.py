# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis (michael.aivazis@para-sim.com)
# grace bato           (mary.grace.p.bato@jpl.nasa.gov)
# eric m. gurrola      (eric.m.gurrola@jpl.nasa.gov)
#
# (c) 2013-2020 parasim inc
# (c) 2010-2020 california institute of technology
# all rights reserved


# externals
import csv
# framework
import altar
# the encapsulation of the layout of the data
from .Data import Data as datasheet


# model declaration
class Reverso(altar.models.bayesian, family="altar.models.reverso"):
    """
    An implementation of the Reverso 2-Magma Chamber Volcano Model, Reverso et al. [2014]
    """


    # user configurable state
    # the workspace name
    case = altar.properties.path(default="synthetic")
    case.doc = "the directory with the input files; output will be placed here as well"

    # the computational strategy to use
    mode = altar.properties.str(default="analytic")
    mode.doc = "the implementation strategy"
    mode.validators = altar.constraints.isMember("analytic")

    # the norm to use for computing the data log likelihood
    norm = altar.norms.norm()
    norm.default = altar.norms.l2()
    norm.doc = "the norm to use when computing the data log likelihood"

    # model parameters; the layout is dynamic and specified in the configuration file
    psets = altar.properties.dict(schema=altar.models.parameters())
    psets.doc = "the model parameter layout specification"

    # the file based inputs
    displacements = altar.properties.path(default="displacements.csv")
    displacements.doc = "the name of the file with the displacements"

    # material parameters
    Qin = altar.properties.float(default=0.6)
    Qin.doc = "basal magma inflow rate"

    # physical parameters
    G = altar.properties.float(default=20.0E9)
    G.doc = "shear modulus, [Pa, kg-m/s**2]"

    v = altar.properties.float(default=0.25)
    v.doc = "Poisson's ratio"

    mu = altar.properties.float(default=2000.0)
    mu.doc = "viscosity [Pa-s]"

    drho = altar.properties.float(default=300.0)
    drho.doc = "density difference (ρ_r-ρ_m), [kg/m**3]"

    g = altar.properties.float(default=9.81)
    g.doc = "gravitational acceleration [m/s**2]"

    # public data
    observations = 0  # the number of data points
    parameters = 0    # adjusted during model initialization
    strategy = None   # the engine that computes the data log likelihood; based on "mode" above


    # framework obligations
    @altar.export
    def initialize(self, application):
        """
        Initialize the state of the model given a problem specification
        """
        # chain up
        super().initialize(application=application)
        # initialize the parameter sets
        self.initializeParameterSets()
        # mount the workspace
        self.ifs = self.mountInputDataspace(pfs=application.pfs)

        # load the data
        data = self.loadInputs()

        # prep to swallow the inputs
        self.ticks = []
        self.d = altar.vector(shape=(3*self.observations))
        self.cd = altar.matrix(shape=(3*self.observations, 3*self.observations)).zero()

        # go through the data records
        for idx, rec in enumerate(data):
            # save the (t,x,y) triplet
            self.ticks.append( (rec.t, rec.x, rec.y) )
            # save the three components of the displacements
            self.d[3*idx + 0] = rec.uE
            self.d[3*idx + 1] = rec.uN
            self.d[3*idx + 2] = rec.uZ
            # populate the covariance matrix
            self.cd[3*idx+0, 3*idx+0] = rec.σE
            self.cd[3*idx+1, 3*idx+1] = rec.σN
            self.cd[3*idx+2, 3*idx+2] = rec.σZ

        # compute the normalization
        self.normalization = self.computeNormalization()
        # compute the inverse of the covariance matrix
        self.cd_inv = self.computeCovarianceInverse()

        # save the parameter meta data
        self.meta()

        # pick an implementation strategy
        # if the user specified {fast} mode
        if self.mode == "fast":
            # attempt to
            try:
                # get the fast strategy that involves a CDM source implemented in C++
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
            # and ask each one to compute the prior of the sample
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
        # transfer the offsets of the various slots to members
        self.HsIdx = psets["H_s"].offset
        self.HdIdx = psets["H_d"].offset
        self.asIdx = psets["a_s"].offset
        self.adIdx = psets["a_d"].offset
        self.acIdx = psets["a_c"].offset

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

        # all done
        return data


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
        channel.line(f"    observations: {self.d.shape} displacements")
        channel.line(f"    covariance: {self.cd.shape}")
        # flush
        channel.log()

        # all done
        return self


    # private data
    # the sample layout; patched during {initialize}
    Hs_idx = 0
    Hd_idx = 0
    as_idx = 0
    ad_idx = 0
    ac_idx = 0

    # input
    ticks = None # the list of observation points
    d = None # the vector of displacements for each observation
    cd = None # the data covariance matrix

    # computed
    cd_inv = None # the inverse of my data covariance matrix
    normalization = 1 # the normalization of the L2 norm

    # administrative
    ifs = None


# end of file

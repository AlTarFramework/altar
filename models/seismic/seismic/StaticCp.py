# -*- python -*-
# -*- coding: utf-8 -*-
#
# Lijun Zhu
# Caltech
#
# (c) 2013-2018 parasim inc
# (c) 2010-2018 california institute of technology
# all rights reserved
#


# the package
import altar
from .Static import Static as static

# declaration
class StaticCp(static, family="altar.models.staticCp"):
    """
    Linear Model with prediction uncertainty Cp, in addition to data uncertainty Cd 
    Cp = Kp Cmu Kp^T 
    Kp = Kmu * <θ>    
    Kp.shape = (observations, nCmu) 
    Cmu.shape = (nCmu, nCmu)
    Kmu.shape =(observations, parameters) (same as the green's function)
    """
    
    # implementation notes
    # we keep Cd as Cd0, data observation as d0 
    # after each beta step, we calculate Cp from the mean model
    # Cd = Cd0 + Cp
    # Cd_inv 
    

    # The properties in super class - Linear Model are included

    # extra properties for Cp 
    # mu is named after shear modulus, but is used for general model parameters
    nCmu = altar.properties.int(default=0)
    nCmu.doc = "the number of model parameter sets"

    cmu_file = altar.properties.path(default="cmu.txt")
    cmu_file.doc = "the covariance describing the uncertainty of model parameter"
    
    # kmu are a set (nCmu) of derivations of Green's functions shape=(observations, parameters)
    kmu_file = altar.properties.str(default="kmu[n].txt")
    kmu_file.doc = "the sensitity kernel of model parameter: input as kmu1.txt, ..."
    
    # initial model 
    initialModel_file = altar.properties.str(default="init_model.txt")
    initialModel_file.doc = "the initial mean model"


    # protocol obligations
    @altar.export
    def initialize(self, application):
        """
        Initialize the state of the model given a {problem} specification
        """
        # chain up
        super().initialize(application=application)

        # convert the input filenames into data
        self.Kmu, self.Cmu, self.meanModel = self.loadInputsCp()
        # set Cp 
        self.Cp = self.computeCp(theta_mean=self.meanModel) 

        # all done
        return self



    def loadInputsCp(self):
        """
        Load the additional data (for Cp problem) in the input files into memory
        """
        # grab the input dataspace
        ifs = self.ifs
            
        # the covariance/uncertainty for model parameter Cmu
        try:
            # get the path to the file
            cmuf = ifs[self.cmu_file]
        # if the file doesn't exist
        except ifs.NotFoundError:
            # grab my error channel
            channel = self.error
            # complain
            channel.log(f"missing data covariance matrix: no '{self.cmu_file}' in '{self.case}'")
            # and raise the exception again
            raise
        # if all goes well
        else:
            # allocate the matrix
            cmu = altar.matrix(shape=(self.nCmu, self.nCmu))
            # and load the file contents into memory
            cmu.load(cmuf.uri)    
            
        # the sensitivity kernel, Kmu ususally
        nCmu = self.nCmu 
        prefix, suffix = self.kmu_file.split("[n]")
        kmu =[]
        kmu_i = altar.matrix(shape=(self.observations, self.parameters))
        for i in range (nCmu):
            kmufn = prefix+str(i+1)+suffix
            try:
                kmuf = ifs[kmufn]
            except ifs.NotFoundErr:
                channel.log(f"missing sensitivity kernel: no '{kmufn}' in '{self.case}'")
                raise
            else:
                kmu_i.load(kmuf.uri)
                kmu.append(kmu_i)
                
        
        # the initial model
        try:
            # get the path to the file
            initModelf = ifs[self.initialModel_file]
        # if the file doesn't exist
        except ifs.NotFoundError:
            channel.log(f"missing initial model file: no '{initModelf}' in '{self.case}'")
            raise
        # if all goes well
        else:
            # and load the file contents into memory
            initModel = altar.vector(shape=self.parameters)
            initModel.load(initModelf.uri)    
        

        # all done
        return kmu, cmu, initModel

    #Cp - related functions 

    def initializeCovariance(self, samples):
        """
        initialize data covariance related variables
        """
        # make copies of the original Cd, data_obs, green
        self.Cd0 = self.Cd.clone()
        self.d0 = self.d.clone() 
        self.G0 = self.G.clone()
        
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


    def computeCp(self, theta_mean):
        """
        Calculate Cp 
        """
        
        # grab the samples  shape=(samples, parameters) 
        parameters = self.parameters
        observations = self.observations
        nCmu = self.nCmu
            
        Cp = altar.matrix(shape=(observations, observations))
        
        # calculate 
        kv = altar.vector(shape=observations)
        cmu = self.Cmu
        kmu = self.Kmu
        Kp = altar.matrix(shape=(observations, nCmu))
        for i in range(nCmu):
            # get kmu_i from list, shape=(observations, parameters)
            kmu_i = kmu[i]
            #  kv = Kmu_i * thetha_mean
            # dgemv y = alpha Op(A) x + beta y   
            altar.blas.dgemv(kmu_i.opNoTrans, 1.0, kmu_i, theta_mean, 0.0, kv)
            Kp.setColumn(i, kv)
        
        # KpC = Kp * Cmu
        KpC = altar.matrix(shape=(observations, nCmu))
        altar.blas.dsymm(cmu.sideRight, cmu.upperTriangular, 1.0, cmu, Kp, 0.0, KpC)
        # Cp = KpC*Kp
        altar.blas.dgemm(KpC.opNoTrans, Kp.opTrans, 1.0, KpC, Kp, 0.0, Cp)

        # all done                  
        return Cp     


    @altar.export
    def update(self, annealer):
        """
        Model update interface
        """
        super().update(annealer=annealer)
        
        # get the work samples 
        step = annealer.worker.step 
        θ = self.restrict(theta=step.theta)
        
        # calculate the mean model 
        theta_mean = self.meanModel
        for i in range(self.parameters):
            param_v = θ.getColumn(i)
            param_mean = param_v.mean()
            theta_mean[i] = param_mean
        
        # compute Cp from the mean model 
        self.Cp = self.computeCp(theta_mean = theta_mean)
        
        # update Cd
        self.Cd.copy(self.Cd0)
        self.Cd += self.Cp

        # compute the normalization
        self.normalization = self.computeNormalization(observations=self.observations, cd=self.Cd)

        # compute the inverse of {Cd}
        self.Cd_inv = self.computeCovarianceInverse(self.Cd)
        
        # merge Cd to green and d
        # G = Cd_inv x G; d = Cd_inv x d
        Cd_inv = self.Cd_inv
        self.G.copy(self.G0)
        self.G = altar.blas.dtrmm(Cd_inv.sideLeft, Cd_inv.upperTriangular, Cd_inv.opNoTrans,
            Cd_inv.nonUnitDiagonal, 1, Cd_inv, self.G)
        self.d.copy(self.d0)
        self.d = altar.blas.dtrmv( Cd_inv.upperTriangular, Cd_inv.opNoTrans, Cd_inv.nonUnitDiagonal,
            Cd_inv, self.d)    
            
        # prepare the residuals matrix
        samples = step.samples
        self.residuals = self.initializeResiduals(samples=samples, data=self.d)
        
        # recalculate densities
        # self.densities(annealer=annealer, step=step)
        #all done
        return self

    # inputs
    G0 = None # the original Green functions
    d0 = None # the vector with the original observations
    Cd0 = None # the original data covariance matrix
    Cmu = None # the covariance of sensitivity kernel
    Kmu = None # the sensitivity kernel

    # computed
    Cp = None # the covariance matrix associated with model uncertainty
    meanModel = None

# end of file

# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2020 parasim inc
# (c) 2010-2020 california institute of technology
# all rights reserved
#


# the package
import altar
# my protocol
from .Monitor import Monitor as monitor


# an implementation of the monitor protocol
class Reporter(altar.component, family="altar.simulations.monitors.reporter", implements=monitor):
    """
    Reporter reports simulation progress by using application journal channels
    """


    # protocol obligations
    @altar.export
    def initialize(self, application):
        """
        Initialize me given an {application} context
        """
        # nothing to do
        return self


    # implementation details
    def simulationStart(self, controller, **kwds):
        """
        Handler invoked when the simulation is about to start
        """
        # grab a channel
        channel = controller.info
        # say something
        channel.log(f"{self.pyre_name}: start")
        # all done
        return


    def samplePosteriorStart(self, controller, **kwds):
        """
        Handler invoked at the beginning of sampling the posterior
        """
        # grab a channel
        channel = controller.info
        # say something
        channel.log(f"{self.pyre_name}: samplePosteriorStart")
        # all done
        return


    def prepareSamplingPDFStart(self, controller, **kwds):
        """
        Handler invoked at the beginning of the preparation of the sampling PDF
        """
        # grab a channel
        channel = controller.info
        # say something
        channel.log(f"{self.pyre_name}: prepareSamplingPDFStart")
        # all done
        return


    def prepareSamplingPDFFinish(self, controller, **kwds):
        """
        Handler invoked at the end of the preparation of the sampling PDF
        """
        # grab a channel
        channel = controller.info
        # say something
        channel.log(f"{self.pyre_name}: prepareSamplingPDFFinish")
        # all done
        return


    def betaStart(self, controller, **kwds):
        """
        Handler invoked at the beginning of the beta step
        """
        # grab a channel
        channel = controller.info
        # say something
        channel.log(f"{self.pyre_name}: betaStart")
        # all done
        return


    def walkChainsStart(self, controller, **kwds):
        """
        Handler invoked at the beginning of the chain walk
        """
        # grab a channel
        channel = controller.info
        # say something
        channel.log(f"{self.pyre_name}: walkChainsStart")
        # all done
        return


    def chainAdvanceStart(self, controller, **kwds):
        """
        Handler invoked at the beginning of a single step of chain walking
        """
        # grab a channel
        channel = controller.info
        # say something
        channel.log(f"{self.pyre_name}: chainAdvanceStart")
        # all done
        return


    def chainAdvanceFinish(self, controller, **kwds):
        """
        Handler invoked at the end of a single step of chain walking
        """
        # grab a channel
        channel = controller.info
        # say something
        channel.log(f"{self.pyre_name}: chainAdvanceFinish")
        # all done
        return


    def verifyStart(self, controller, **kwds):
        """
        Handler invoked before we start verifying the generated sample
        """
        # grab a channel
        channel = controller.info
        # say something
        channel.log(f"{self.pyre_name}: verifyStart")
        # all done
        return


    def verifyFinish(self, controller, **kwds):
        """
        Handler invoked after we are done verifying the generated sample
        """
        # grab a channel
        channel = controller.info
        # say something
        channel.log(f"{self.pyre_name}: verifyFinish")
        # all done
        return


    def priorStart(self, controller, **kwds):
        """
        Handler invoked before we compute the prior
        """
        # grab a channel
        channel = controller.info
        # say something
        channel.log(f"{self.pyre_name}: priorStart")
        # all done
        return


    def priorFinish(self, controller, **kwds):
        """
        Handler invoked after we compute the prior
        """
        # grab a channel
        channel = controller.info
        # say something
        channel.log(f"{self.pyre_name}: priorFinish")
        # all done
        return


    def dataStart(self, controller, **kwds):
        """
        Handler invoked before we compute the data likelihood
        """
        # grab a channel
        channel = controller.info
        # say something
        channel.log(f"{self.pyre_name}: dataStart")
        # all done
        return


    def dataFinish(self, controller, **kwds):
        """
        Handler invoked after we compute the data likelihood
        """
        # grab a channel
        channel = controller.info
        # say something
        channel.log(f"{self.pyre_name}: dataFinish")
        # all done
        return


    def posteriorStart(self, controller, **kwds):
        """
        Handler invoked before we assemble the posterior
        """
        # grab a channel
        channel = controller.info
        # say something
        channel.log(f"{self.pyre_name}: posteriorStart")
        # all done
        return


    def posteriorFinish(self, controller, **kwds):
        """
        Handler invoked after we assemble the posterior
        """
        # grab a channel
        channel = controller.info
        # say something
        channel.log(f"{self.pyre_name}: posteriorFinish")
        # all done
        return


    def acceptStart(self, controller, **kwds):
        """
        Handler invoked at the beginning of sample accept/reject
        """
        # grab a channel
        channel = controller.info
        # say something
        channel.log(f"{self.pyre_name}: acceptStart")
        # all done
        return


    def acceptFinish(self, controller, **kwds):
        """
        Handler invoked at the end of sample accept/reject
        """
        # grab a channel
        channel = controller.info
        # say something
        channel.log(f"{self.pyre_name}: acceptFinish")
        # all done
        return


    def walkChainsFinish(self, controller, **kwds):
        """
        Handler invoked at the end of the chain walk
        """
        # grab a channel
        channel = controller.info
        # say something
        channel.log(f"{self.pyre_name}: walkChainsFinish")
        # all done
        return


    def resampleStart(self, controller, **kwds):
        """
        Handler invoked before we start resampling
        """
        # grab a channel
        channel = controller.info
        # say something
        channel.log(f"{self.pyre_name}: resampleStart")
        # all done
        return


    def resampleFinish(self, controller, **kwds):
        """
        Handler invoked after we are done resampling
        """
        # grab a channel
        channel = controller.info
        # say something
        channel.log(f"{self.pyre_name}: resampleFinish")
        # all done
        return


    def betaFinish(self, controller, **kwds):
        """
        Handler invoked at the end of the beta step
        """
        # grab a channel
        channel = controller.info
        # say something
        channel.log(f"{self.pyre_name}: betaFinish")
        # all done
        return


    def samplePosteriorFinish(self, controller, **kwds):
        """
        Handler invoked at the end of sampling the posterior
        """
        # grab a channel
        channel = controller.info
        # say something
        channel.log(f"{self.pyre_name}: samplePosteriorFinish")
        # all done
        return


    def simulationFinish(self, controller, **kwds):
        """
        Handler invoked when the simulation is about to finish
        """
        # grab a channel
        channel = controller.info
        # say something
        channel.log(f"{self.pyre_name}: finish")
        # all done
        return


# end of file

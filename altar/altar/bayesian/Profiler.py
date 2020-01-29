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


# an implementation of the monitor protocol
class Profiler(altar.component,
               family="altar.simulations.monitors.profiler",
               implements=altar.simulations.monitor):
    """
    Profiler times the various simulation phases
    """


    # user configurable state
    seed = altar.properties.str()
    seed.doc = "a template for the filename with the timing results"
    seed.default = "prof-{{wid:05}}-{{beta:03}}x{{parameters:03}}x{{chains:06}}x{{steps:03}}.csv"


    # protocol obligations
    @altar.export
    def initialize(self, application):
        """
        Initialize me given an {application} context
        """
        self.pfs = application.pfs
        # nothing to do
        return self


    # meta-methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # the counter of beta steps
        self.beta = 0
        # all done
        return


    # implementation details
    def simulationStart(self, controller, **kwds):
        """
        Handler invoked when the simulation is about to start
        """
        # start the timer
        self.pyre_executive.newTimer(name="altar.profiler.simulation").start()
        # all done
        return


    def samplePosteriorStart(self, controller, **kwds):
        """
        Handler invoked at the beginning of sampling the posterior
        """
        # start the timer
        self.pyre_executive.newTimer(name="altar.profiler.samplePosterior").start()
        # all done
        return


    def prepareSamplingPDFStart(self, controller, **kwds):
        """
        Handler invoked at the beginning of the preparation of the sampling PDF
        """
        # start the timer
        self.pyre_executive.newTimer(name="altar.profiler.prepareSamplingPDF").start()
        # all done
        return


    def prepareSamplingPDFFinish(self, controller, **kwds):
        """
        Handler invoked at the end of the preparation of the sampling PDF
        """
        # grab the timer and stop it
        self.pyre_executive.newTimer(name="altar.profiler.prepareSamplingPDF").stop()
        # all done
        return


    def betaStart(self, controller, **kwds):
        """
        Handler invoked at the beginning of the beta step
        """
        # start the timer
        self.pyre_executive.newTimer(name="altar.profiler.beta").start()
        # all done
        return


    def walkChainsStart(self, controller, **kwds):
        """
        Handler invoked at the beginning of the chain walk
        """
        # start the timer
        self.pyre_executive.newTimer(name="altar.profiler.walk").start()
        # all done
        return


    def chainAdvanceStart(self, controller, **kwds):
        """
        Handler invoked at the beginning of a single step of chain walking
        """
        # start the timer
        self.pyre_executive.newTimer(name="altar.profiler.chainAdvance").start()
        # all done
        return


    def chainAdvanceFinish(self, controller, **kwds):
        """
        Handler invoked at the end of a single step of chain walking
        """
        # grab the timer and stop it
        self.pyre_executive.newTimer(name="altar.profiler.chainAdvance").stop()
        # all done
        return


    def verifyStart(self, controller, **kwds):
        """
        Handler invoked before we start verifying the generated sample
        """
        # start the timer
        self.pyre_executive.newTimer(name="altar.profiler.verify").start()
        # all done
        return


    def verifyFinish(self, controller, **kwds):
        """
        Handler invoked after we are done verifying the generated sample
        """
        # grab the timer and stop it
        self.pyre_executive.newTimer(name="altar.profiler.verify").stop()
        # all done
        return


    def priorStart(self, controller, **kwds):
        """
        Handler invoked before we compute the prior
        """
        # start the timer
        self.pyre_executive.newTimer(name="altar.profiler.prior").start()
        # all done
        return


    def priorFinish(self, controller, **kwds):
        """
        Handler invoked after we compute the prior
        """
        # grab the timer and stop it
        self.pyre_executive.newTimer(name="altar.profiler.prior").stop()
        # all done
        return


    def dataStart(self, controller, **kwds):
        """
        Handler invoked before we compute the data likelihood
        """
        # start the timer
        self.pyre_executive.newTimer(name="altar.profiler.data").start()
        # all done
        return


    def dataFinish(self, controller, **kwds):
        """
        Handler invoked after we compute the data likelihood
        """
        # grab the timer and stop it
        self.pyre_executive.newTimer(name="altar.profiler.data").stop()
        # all done
        return


    def posteriorStart(self, controller, **kwds):
        """
        Handler invoked before we assemble the posterior
        """
        # start the timer
        self.pyre_executive.newTimer(name="altar.profiler.posterior").start()
        # all done
        return


    def posteriorFinish(self, controller, **kwds):
        """
        Handler invoked after we assemble the posterior
        """
        # grab the timer and stop it
        self.pyre_executive.newTimer(name="altar.profiler.posterior").stop()
        # all done
        return


    def acceptStart(self, controller, **kwds):
        """
        Handler invoked at the beginning of sample accept/reject
        """
        # start the timer
        self.pyre_executive.newTimer(name="altar.profiler.accept").start()
        # all done
        return


    def acceptFinish(self, controller, **kwds):
        """
        Handler invoked at the end of sample accept/reject
        """
        # grab the timer and stop it
        self.pyre_executive.newTimer(name="altar.profiler.accept").stop()
        # all done
        return


    def resampleStart(self, controller, **kwds):
        """
        Handler invoked at the beginning of resampling
        """
        # start the timer
        self.pyre_executive.newTimer(name="altar.profiler.resample").start()
        # all done
        return


    def resampleFinish(self, controller, **kwds):
        """
        Handler invoked at the end of resampling
        """
        # grab the timer and stop it
        self.pyre_executive.newTimer(name="altar.profiler.resample").stop()
        # all done
        return


    def walkChainsFinish(self, controller, **kwds):
        """
        Handler invoked at the end of the chain walk
        """
        # grab the timer and stop it
        self.pyre_executive.newTimer(name="altar.profiler.walk").stop()
        # all done
        return


    def betaFinish(self, controller, **kwds):
        """
        Handler invoked at the end of the beta step
        """
        # grab the timer and stop it
        self.pyre_executive.newTimer(name="altar.profiler.beta").stop()
        # update the beta step counter
        self.beta += 1
        # all done
        return


    def samplePosteriorFinish(self, controller, **kwds):
        """
        Handler invoked at the end of sampling the posterior
        """
        # grab the timer and stop it
        self.pyre_executive.newTimer(name="altar.profiler.samplePosterior").stop()
        # all done
        return


    def simulationFinish(self, controller, **kwds):
        """
        Handler invoked when the simulation is about to finish
        """
        # grab the timer and stop it
        timer = self.pyre_executive.newTimer(name="altar.profiler.simulation")
        # stop it
        timer.stop()

        # save the measurements
        self.save(controller=controller)

        # all done
        return


    # implementation details
    def save(self, controller):
        """
        Save the times collected by my timers
        """
        # grab the csv package
        import csv

        # make a list of the phases i care about
        phases = [
            "simulation",
            "samplePosterior",
            "prepareSamplingPDF",
            "beta",
            "walk",
            "chainAdvance",
            "verify",
            "prior",
            "data",
            "posterior",
            "accept",
            "resample",
        ]
        # convert it into a list of the associated timers
        timers = [
            self.pyre_executive.newTimer(name=f"altar.profiler.{phase}")
            for phase in phases
        ]

        # grab the run characteristics
        wid = controller.worker.wid
        beta = self.beta
        parameters = controller.model.parameters
        chains = controller.model.job.chains
        steps = controller.model.job.steps

        # build the filename
        filename = self.seed.format(
            wid=wid, beta=beta, parameters=parameters, chains=chains, steps=steps)
        # open a file for storing the timings
        with open(filename, "w", newline='') as stream:
            # make a csv write
            writer = csv.writer(stream)

            # persist the run characteristics
            writer.writerow(("run characteristics",))
            writer.writerow(("beta steps", beta))
            writer.writerow(("parameters", parameters))
            writer.writerow(("chains", chains))
            writer.writerow(("steps", steps))

            # persist the timings
            writer.writerow(("timings",))
            # go through the simulation phases and their timers
            for phase, timer in zip(phases, timers):
                # read the timer
                duration = timer.read()
                # and save it
                writer.writerow((phase,duration))

        # all done
        return


    # private data
    pfs = None # a reference to the application pfs so I can save my timing results


# end of file

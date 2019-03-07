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


#
class Notifier(altar.component,
               family="altar.simulations.dispatchers.notifier",
               implements=altar.simulations.dispatcher):

    """
    A dispatcher of events generated during the annealing process
    """


    # constants: the event loop identifiers
    start = "simulationStart"

    samplePosteriorStart = "samplePosteriorStart"
    prepareSamplingPDFStart = "prepareSamplingPDFStart"
    prepareSamplingPDFFinish = "prepareSamplingPDFFinish"
    betaStart = "betaStart"
    walkChainsStart = "walkChainsStart"
    chainAdvanceStart = "chainAdvanceStart"
    verifyStart = "verifyStart"
    verifyFinish = "verifyFinish"
    priorStart = "priorStart"
    priorFinish = "priorFinish"
    dataStart = "dataStart"
    dataFinish = "dataFinish"
    posteriorStart = "posteriorStart"
    posteriorFinish = "posteriorFinish"
    acceptStart = "acceptStart"
    acceptFinish = "acceptFinish"
    chainAdvanceFinish = "chainAdvanceFinish"
    walkChainsFinish = "walkChainsFinish"
    resampleStart = "resampleStart"
    resampleFinish = "resampleFinish"
    betaFinish = "betaFinish"
    samplePosteriorFinish = "samplePosteriorFinish"

    finish = "simulationFinish"


    # protocol obligations
    @altar.export
    def initialize(self, application):
        """
        Initialize me given an {application} context
        """
        # nothing to do
        return self


    # interface
    def register(self, monitor):
        """
        Enable {monitor} as an observer of simulation events
        """
        # go through all known event types
        for event in self.events.keys():
            # check
            try:
                # whether the {monitor} implements a handler for this particular event
                handler = getattr(monitor, event)
            # if not
            except AttributeError:
                # no worries
                continue
            # otherwise, add the handler to the correct event table entry
            self.events[event].addObserver(handler)
        # all done
        return


    def notify(self, event, controller):
        """
        Notify all handlers that are waiting for {event}
        """
        # find the observable associated with this event
        observable = self.events[event]
        # and ask it to notify its observers
        observable.notifyObservers(controller=controller)
        # all done
        return


    # meta-methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)

        # establish the table of handled events
        self.events = {
            self.start: altar.patterns.observable(),
            self.samplePosteriorStart: altar.patterns.observable(),
            self.prepareSamplingPDFStart: altar.patterns.observable(),
            self.prepareSamplingPDFFinish: altar.patterns.observable(),
            self.betaStart: altar.patterns.observable(),
            self.walkChainsStart: altar.patterns.observable(),
            self.chainAdvanceStart: altar.patterns.observable(),
            self.verifyStart: altar.patterns.observable(),
            self.verifyFinish: altar.patterns.observable(),
            self.priorStart: altar.patterns.observable(),
            self.priorFinish: altar.patterns.observable(),
            self.dataStart: altar.patterns.observable(),
            self.dataFinish: altar.patterns.observable(),
            self.posteriorStart: altar.patterns.observable(),
            self.posteriorFinish: altar.patterns.observable(),
            self.acceptStart: altar.patterns.observable(),
            self.acceptFinish: altar.patterns.observable(),
            self.chainAdvanceFinish: altar.patterns.observable(),
            self.walkChainsFinish: altar.patterns.observable(),
            self.resampleStart: altar.patterns.observable(),
            self.resampleFinish: altar.patterns.observable(),
            self.samplePosteriorFinish: altar.patterns.observable(),
            self.betaFinish: altar.patterns.observable(),
            self.finish: altar.patterns.observable(),
        }

        # all done
        return


# end of file

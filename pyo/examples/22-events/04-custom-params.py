"""
04-custom-params.py - Passing custom parameters to the instrument.

The built-in arguments of the Events object can't cover all possible controls
an instrument could need to process its sounds. Because of that, the user
should be able to create its own custom parameters an pass them to the
instrument's instances generated by the events. To do so, it's very simple.
One can give any argument to the Events object, it will be automatically part
of the parameters passed to the instrument's instance. In the instrument,
these arguments become instance variables (self.param_name).

"""

from pyo import *

s = Server().boot()

class MyInstrument(EventInstrument):
    def __init__(self, **args):
        EventInstrument.__init__(self, **args)

        # Here, we use two custom parameters, self.duty and self.cutoff. These
        # variables must exist, and therefore should be given as arguments to
        # the Events object that produce the events.
        
        self.phase = Phasor([self.freq, self.freq*1.003])
        self.osc = Compare(self.phase, self.duty, mode="<", mul=1, add=-0.5)
        self.filt = ButLP(self.osc, freq=self.cutoff, mul=self.env).out()

e = Events(instr = MyInstrument,
           degree = EventSeq([5.00, 5.04, 5.07, 6.00]),
           duty = EventSeq([0.02, 0.1, 0.25, 0.5]),     # self.duty in the instrument
           cutoff = EventSeq([5000, 4000, 3000, 2000]), # self.cutoff in the instrument
           beat = 1/2,
           db = [-6, -9, -9, -12],
           attack = 0.001, decay = 0.05, sustain = 0.5, release = 0.005).play()

s.gui(locals())

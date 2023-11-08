
from Instruments.DigitalScope import dpo_2014B
from Instruments.Keysight_34461 import A34461
from Instruments.KeySight_N670x import N670x
from Instruments.KeySight_RP7954 import RP790x

import time 

class Instruments:

    def __init__(self) -> None:
        self.supply = N670x('USB0::0x0957::0x0F07::MY50002157::INSTR')
        # self.Battery = RP790x('USB0::0x2A8D::0x2802::MY59003109::INSTR')
        self.scope = dpo_2014B('USB0::0x0699::0x0456::C014546::INSTR')
        self.voltmeter=A34461('USB0::0x2A8D::0x1301::MY57229855::INSTR')
        self.multimeter=A34461('USB0::0x2A8D::0x1401::MY57216238::INSTR')
        self.multimeter.set_meter__OutputVoltage___ImdpedenceAuto____On()
        # self.multimeter.set_meter__OutputCurrent___ImdpedenceAuto____On()
        self.voltmeter.set_meter__OutputVoltage___ImdpedenceAuto____On()
        self.multimeter.set_Voltage__NPLC(1) # set voltmeter in fast mode
        # time.sleep(2)
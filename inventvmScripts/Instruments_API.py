
from Instruments.DigitalScope import dpo_2014B
from Instruments.Keysight_34461 import A34461
import time 

class Instruments:

    def __init__(self) -> None:
        self.scope = dpo_2014B('USB0::0x0699::0x0456::C010843::INSTR')
        self.voltmeter=A34461('USB0::0x2A8D::0x1301::MY57229855::INSTR')
        self.currentmeter=A34461('USB0::0x2A8D::0x1401::MY57216238::INSTR')
        self.voltmeter.set_meter__OutputVoltage___ImdpedenceAuto____On()
        self.currentmeter.set_meter__OutputVoltage___ImdpedenceAuto____On()
        time.sleep(2)
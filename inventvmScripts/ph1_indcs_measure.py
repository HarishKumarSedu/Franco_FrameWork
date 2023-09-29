
import pandas as pd
from time import sleep
from Instruments.multimeter import mul_34401A
from Instruments.Keysight_34461 import A34461
from Instruments.KeySight_N670x import N670x
from writeExcel import writeInExcel

class ph1_indcs_measure:

    def __init__(self):
        self.voltmeter_ph1Il_out = mul_34401A('GPIB0::25::INSTR')
        self.supply = N670x(port='USB0::0x0957::0x0F07::MY50002157::INSTR')

        # self.ph1_sweepHighSide__Curr()

    def ph1_sweepHighSide__Curr(self,filename='ph1_indcs_measure/ph1_indcs_measure.xlsx',sheet='sheet1'):
        set_current_A = []
        ph1Il_out_V = []
        try:
            for curr in range(0,-3000,-1):
                self.supply.setNegCurrent(channel=3,current=curr*0.001)
                set_current_A.append(self.supply.getCurrent(channel=3))
                ph1Il_out_V.append(self.supply.getCurrent(channel=3))
                sleep(0.05)
            writeInExcel(set_current_A=set_current_A,ph1Il_out_V=ph1Il_out_V,sheet=sheet,filename=filename)
        except KeyboardInterrupt:
            self.supply.setNegCurrent(channel=3,current=0)
            writeInExcel(set_current_A=set_current_A,ph1Il_out_V=ph1Il_out_V,sheet=sheet,filename=filename)

if __name__ == '__main__':
    ph1=ph1_indcs_measure()
    ph1.ph1_sweepHighSide__Curr()


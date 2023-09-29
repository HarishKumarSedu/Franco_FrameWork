
import pandas as pd
from time import sleep
from Instruments.multimeter import mul_34401A
from Instruments.Keysight_34461 import A34461
from Instruments.KeySight_N670x import N670x
from writeExcel import writeInExcel

class cfly_Sense:

    def __init__(self):
        self.voltmeter_cfly = mul_34401A('GPIB0::25::INSTR')
        self.supply = N670x(port='USB0::0x0957::0x0F07::MY50002157::INSTR')



    def cfly_sweep__Volt(self,filename='cfly_sense_measure/cfly_sense_measure.xlsx',sheet='sheet1'):
        ph1_cfly_sns_masure = []
        cfly_voltage_force = []
        try:
            for i in range(0,4000,1):
                cfly_voltage_force.append(i*0.001)
                self.supply.setVoltage(channel=1,voltage=cfly_voltage_force[-1])
                ph1_cfly_sns_masure.append(self.voltmeter_cfly.meas_V())
                
            cfly_voltage_force.append(0)
            writeInExcel(cfly_voltage_force=cfly_voltage_force,ph1_cfly_sns_masure=ph1_cfly_sns_masure,sheet=sheet,filename=filename)
        except KeyboardInterrupt:
            cfly_voltage_force.append(0)
            writeInExcel(cfly_voltage_force=cfly_voltage_force,ph1_cfly_sns_masure=ph1_cfly_sns_masure,sheet=sheet,filename=filename)
          
if __name__ == '__main__':
    cflySense=cfly_Sense()
    cflySense.cfly_sweep__Volt()


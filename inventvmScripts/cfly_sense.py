
import pandas as pd
from time import sleep
from Instruments.multimeter import mul_34401A
from Instruments.Keysight_34461 import A34461
from Instruments.KeySight_N670x import N670x
from writeExcel import writeInExcel
import pyvisa as visa 

class cfly_Sense:

    def __init__(self):
        self.voltmeter_cfly_SNS = mul_34401A('GPIB0::25::INSTR')
        self.voltmeter_cfly_Ref = mul_34401A('USB0::0x2A8D::0x1301::MY57229855::INSTR')
        self.supply = N670x(port='USB0::0x0957::0x0F07::MY50002157::INSTR')



    def cfly_sweep__Volt(self,filename='cfly_sense_measure/cfly_sense_measure1.xlsx',sheet='cm_0V'):
        ph1_cfly_sns_masure = []
        ph1_cfly_ref_masure = []
        cfly_voltage_force = []
        try:
            for i in range(0,40,1):
                cflyVolt = i*0.1
                self.supply.setVoltage(channel=1,voltage=cflyVolt)
                ph1_cfly_sns_masure.append(self.voltmeter_cfly_SNS.meas_V())
                ph1_cfly_ref_masure.append(self.voltmeter_cfly_Ref.meas_V())
                cfly_voltage_force.append(cflyVolt)

            print(ph1_cfly_sns_masure,cfly_voltage_force)
            writeInExcel(cfly_voltage_force=cfly_voltage_force,ph1_cfly_sns_masure=ph1_cfly_sns_masure,ph1_cfly_ref_masure=ph1_cfly_ref_masure,sheet=sheet,filename=filename)
        except  visa.errors.VisaIOError:
            writeInExcel(cfly_voltage_force=cfly_voltage_force,ph1_cfly_sns_masure=ph1_cfly_sns_masure,ph1_cfly_ref_masure=ph1_cfly_ref_masure,sheet=sheet,filename=filename)

          
if __name__ == '__main__':
    cflySense=cfly_Sense()
    cflySense.cfly_sweep__Volt()


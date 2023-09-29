import re 
import pandas as pd
from time import sleep
from Instruments.multimeter import mul_34401A
from Instruments.Keysight_34461 import A34461
from Instruments.KeySight_N670x import N670x
from writeExcel import writeInExcel
import pyvisa as visa 
class input_CurreSenseV:

    def __init__(self) -> None:
        self.voltMeter_ibus__Sense = mul_34401A('GPIB0::25::INSTR')
        self.voltMeter_vbusCurrent__Sense = A34461('USB0::0x2A8D::0x1301::MY57229855::INSTR')
        # self.voltMeter = mul_34401A('GPIB0::25::INSTR')
        self.supply = N670x(port='USB0::0x0957::0x0F07::MY50000622::INSTR')
        self.instructions_raw = [
        ]

        self.parse_Instruction()

        self.supply.setVoltage(channel=3,voltage=5.006) # CMID 

        self.supply.setVoltage(1,5) # vbus 

        # self.input_CurreSense_loading(sheet='Vbus_5V',filename='Input_CurrentSense/input_CurrentSense.xlsx')

    def input_CurreSense_loading(self,filename,sheet):
        input_CurreSense_current_vbus = []
        input_CurreSense_current_Cmid = []
        input_CurreSense_voltage = []
        input_CurreSense_CalCulated_current = []
        error_percentage = []
        vbus = 5.007

        try:
            while True:
                current_vbus = self.supply.getCurrent(channel=1)
                print(current_vbus)
                if current_vbus < 2.97:
                    self.supply.setVoltage(channel=3,voltage=vbus)
                    sleep(0.1)
                    input_CurreSense_current_vbus.append(current_vbus)
                    input_CurreSense_current_Cmid.append(-1*self.supply.getCurrent(channel=3))
                    sleep(0.1)
                    input_CurreSense_voltage.append(self.voltMeter.meas_V())
                    vbus = vbus - 0.010
                    input_CurreSense_CalCulated_current.append((input_CurreSense_voltage[-1]*2750)/500)
                    error_percentage.append(((input_CurreSense_CalCulated_current[-1] - input_CurreSense_current_vbus[-1] )/input_CurreSense_current_vbus[-1])*100)
                else:
                    self.supply.setVoltage(channel=1,voltage=5.006)
                    writeInExcel(input_CurreSense_voltage=input_CurreSense_voltage,input_CurreSense_current_vbus=input_CurreSense_current_vbus,input_CurreSense_current_Cmid=input_CurreSense_current_Cmid,input_CurreSense_CalCulated_current=input_CurreSense_CalCulated_current,error_percentage=error_percentage,sheet=sheet,filename=filename)
                    break
        except visa.errors.VisaIOError or KeyboardInterrupt:
            print(input_CurreSense_current_vbus)
            self.supply.setVoltage(channel=1,voltage=5.006)
            writeInExcel(input_CurreSense_voltage=input_CurreSense_voltage,input_CurreSense_current_vbus=input_CurreSense_current_vbus,input_CurreSense_current_Cmid=input_CurreSense_current_Cmid,input_CurreSense_CalCulated_current=input_CurreSense_CalCulated_current,error_percentage=error_percentage,sheet=sheet,filename=filename)
    
    def input_CurreSense_external_res(self,filename,sheet):
        vbus = 5.007
        ibus_Sense__Voltage = []
        VbusCurrent_Sense__Voltage = []
        try:
            while True:
                current_vbus = self.supply.getCurrent(channel=1)
                print(current_vbus)
                if current_vbus < 2.97:
                   self.supply.setVoltage(channel=3,voltage=vbus)
                   ibus_Sense__Voltage.append(self.voltMeter_ibus__Sense.meas_V())
                   VbusCurrent_Sense__Voltage.append(self.voltMeter_vbusCurrent__Sense.meas_V())
                   vbus = vbus - 0.010
                else:
                    self.supply.setVoltage(channel=1,voltage=5.006)
                    writeInExcel(ibus_Sense__Voltage=ibus_Sense__Voltage,VbusCurrent_Sense__Voltage=VbusCurrent_Sense__Voltage,sheet=sheet,filename=filename)
                    break
        except visa.errors.VisaIOError or KeyboardInterrupt:
            self.supply.setVoltage(channel=1,voltage=5.006)
            writeInExcel(ibus_Sense__Voltage=ibus_Sense__Voltage,VbusCurrent_Sense__Voltage=VbusCurrent_Sense__Voltage,sheet=sheet,filename=filename)
                   
    def parse_Instruction(self):
        self.instructions=[]
        for instruction in self.instructions_raw:
            register_parse_data = self.parse_registerAddress(address=instruction)
            self.instructions.append(register_parse_data)
            reg_data = self.dut.read_register(register_parse_data.get("RegisterAddress")) 
            print('RegData',reg_data)
            self.dut.write_register(register_parse_data.get("RegisterAddress"), reg_data | register_parse_data.get("RegisterValue") << register_parse_data.get("RegisterLSB"))
            
    
    def parse_registerAddress(self,address):
        register = address
        if re.match(re.compile("0x"),register):
           register = register.split("_")
           register_value = int(register[1],16)
           if re.search(":",register[0]):
               Reg = {}
           else:
               if "[" in register[0] :
                   register = register[0].split("[")
                   register_address = int(register[0],16)
                   register_LSB = int(register[1].strip("]"))
                   Reg = {"RegisterAddress":register_address,"RegisterLSB":register_LSB,"RegisterValue":register_value }
        return Reg
    
    
if __name__ == '__main__':
    input_CurrSense = input_CurreSenseV()
    # input_CurrSense.input_CurreSense_loading(sheet='Vbus_5V',filename='Input_CurrentSense/input_CurrentSense4.xlsx')
    input_CurrSense.input_CurreSense_external_res(sheet='Vbus_5V',filename='Input_CurrentSense/input_CurrentSense4.xlsx')
    # try:
    #     input_CurrSense.input_CurreSense_loading(sheet='Vbus_5V',filename='Input_CurrentSense/input_CurrentSense1.xlsx')
    # except KeyboardInterrupt:
    #     input_CurrSense = input_CurreSenseV()
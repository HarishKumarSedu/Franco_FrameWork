import re 
import pandas as pd
from time import sleep
from FrancoTest import test_station,dut
from Instruments.multimeter import mul_34401A
from Instruments.KeySight_N670x import N670x
from writeExcel import writeInExcel

class LDO_1_2V:

    def __init__(self) -> None:
        self.dut = dut
        self.voltMeter = mul_34401A('GPIB0::25::INSTR')
        self.supply = N670x(port='USB0::0x0957::0x0F07::MY50000622::INSTR')
        self.instructions_raw = [
        ]

        self.parse_Instruction()

        print(self.voltMeter.meas_V())
        self.supply.setNegCurrent(channel=4,current=-0.002)

        self.supply.setVoltage(3,3.8) # Vbat 
        self.supply.setVoltage(1,5) # vbus 

        self.ldo_1_2_loading(sheet='Vbat_3_8V_vbus_5v',filename='LDO_1_2V/LDO_1_2V.xlsx')
        sleep(1)
        self.supply.setVoltage(3,0) # Vbat 
        self.supply.setVoltage(1,5) # vbus 
        self.ldo_1_2_loading(sheet='Vbat_0V_vbus_5v',filename='LDO_1_2V/LDO_1_2V.xlsx')

    def ldo_1_2_loading(self,filename,sheet):
        ldo_1_2_current = []
        ldo_1_2_voltage = []
        for i in range(-5,-55,-5):
            ldo_1_2_current.append(i*0.001)
            self.supply.setNegCurrent(channel=4,current=ldo_1_2_current[-1])
            sleep(0.1)
            ldo_1_2_voltage.append(self.voltMeter.meas_V())
        self.supply.setNegCurrent(channel=4,current=0.0)
        print(ldo_1_2_current)
        print(ldo_1_2_voltage)

        writeInExcel(ldo_1_2_voltage=ldo_1_2_voltage,ldo_1_2_current=ldo_1_2_current,sheet=sheet,filename=filename)


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
    LDO_1_2V()
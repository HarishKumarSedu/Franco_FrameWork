import re 
import pandas as pd
from time import sleep
# from FrancoTest import test_station,dut
from Instruments.multimeter import mul_34401A
from Instruments.KeySight_N670x import N670x

class ph1_indcs:

    def __init__(self,dut) -> None:
        self.dut = dut
        self.instructions_raw = [
            "0x00000220[1]_0x1",
            "0x00000220[2]_0x1",
            "0x00000220[8]_0x1",
            "0x00000220[29]_0x1",
            "0x00000220[28]_0x1",
            "0x00000284[3]_0x1",
            "0x00000284[4]_0x1",
            "0x00000280[15]_0x1",
            "0x00000280[14]_0x1",
        ]

        # self.parse_Instruction()

    def parse_Instructions(self):
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
    ph1_indcs()
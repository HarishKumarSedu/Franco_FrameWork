from FrancoTest import test_station, dut
import re 
from time import sleep

class DCO_Trim:

    def __init__(self) -> None:
        self.dut = dut
        self.instructions_raw = [
            "0x00000290[27:24]_0x4",
            "0x00000290[23:21]_0x7",
        ] 
        self.trim_register__raw = "0x00000238[15:10]"

        self.parse_Instruction()
        self.dco_trim()

    def dco_trim(self):
        trim_register = self.parse_registerAddress(address=self.trim_register__raw)
        for i in range(0,2**(trim_register.get('RegisterMSB')- trim_register.get('RegisterLSB')+1)):
            print(i)
            self.write_register(trim_register,i)
            sleep(0.2)

    def write_register(self,register,write_value):
        reg_data = self.read_register(register=register)
        print('RegData',hex(reg_data))
        self.dut.write_register(register.get("RegisterAddress"), reg_data & write_value << register.get("RegisterLSB"))
    
    def read_register(self,register):
        return self.dut.read_register(register.get("RegisterAddress"))
    
    def parse_Instruction(self):
        self.instructions=[]
        for instruction in self.instructions_raw:
            register_parse_data = self.parse_registerAddress(address=instruction)
            self.write_register(register=register_parse_data,write_value=register_parse_data.get("RegisterValue"))
    
    def parse_registerAddress(self,address):
        register = address
        if re.match(re.compile("0x"),register):
           if re.search("_",register):
                register = register.split("_")
                register_value = int(register[1],16)
                if re.search(":",register[0]):
                    register = register[0].split(":")
                    register_LSB = int(register[1].strip("]"))
                    register = register[0].split("[")
                    register_address = int(register[0],16)
                    register_MSB = int(register[1])
                    Reg = {"RegisterAddress":register_address,"RegisterLSB":register_LSB,"RegisterMSB":register_MSB,"RegisterValue":register_value }
           else:
                if "[" in register[0] :
                    register = register[0].split("[")
                    register_address = int(register[0],16)
                    register_LSB = int(register[1].strip("]"))
                    Reg = {"RegisterAddress":register_address,"RegisterLSB":register_LSB,"RegisterMSB":register_LSB,"RegisterValue":register_value }
                else:
                    if re.search(":",register):
                        register = register.split(":")
                        register_LSB = int(register[1].strip("]"))
                        register = register[0].split("[")
                        register_address = int(register[0],16)
                        register_MSB = int(register[1])
                        Reg = {"RegisterAddress":register_address,"RegisterLSB":register_LSB,"RegisterMSB":register_MSB,"RegisterValue":0 }
                    else:
                        if "[" in register :
                            register = register[0].split("[")
                            register_address = int(register[0],16)
                            register_LSB = int(register[1].strip("]"))
                            Reg = {"RegisterAddress":register_address,"RegisterLSB":register_LSB,"RegisterMSB":register_LSB,"RegisterValue":0 }
        return Reg
    
if __name__ == '__main__':
    DCO_Trim()
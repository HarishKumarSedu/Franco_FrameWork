from Franco_Test__APIs import FrancoAPIS
import re 
from time import sleep

class DCO_Trim:

    def __init__(self,dut) -> None:
        self.dut = FrancoAPIS(dut=dut)
        self.instructions_raw = [
            "0x00000290[27:24]_0x4",
            "0x00000290[23:21]_0x7",
        ] 
        self.trim_register__raw = "0x00000238[15:10]"

        self.dut.parse_Instruction()
        self.dco_trim()

    def dco_trim(self):
        trim_register = self.dut.parse_registerAddress(address=self.trim_register__raw)
        for i in range(0,2**(trim_register.get('RegisterMSB')- trim_register.get('RegisterLSB')+1)):
            print(i)
            self.dut.write_register(trim_register,i)
            sleep(0.2)


    
if __name__ == '__main__':
    DCO_Trim()
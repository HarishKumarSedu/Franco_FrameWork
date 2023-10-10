# from FrancoTest import Franco
import re 
from time import sleep

class Vref_0p6V:

    def __init__(self,dut) -> None:
        self.dut = dut
        self.instructions_raw = [
            "0x00000220[8]_0x1",
            "0x00000220[29]_0x1",
            "0x00000230[5]_0x1",
            "0x00000284[31]_0x1",
            "0x00000284[26]_0x1",
            "0x00000284[30:27]_0x8",
            "0x00000288[18]_0x1",
            "0x00000288[21:19]_0x2",
            "0x00000234[7]_0x1",
            "0x00000288[15:9]_0x1",
            "0x00000284[30:27]_0x7",
            "0x00000284[25:22]_0x6",
        ] 
        self.trim_register__raw = "0x00000254[7:3]"

        # self.parse_Instruction(instructions_raw=self.instructions_raw)
        self.V0p6_Instructions()

    def V0p6_Instructions(self):
        self.dut.IVM.REG_AON_RW.DS_AON_EN_VDDSNS_UVLO_B.value=1
        self.dut.IVM.REG_TEST0_RW.DS_TEST1_VIS_EN.value=1
        self.dut.IVM.REG_TEST0_RW.DS_TEST2_VIS_EN.value=1
        self.dut.IVM.REG_TEST0_RW.DS_TEST1_VIS_SEL.value=8
        self.dut.IVM.REG_LDOS_RW.DS_LDO1P2_VIS_ENA.value=1
        self.dut.IVM.REG_TEST1_RW.DS_AON_EN_TEST.value=1
        self.dut.IVM.REG_TEST1_RW.DS_AON_TEST_SEL.value=2
        self.dut.IVM.REG_TEST0_RW.DS_TEST2_VIS_SEL.value=6
        self.dut.IVM.REG_TEST0_RW.DS_TEST1_VIS_EN.value=0
        sleep(4)
        self.dut.IVM.REG_TEST0_RW.DS_TEST1_VIS_SEL.value=7
        self.dut.IVM.REG_TEST0_RW.DS_TEST1_VIS_EN.value=1


    def write_register(self,register,write_value):
        reg_data = self.read_register(register=register)
        self.dut.write_register(register.get("RegisterAddress"), reg_data | write_value << register.get("RegisterLSB"))
        reg_data = self.read_register(register=register)
        print('RegData',hex(reg_data))
    
    def read_register(self,register):
        return self.dut.read_register(register.get("RegisterAddress"))
    
    def parse_Instruction(self,instructions_raw):
        self.instructions=[]
        for instruction in instructions_raw:
            register_parse_data = self.parse_registerAddress(address=instruction)
            self.write_register(register=register_parse_data,write_value=register_parse_data.get("RegisterValue"))
    
    def parse_registerAddress(self,address:str):
        register = address
        Reg={}
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
    Vref_0p6V()
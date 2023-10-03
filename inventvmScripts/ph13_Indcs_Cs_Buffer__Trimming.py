from Franco_Test__APIs import FrancoAPIS
import re 
from time import sleep
from startup import Startup

class PH13_Indcs_CS_Buffer_Trim:

    def __init__(self,dut) -> None:
        self.dut = FrancoAPIS(dut=dut)
        
        # self.dut = dut
        self.instructions_raw = [
        ] 
        self.trim_register__raw = "0x00000260[32:29]"
        self.trim_register  = self.dut.dut.IVM.REG_TRIM3_RW.DS_PH13_INDCS_TRIM_BUF



    def parse_Instructions(self):
        Startup(dut=self.dut.dut).buck_PowerUp()
        self.dut.parse_Instruction(instructions_raw=self.instructions_raw)

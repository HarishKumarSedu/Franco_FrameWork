from Franco_Test__APIs import FrancoAPIS
import re 
from time import sleep
from startup import Startup

class PH1S4_Indcs_Mirror_Trim:

    def __init__(self,dut) -> None:
        self.dut = FrancoAPIS(dut=dut)
        
        # self.dut = dut
        self.instructions_raw = [
            "0x00000284[4]_0x0",
            "0x00000284[3]_0x1",
            "0x00000280[14]_0x0",
            "0x00000280[15]_0x1",
        ] 
        self.trim_register__raw = "0x00000278[16:12]"
        self.trim_register  = self.dut.dut.IVM.REG_TRIM9_RW.DS_PH1_INDCS_MIR_TRIM_S4


    def parse_Instructions(self):
        Startup(dut=self.dut.dut).buck_PowerUp()
        self.dut.parse_Instruction(instructions_raw=self.instructions_raw)

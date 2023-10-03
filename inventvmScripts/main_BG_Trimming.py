
from Franco_Test__APIs import FrancoAPIS
import re 
from time import sleep

class MainBG_Trim:

    def __init__(self,dut) -> None:
        self.dut = FrancoAPIS(dut=dut)
        # self.dut = dut
        self.instructions_raw = [
            "0x00000220[8]_0x1",
            "0x00000220[29]_0x1",
            "0x00000220[28]_0x1",
            "0x00000284[31]_0x1",
            "0x00000284[30:27]_0x8",
            "0x00000288[15:9]_0x1",
            "0x00000284[30:27]_0xA",
            "0x00000288[8]_0x1",
            "0x00000288[15:9]_0x1",
        ] 
        self.trim_register__raw = "0x00000258[9:6]"
        self.trim_register  = self.dut.dut.IVM.REG_TRIM1_RW.DS_REF_TRIM

    def parse_Instructions(self):
        self.dut.parse_Instruction(instructions_raw=self.instructions_raw)

    def mainBg_Instructions(self):
        self.dut.dut.IVM.REG_PWRUP0_RW.DS_HVLDO_EN.value = 1
        self.dut.dut.IVM.REG_PWRUP0_RW.DS_LDO1P8_PDNB.value = 1
        self.dut.dut.IVM.REG_PWRUP0_RW.DS_REF_PDNB.value = 1
        self.dut.dut.IVM.REG_TEST0_RW.DS_TEST1_VIS_EN.value = 1
        self.dut.dut.IVM.REG_TEST0_RW.DS_TEST1_VIS_SEL.value = 10
        self.dut.dut.IVM.REG_TEST1_RW.DS_REF_TST_VIS_EN.value = 1
        self.dut.dut.IVM.REG_TEST1_RW.DS_REF_TST_VIS.value = 1

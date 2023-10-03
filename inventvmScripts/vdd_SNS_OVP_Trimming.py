from Franco_Test__APIs import FrancoAPIS
import re 
from time import sleep

class VDDSNS_OVP_Trim:

    def __init__(self,dut) -> None:
        self.dut = FrancoAPIS(dut=dut)
        # self.dut = dut
        self.instructions_raw = [
            "0x00000220[8]_0x1",
            "0x00000220[29]_0x1",
            "0x00000220[28]_0x1",
            "0x00000220[10]_0x1",
            "0x00000230[3:0]_0x8",
            "0x00000290[20:17]_0x0",
            "0x00000288[22:19]_0x3",
        ] 
        self.trim_register__raw = "0x00000254[21:18]"
        self.trim_register  = self.dut.dut.IVM.REG_TRIM0_RW.DS_AON_VDDSNS_OVP_TRIM


    def parse_Instructions(self):
        self.dut.parse_Instruction(instructions_raw=self.instructions_raw)

    def vddSNS_Ovp_Instructions(self):
        self.dut.dut.IVM.REG_PWRUP0_RW.DS_HVLDO_EN.VALUE=1
        self.dut.dut.IVM.REG_PWRUP0_RW.DS_LDO1P8_PDNB.VALUE=1
        self.dut.dut.IVM.REG_PWRUP0_RW.DS_REF_PDNB.VALUE=1
        self.dut.dut.IVM.REG_PWRUP0_RW.DS_AON_EN_VDDSNS_OVP.VALUE=1
        self.dut.dut.IVM.REG_AON_RW.DS_AON_VDDSNS_OVP_SEL.VALUE=8
        self.dut.dut.IVM.REG_VIS_MUX_RW.TST2_BLOCK_SEL.VALUE=0
        self.dut.dut.IVM.REG_VIS_MUX_RW.TST2_SEL.VALUE=3

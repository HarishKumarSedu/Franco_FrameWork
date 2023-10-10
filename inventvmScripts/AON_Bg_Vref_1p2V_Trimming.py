import re 
from time import sleep

class Vref_1p2V:

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
        self.p6_Instructions()

    def V1p2_Instructions(self):
        self.dut.IVM.REG_AON_RW.DS_AON_EN_VDDSNS_UVLO_B.value=1
        self.dut.IVM.REG_TEST0_RW.DS_TEST1_VIS_EN.value=1
        self.dut.IVM.REG_TEST0_RW.DS_TEST2_VIS_EN.value=1
        self.dut.IVM.REG_TEST0_RW.DS_TEST1_VIS_SEL.value=8
        self.dut.IVM.REG_LDOS_RW.DS_LDO1P2_VIS_ENA.value=1
        self.dut.IVM.REG_TEST1_RW.DS_AON_EN_TEST.value=1
        self.dut.IVM.REG_TEST1_RW.DS_AON_TEST_SEL.value=2
        self.dut.IVM.REG_TEST0_RW.DS_TEST1_VIS_SEL.value=7
        self.dut.IVM.REG_TEST0_RW.DS_TEST2_VIS_SEL.value=6
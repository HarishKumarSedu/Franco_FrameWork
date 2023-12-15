from time import sleep
class Cfly_chg_dshg:
    def __init__(self,dut):
        self.dut = dut

    def ph1_cfly_charge(self):
        self.dut.IVM.REG_FORCE_RW.DS_PH1_FORCE_BAL_EN.value = 1
        self.dut.IVM.REG_FORCE_RW.DS_PH1_FORCE_DISCHG.value = 1
        sleep(0.1)
        self.dut.IVM.REG_FORCE_RW.DS_PH1_FORCE_DISCHG.value = 0
        self.dut.IVM.REG_FORCE_RW.DS_PH1_FORCE_BAL_EN.value = 0
        sleep(0.1)
        self.dut.IVM.REG_FORCE_RW.DS_PH1_FORCE_CHG_TOP.value = 1
        self.dut.IVM.REG_FORCE_RW.DS_PH1_FORCE_CHG_BTM.value = 1
        self.dut.IVM.REG_FORCE_RW.DS_PH1_FORCE_BAL_EN.value = 1
    def ph1_cfly_discharge(self):
        self.dut.IVM.REG_FORCE_RW.DS_PH1_FORCE_CHG_TOP.value = 0
        self.dut.IVM.REG_FORCE_RW.DS_PH1_FORCE_CHG_BTM.value = 0
        self.dut.IVM.REG_FORCE_RW.DS_PH1_FORCE_BAL_EN.value = 1
        self.dut.IVM.REG_FORCE_RW.DS_PH1_FORCE_DISCHG.value = 1
        sleep(0.1)
        self.dut.IVM.REG_FORCE_RW.DS_PH1_FORCE_DISCHG.value = 0
        self.dut.IVM.REG_FORCE_RW.DS_PH1_FORCE_BAL_EN.value = 0




    def ph2_cfly_charge(self):
        self.dut.IVM.REG_FORCE_RW.DS_PH2_FORCE_BAL_EN.value = 1
        self.dut.IVM.REG_FORCE_RW.DS_PH2_FORCE_DISCHG.value = 1
        sleep(0.1)
        self.dut.IVM.REG_FORCE_RW.DS_PH2_FORCE_DISCHG.value = 0
        self.dut.IVM.REG_FORCE_RW.DS_PH2_FORCE_BAL_EN.value = 0
        sleep(0.1)
        self.dut.IVM.REG_FORCE_RW.DS_PH2_FORCE_CHG_TOP.value = 1
        self.dut.IVM.REG_FORCE_RW.DS_PH2_FORCE_CHG_BTM.value = 1
        self.dut.IVM.REG_FORCE_RW.DS_PH2_FORCE_BAL_EN.value = 1

    def ph2_cfly_discharge(self):
        self.dut.IVM.REG_FORCE_RW.DS_PH2_FORCE_CHG_TOP.value = 0
        self.dut.IVM.REG_FORCE_RW.DS_PH2_FORCE_CHG_BTM.value = 0
        self.dut.IVM.REG_FORCE_RW.DS_PH2_FORCE_BAL_EN.value = 1
        self.dut.IVM.REG_FORCE_RW.DS_PH2_FORCE_DISCHG.value = 1
        sleep(0.1)
        self.dut.IVM.REG_FORCE_RW.DS_PH2_FORCE_DISCHG.value = 0
        self.dut.IVM.REG_FORCE_RW.DS_PH2_FORCE_BAL_EN.value = 0



    def ph3_cfly_charge(self):
        self.dut.IVM.REG_FORCE_RW.DS_PH3_FORCE_BAL_EN.value = 1
        self.dut.IVM.REG_FORCE_RW.DS_PH3_FORCE_DISCHG.value = 1
        sleep(0.1)
        self.dut.IVM.REG_FORCE_RW.DS_PH3_FORCE_DISCHG.value = 0
        self.dut.IVM.REG_FORCE_RW.DS_PH3_FORCE_BAL_EN.value = 0
        sleep(0.1)
        self.dut.IVM.REG_FORCE_RW.DS_PH3_FORCE_CHG_TOP.value = 1
        self.dut.IVM.REG_FORCE_RW.DS_PH3_FORCE_CHG_BTM.value = 1
        self.dut.IVM.REG_FORCE_RW.DS_PH3_FORCE_BAL_EN.value = 1

    def ph3_cfly_discharge(self):
        self.dut.IVM.REG_FORCE_RW.DS_PH3_FORCE_CHG_TOP.value = 0
        self.dut.IVM.REG_FORCE_RW.DS_PH3_FORCE_CHG_BTM.value = 0
        self.dut.IVM.REG_FORCE_RW.DS_PH3_FORCE_BAL_EN.value = 1
        self.dut.IVM.REG_FORCE_RW.DS_PH3_FORCE_DISCHG.value = 1
        sleep(0.1)
        self.dut.IVM.REG_FORCE_RW.DS_PH3_FORCE_DISCHG.value = 0
        self.dut.IVM.REG_FORCE_RW.DS_PH3_FORCE_BAL_EN.value = 0



    def ph4_cfly_charge(self):
        self.dut.IVM.REG_FORCE_RW.DS_PH4_FORCE_BAL_EN.value = 1
        self.dut.IVM.REG_FORCE_RW.DS_PH4_FORCE_DISCHG.value = 1
        sleep(0.1)
        self.dut.IVM.REG_FORCE_RW.DS_PH4_FORCE_DISCHG.value = 0
        self.dut.IVM.REG_FORCE_RW.DS_PH4_FORCE_BAL_EN.value = 0
        sleep(0.1)
        self.dut.IVM.REG_FORCE_RW.DS_PH4_FORCE_CHG_TOP.value = 1
        self.dut.IVM.REG_FORCE_RW.DS_PH4_FORCE_CHG_BTM.value = 1
        self.dut.IVM.REG_FORCE_RW.DS_PH4_FORCE_BAL_EN.value = 1

    def ph4_cfly_discharge(self):
        self.dut.IVM.REG_FORCE_RW.DS_PH4_FORCE_CHG_TOP.value = 0
        self.dut.IVM.REG_FORCE_RW.DS_PH4_FORCE_CHG_BTM.value = 0
        self.dut.IVM.REG_FORCE_RW.DS_PH4_FORCE_BAL_EN.value = 1
        self.dut.IVM.REG_FORCE_RW.DS_PH4_FORCE_DISCHG.value = 1
        sleep(1)
        self.dut.IVM.REG_FORCE_RW.DS_PH4_FORCE_DISCHG.value = 0
        self.dut.IVM.REG_FORCE_RW.DS_PH4_FORCE_BAL_EN.value = 0
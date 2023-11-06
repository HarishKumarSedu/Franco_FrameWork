import re , pandas as pd , time
from Franco_Test__APIs import FrancoAPIS
from startup import Startup
from Instruments_API import Instruments
class QuickCheck:

    def __init__(self,dut) -> None:
        self.dut = dut
        self.apis = FrancoAPIS(dut=dut)
        self.startup = Startup(dut=dut)
        self.multimeter = Instruments().multimeter
        self.supply = Instruments().supply
        self.supply.outp_ON(channel=1)
        self.supply.setVoltage(channel=1,voltage=5)
        time.sleep(1)
        self.SetUp()


    def SetUp(self):
        # self.startup.cirrus_Startup() # Run the buck powerup 
        # self.startup.IVM_Startup() # Run the buck powerup 
        self.startup.buck_PowerUp() # Run the buck powerup 
        # set the powersupply @vsys with sinfel quadrent 
        self.dut.IVM.REG_TEST0_RW.DS_PH1_DRV_TEST_HS.value=1
        self.dut.IVM.REG_TEST0_RW.DS_PH1_DRV_TEST_EN.value=1
        time.sleep(1)
        self.dut.IVM.REG_TEST0_RW.DS_PH1_DRV_TEST_HS.value=0
        self.dut.IVM.REG_TEST0_RW.DS_PH1_DRV_TEST_EN.value=0
        self.startup.buck_PowerDown() # Run the buck powerdown 
        self.supply.outp_OFF(channel=1)
        print('Phase 1 Working')
        # time.sleep(1)
        # self.dut.IVM.REG_TEST0_RW.DS_PH2_DRV_TEST_HS.value=0
        # self.dut.IVM.REG_TEST0_RW.DS_PH2_DRV_TEST_EN.value=0
        self.supply.outp_ON(channel=1)
        time.sleep(1)
        self.startup.buck_PowerUp() # Run the buck powerup
        self.dut.IVM.REG_TEST0_RW.DS_PH2_DRV_TEST_HS.value=1
        self.dut.IVM.REG_TEST0_RW.DS_PH2_DRV_TEST_EN.value=1
        time.sleep(1)
        self.dut.IVM.REG_TEST0_RW.DS_PH2_DRV_TEST_HS.value=0
        self.dut.IVM.REG_TEST0_RW.DS_PH2_DRV_TEST_EN.value=0
        self.startup.buck_PowerDown() # Run the buck powerdown 
        self.supply.outp_OFF(channel=1)
        print('Phase 2 Working')
        self.supply.outp_ON(channel=1)
        time.sleep(1)
        self.startup.buck_PowerUp() # Run the buck powerup
        self.dut.IVM.REG_TEST0_RW.DS_PH3_DRV_TEST_HS.value=1
        self.dut.IVM.REG_TEST0_RW.DS_PH3_DRV_TEST_EN.value=1
        time.sleep(1)
        self.dut.IVM.REG_TEST0_RW.DS_PH3_DRV_TEST_HS.value=0
        self.dut.IVM.REG_TEST0_RW.DS_PH3_DRV_TEST_EN.value=0
        self.startup.buck_PowerDown() # Run the buck powerdown 
        self.supply.outp_OFF(channel=1)
        print('Phase 3 Working')
        self.supply.outp_ON(channel=1)
        time.sleep(1)
        self.startup.buck_PowerUp() # Run the buck powerup
        self.dut.IVM.REG_TEST0_RW.DS_PH4_DRV_TEST_HS.value=1
        self.dut.IVM.REG_TEST0_RW.DS_PH4_DRV_TEST_EN.value=1
        time.sleep(1)
        self.dut.IVM.REG_TEST0_RW.DS_PH4_DRV_TEST_HS.value=0
        self.dut.IVM.REG_TEST0_RW.DS_PH4_DRV_TEST_EN.value=0
        self.startup.buck_PowerDown() # Run the buck powerdown 
        self.supply.outp_OFF(channel=1)
        print('Phase 4 Working')
        time.sleep(1)

        # self.startup.cirrus_PowerDown() # Run the buck powerup 
        # self.startup.IVM_Powerdown() # Run the buck powerup 
        self.startup.buck_PowerDown() # Run the buck powerdown 
        print('Device Driver passed')
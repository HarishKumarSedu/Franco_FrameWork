import pandas as pd 
import re 
from time import sleep
from Instruments.KeySight_N670x import N670x
from writeExcel import writeInExcel
from startup import Startup
from Franco_Test__APIs import FrancoAPIS
#from Instruments_API import Instruments
class Startup_read_curr:

    def __init__(self,dut):
        self.dut = dut
        self.supply = N670x(port='USB0::0x0957::0x0F07::MY50002157::INSTR')
        self.supply.setCurrRange(channel=1)
        self.supply.setCurrRange(channel=3)
        self.apis = FrancoAPIS(dut=dut)
        self.startup = Startup(dut=dut)

    def readCurr(self,ibat,ibus):
        sleep(1)
        ibat.append(self.supply.getCurrent(channel = 1))
        ibus.append(self.supply.getCurrent(channel = 3))
        print('ibat: ', ibat)
        print('ibus: ', ibus)
        sleep(1)
        return ibat,ibus

    def buck_startup_curr_meas(self,dut,filename='curr_meas/ibat_ibus_before_switching.xlsx',sheet='VBUS 15V'):
        ibat = []
        ibus = []
        self.dut = dut
        buck_startup =     [
    'Powerup',
    'self.dut.IVM.REG_PWRUP0_RW.DS_HVLDO_EN.value = 1  ',
    'self.dut.IVM.REG_PWRUP0_RW.DS_LDO1P8_PDNB.value = 1',
    'self.dut.IVM.REG_PWRUP0_RW.DS_REF_PDNB.value = 1   ',
    'self.dut.IVM.REG_PWRUP0_RW.DS_AON_EN_DETACH.value = 1',
    'self.dut.IVM.REG_PWRUP0_RW.DS_AON_EN_VDDSNS_OVP.value = 1',
    'self.dut.IVM.REG_PWRUP0_RW.DS_AON_EN_VBUS_OVP.value = 1',
    'self.dut.IVM.REG_PWRUP0_RW.DS_IFET_CP_SS_EN.value = 1',
    'self.dut.IVM.REG_PWRUP0_RW.DS_IFET_CP_EN.value = 1',
    'self.dut.IVM.REG_PWRUP0_RW.DS_IFET_CP_SS_EN.value = 0',
    'self.dut.IVM.REG_PWRUP0_RW.DS_NEGCP_EN.value = 1',
    'self.dut.IVM.REG_IFET_RW.DS_NEGCP_EN_SOFTSTART.value = 0',
    'self.dut.IVM.REG_PWRUP0_RW.DS_IFET_EN.value = 1',
    'self.dut.IVM.REG_PWRUP0_RW.DS_IFET_EN_DEL_DN.value = 1',
    'self.dut.IVM.REG_PWRUP0_RW.DS_IFET_IBUS_EN.value = 1',
    'self.dut.IVM.REG_PWRUP0_RW.DS_IFET_IBUS_EN_D.value = 1',
    'self.dut.IVM.REG_PWRUP0_RW.DS_PH13_INDCS_EN_BUF.value = 1',
    'self.dut.IVM.REG_PWRUP0_RW.DS_PH24_INDCS_EN_BUF.value = 1',
    'self.dut.IVM.REG_PWRUP1_RW.DS_PH1_DRV_BST_EN.value = 1',
    'self.dut.IVM.REG_PWRUP2_RW.DS_PH1_DRV_BST12_EN.value = 1',
    'self.dut.IVM.REG_PWRUP2_RW.TEMP_ENABLE.value = 1',
    'self.dut.IVM.REG_PWRUP1_RW.DS_PH1_INDCS_PP_EN.value = 1',
    'self.dut.IVM.REG_PWRUP1_RW.DS_PH1_INDCS_PP_EN_D.value = 1',
    'self.dut.IVM.REG_PWRUP0_RW.DS_PH1_CFLY_SENSE_EN.value = 1',
    'self.dut.IVM.REG_PWRUP0_RW.DS_PH1_CFLY_SENSE_EN_D.value = 1',
    'self.dut.IVM.REG_PWRUP0_RW.DS_PH1_CFLY_EN_CHG.value = 1',
    'self.dut.IVM.REG_PWRUP0_RW.DS_PH1_CFLY_EN_CHG_D.value = 1',
    'self.dut.IVM.REG_PWRUP1_RW.DS_PH2_DRV_BST_EN.value = 1',
    'self.dut.IVM.REG_PWRUP2_RW.DS_PH2_DRV_BST12_EN.value = 1',
    'self.dut.IVM.REG_PWRUP1_RW.DS_PH2_INDCS_PP_EN.value = 1',
    'self.dut.IVM.REG_PWRUP1_RW.DS_PH2_INDCS_PP_EN_D.value = 1',
    'self.dut.IVM.REG_PWRUP0_RW.DS_PH2_CFLY_SENSE_EN.value = 1',
    'self.dut.IVM.REG_PWRUP0_RW.DS_PH2_CFLY_SENSE_EN_D.value = 1',
    'self.dut.IVM.REG_PWRUP0_RW.DS_PH2_CFLY_EN_CHG.value = 1',
    'self.dut.IVM.REG_PWRUP0_RW.DS_PH2_CFLY_EN_CHG_D.value = 1',
    'self.dut.IVM.REG_PWRUP1_RW.DS_PH3_DRV_BST_EN.value = 1',
    'self.dut.IVM.REG_PWRUP2_RW.DS_PH3_DRV_BST12_EN.value = 1',
    'self.dut.IVM.REG_PWRUP1_RW.DS_PH3_INDCS_PP_EN.value = 1',
    'self.dut.IVM.REG_PWRUP1_RW.DS_PH3_INDCS_PP_EN_D.value = 1',
    'self.dut.IVM.REG_PWRUP0_RW.DS_PH3_CFLY_SENSE_EN.value = 1',
    'self.dut.IVM.REG_PWRUP0_RW.DS_PH3_CFLY_SENSE_EN_D.value = 1',
    'self.dut.IVM.REG_PWRUP0_RW.DS_PH3_CFLY_EN_CHG.value = 1',
    'self.dut.IVM.REG_PWRUP0_RW.DS_PH3_CFLY_EN_CHG_D.value = 1',
    'self.dut.IVM.REG_PWRUP1_RW.DS_PH4_DRV_BST_EN.value = 1',
    'self.dut.IVM.REG_PWRUP2_RW.DS_PH4_DRV_BST12_EN.value = 1',
    'self.dut.IVM.REG_PWRUP1_RW.DS_PH4_INDCS_PP_EN.value = 1',
    'self.dut.IVM.REG_PWRUP1_RW.DS_PH4_INDCS_PP_EN_D.value = 1',
    'self.dut.IVM.REG_PWRUP0_RW.DS_PH4_CFLY_SENSE_EN.value = 1',
    'self.dut.IVM.REG_PWRUP0_RW.DS_PH4_CFLY_SENSE_EN_D.value = 1',
    'self.dut.IVM.REG_PWRUP0_RW.DS_PH4_CFLY_EN_CHG.value = 1',
    'self.dut.IVM.REG_PWRUP0_RW.DS_PH4_CFLY_EN_CHG_D.value = 1',
    'self.dut.IVM.REG_PWRUP2_RW.DS_INDCS_BUCK_MODE.value = 1',
    'self.dut.IVM.REG_PWRUP1_RW.DS_PH1_INDCS_PP_EN_D.value = 1',
    'self.dut.IVM.REG_PWRUP0_RW.DS_PH1_CFLY_SENSE_EN_D.value = 1',
    'self.dut.IVM.REG_PWRUP0_RW.DS_PH1_CFLY_EN_CHG_D.value = 1',
    'self.dut.IVM.REG_PWRUP1_RW.DS_PH2_INDCS_PP_EN_D.value = 1',
    'self.dut.IVM.REG_PWRUP0_RW.DS_PH2_CFLY_SENSE_EN_D.value = 1',
    'self.dut.IVM.REG_PWRUP0_RW.DS_PH2_CFLY_EN_CHG_D.value = 1',
    'self.dut.IVM.REG_PWRUP1_RW.DS_PH3_INDCS_PP_EN_D.value = 1',
    'self.dut.IVM.REG_PWRUP0_RW.DS_PH3_CFLY_SENSE_EN_D.value = 1',
    'self.dut.IVM.REG_PWRUP0_RW.DS_PH3_CFLY_EN_CHG_D.value = 1',
    'self.dut.IVM.REG_PWRUP1_RW.DS_PH4_INDCS_PP_EN_D.value = 1',
    'self.dut.IVM.REG_PWRUP0_RW.DS_PH4_CFLY_SENSE_EN_D.value = 1',
    'self.dut.IVM.REG_PWRUP0_RW.DS_PH4_CFLY_EN_CHG_D.value = 1',
    'self.dut.IVM.REG_PWRUP2_RW.DS_INDCS_CLR_OCP.value = 0',
    'self.dut.IVM.REG_PWRUP1_RW.DS_PH1_INDCS_FORCE_AZ.value = 0',
    'self.dut.IVM.REG_PWRUP1_RW.DS_PH2_INDCS_FORCE_AZ.value = 0',
    'self.dut.IVM.REG_PWRUP1_RW.DS_PH3_INDCS_FORCE_AZ.value = 0',
    'self.dut.IVM.REG_PWRUP1_RW.DS_PH4_INDCS_FORCE_AZ.value = 0',
    'self.dut.IVM.REG_PWRUP2_RW.DS_PH1_INDCS_REPLICA_AON.value = 1',
    'self.dut.IVM.REG_PWRUP1_RW.DS_PH1_INDCS_EN_OCP.value = 0',
    'self.dut.IVM.REG_PWRUP1_RW.DS_PH1_INDCS_EN_ZC.value = 1',
    'self.dut.IVM.REG_PWRUP1_RW.DS_PH2_INDCS_EN_OCP.value = 0',
    'self.dut.IVM.REG_PWRUP1_RW.DS_PH2_INDCS_EN_ZC.value = 1',
    'self.dut.IVM.REG_PWRUP1_RW.DS_PH3_INDCS_EN_OCP.value = 0',
    'self.dut.IVM.REG_PWRUP1_RW.DS_PH3_INDCS_EN_ZC.value = 1',
    'self.dut.IVM.REG_PWRUP1_RW.DS_PH4_INDCS_EN_OCP.value = 0',
    'self.dut.IVM.REG_PWRUP1_RW.DS_PH4_INDCS_EN_ZC.value = 1',
    'self.dut.IVM.REG_PWRUP2_RW.DS_PH1_DRV_BOOST_PRCHG_LSH_EN.value = 1',
    'self.dut.IVM.REG_PWRUP1_RW.DS_PH1_DRV_EN.value = 1',
    'self.dut.IVM.REG_PWRUP1_RW.DS_PH1_DRV_EN_D.value = 1',
    'self.dut.IVM.REG_PWRUP2_RW.DS_PH2_DRV_BOOST_PRCHG_LSH_EN.value = 1',
    'self.dut.IVM.REG_PWRUP1_RW.DS_PH2_DRV_EN.value = 1',
    'self.dut.IVM.REG_PWRUP1_RW.DS_PH2_DRV_EN_D.value = 1',
    'self.dut.IVM.REG_PWRUP2_RW.DS_PH3_DRV_BOOST_PRCHG_LSH_EN.value = 1',
    'self.dut.IVM.REG_PWRUP1_RW.DS_PH3_DRV_EN.value = 1',
    'self.dut.IVM.REG_PWRUP1_RW.DS_PH3_DRV_EN_D.value = 1',
    'self.dut.IVM.REG_PWRUP2_RW.DS_PH4_DRV_BOOST_PRCHG_LSH_EN.value = 1',
    'self.dut.IVM.REG_PWRUP1_RW.DS_PH4_DRV_EN.value = 1',
    'self.dut.IVM.REG_PWRUP1_RW.DS_PH4_DRV_EN_D.value = 1',]
        sleep(5)
        self.readCurr(ibat,ibus) 
        self.dut.IVM.REG_PWRUP0_RW.DS_HVLDO_EN.value = 1 
        sleep(5)
        self.readCurr(ibat,ibus) 
        self.dut.IVM.REG_PWRUP0_RW.DS_LDO1P8_PDNB.value = 1 
        sleep(5)
        self.readCurr(ibat,ibus)     
        self.dut.IVM.REG_PWRUP0_RW.DS_REF_PDNB.value = 1 
        sleep(5)
        self.readCurr(ibat,ibus)    
        self.dut.IVM.REG_PWRUP0_RW.DS_AON_EN_DETACH.value = 1  
        sleep(5) 
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP0_RW.DS_AON_EN_VDDSNS_OVP.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP0_RW.DS_AON_EN_VBUS_OVP.value = 1
        sleep(5) 
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP0_RW.DS_IFET_CP_SS_EN.value = 1
        sleep(5)  
        self.readCurr(ibat,ibus)  
        self.dut.IVM.REG_PWRUP0_RW.DS_IFET_CP_EN.value = 1 
        sleep(5)
        self.readCurr(ibat,ibus)     
        self.dut.IVM.REG_PWRUP0_RW.DS_IFET_CP_SS_EN.value = 0 
        sleep(5)
        self.readCurr(ibat,ibus)   
        self.dut.IVM.REG_PWRUP0_RW.DS_NEGCP_EN.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_IFET_RW.DS_NEGCP_EN_SOFTSTART.value = 0
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP0_RW.DS_IFET_EN.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP0_RW.DS_IFET_EN_DEL_DN.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP0_RW.DS_IFET_IBUS_EN.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP0_RW.DS_IFET_IBUS_EN_D.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP0_RW.DS_PH13_INDCS_EN_BUF.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP0_RW.DS_PH24_INDCS_EN_BUF.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP1_RW.DS_PH1_DRV_BST_EN.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP2_RW.DS_PH1_DRV_BST12_EN.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP2_RW.TEMP_ENABLE.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP1_RW.DS_PH1_INDCS_PP_EN.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP1_RW.DS_PH1_INDCS_PP_EN_D.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP0_RW.DS_PH1_CFLY_SENSE_EN.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP0_RW.DS_PH1_CFLY_SENSE_EN_D.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP0_RW.DS_PH1_CFLY_EN_CHG.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP0_RW.DS_PH1_CFLY_EN_CHG_D.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP1_RW.DS_PH2_DRV_BST_EN.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP2_RW.DS_PH2_DRV_BST12_EN.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP1_RW.DS_PH2_INDCS_PP_EN.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP1_RW.DS_PH2_INDCS_PP_EN_D.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP0_RW.DS_PH2_CFLY_SENSE_EN.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP0_RW.DS_PH2_CFLY_SENSE_EN_D.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP0_RW.DS_PH2_CFLY_EN_CHG.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP0_RW.DS_PH2_CFLY_EN_CHG_D.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP1_RW.DS_PH3_DRV_BST_EN.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP2_RW.DS_PH3_DRV_BST12_EN.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP1_RW.DS_PH3_INDCS_PP_EN.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP1_RW.DS_PH3_INDCS_PP_EN_D.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP0_RW.DS_PH3_CFLY_SENSE_EN.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP0_RW.DS_PH3_CFLY_SENSE_EN_D.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP0_RW.DS_PH3_CFLY_EN_CHG.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP0_RW.DS_PH3_CFLY_EN_CHG_D.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP1_RW.DS_PH4_DRV_BST_EN.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP2_RW.DS_PH4_DRV_BST12_EN.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP1_RW.DS_PH4_INDCS_PP_EN.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP1_RW.DS_PH4_INDCS_PP_EN_D.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP0_RW.DS_PH4_CFLY_SENSE_EN.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)  
        self.dut.IVM.REG_PWRUP0_RW.DS_PH4_CFLY_SENSE_EN_D.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP0_RW.DS_PH4_CFLY_EN_CHG.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP0_RW.DS_PH4_CFLY_EN_CHG_D.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP2_RW.DS_INDCS_BUCK_MODE.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP1_RW.DS_PH1_INDCS_PP_EN_D.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP0_RW.DS_PH1_CFLY_SENSE_EN_D.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP0_RW.DS_PH1_CFLY_EN_CHG_D.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP1_RW.DS_PH2_INDCS_PP_EN_D.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP0_RW.DS_PH2_CFLY_SENSE_EN_D.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP0_RW.DS_PH2_CFLY_EN_CHG_D.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP1_RW.DS_PH3_INDCS_PP_EN_D.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP0_RW.DS_PH3_CFLY_SENSE_EN_D.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP0_RW.DS_PH3_CFLY_EN_CHG_D.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP1_RW.DS_PH4_INDCS_PP_EN_D.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP0_RW.DS_PH4_CFLY_SENSE_EN_D.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP0_RW.DS_PH4_CFLY_EN_CHG_D.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP2_RW.DS_INDCS_CLR_OCP.value = 0
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP1_RW.DS_PH1_INDCS_FORCE_AZ.value = 0
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP1_RW.DS_PH2_INDCS_FORCE_AZ.value = 0
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP1_RW.DS_PH3_INDCS_FORCE_AZ.value = 0
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP1_RW.DS_PH4_INDCS_FORCE_AZ.value = 0
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP2_RW.DS_PH1_INDCS_REPLICA_AON.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP1_RW.DS_PH1_INDCS_EN_OCP.value = 0
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP1_RW.DS_PH1_INDCS_EN_ZC.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP1_RW.DS_PH2_INDCS_EN_OCP.value = 0
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP1_RW.DS_PH2_INDCS_EN_ZC.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP1_RW.DS_PH3_INDCS_EN_OCP.value = 0
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP1_RW.DS_PH3_INDCS_EN_ZC.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP1_RW.DS_PH4_INDCS_EN_OCP.value = 0
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP1_RW.DS_PH4_INDCS_EN_ZC.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP2_RW.DS_PH1_DRV_BOOST_PRCHG_LSH_EN.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP1_RW.DS_PH1_DRV_EN.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP1_RW.DS_PH1_DRV_EN_D.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP2_RW.DS_PH2_DRV_BOOST_PRCHG_LSH_EN.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP1_RW.DS_PH2_DRV_EN.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP1_RW.DS_PH2_DRV_EN_D.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP2_RW.DS_PH3_DRV_BOOST_PRCHG_LSH_EN.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP1_RW.DS_PH3_DRV_EN.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP1_RW.DS_PH3_DRV_EN_D.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP2_RW.DS_PH4_DRV_BOOST_PRCHG_LSH_EN.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP1_RW.DS_PH4_DRV_EN.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        self.dut.IVM.REG_PWRUP1_RW.DS_PH4_DRV_EN_D.value = 1
        sleep(5)
        self.readCurr(ibat,ibus)
        writeInExcel(ibat=ibat,ibus=ibus,sheet=sheet,filename=filename,buck_startup=buck_startup)

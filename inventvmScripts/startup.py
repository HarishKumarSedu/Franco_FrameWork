
import pandas as pd 
import re 

class Startup:

    def __init__(self,dut):
        self.dut = dut
        self.regmap = pd.read_csv('chip_validation_regs.csv')


    def buck_PowerUp(self):
    
        # startup_fields = {
        #        "DS_HVLDO_EN"": 1,
        #        "DS_LDO1P8_PDNB"": 1,
        #        "DS_REF_PDNB"": 1,
        #        "DS_REF_TEMPADC_PDNB"": 1,
        #        "DS_AON_EN_DETACH"": 1, 
        #        "DS_AON_EN_VDDSNS_OVP"": 1, 
        #        "DS_AON_EN_VBUS_OVP"": 1,
        #        "DS_IFET_CP_SS_EN"":1,,
        #        "DS_IFET_CP_EN"": 1,
        #        "DS_IFET_CP_SS_EN"":0,,
        #        "DS_NEGCP_EN"": 1,
        #        "DS_IFET_EN"": 1,
        #        "DS_IFET_EN_DEL_DN"": 1,
        #        "DS_IFET_IBUS_EN"": 1,
        #        "DS_IFET_IBUS_EN_D"": 1,
        #        "DS_PH1_DRV_BST_EN"": 1,
        #        "DS_PH1_DRV_BST12_EN"": 1,
        #        "DS_PH1_INDCS_PP_EN"": 1,
        #        "DS_PH1_CFLY_SENSE_EN"":1,,
        #        "DS_PH1_CFLY_EN_CHG"":1,,
        #        "DS_PH2_DRV_BST_EN"": 1,
        #        "DS_PH2_DRV_BST12_EN"": 1,
        #        "DS_PH2_INDCS_PP_EN"": 1,
        #        "DS_PH2_CFLY_SENSE_EN"":1,,
        #        "DS_PH2_CFLY_EN_CHG"":1,,
        #        "DS_PH3_DRV_BST_EN"": 1,
        #        "DS_PH3_DRV_BST12_EN"": 1,
        #        "DS_PH3_INDCS_PP_EN"": 1,
        #        "DS_PH3_CFLY_SENSE_EN"":1,,
        #        "DS_PH3_CFLY_EN_CHG"":1,,
        #        "DS_PH4_DRV_BST_EN"": 1,
        #        "DS_PH4_DRV_BST12_EN"": 1,
        #        "DS_PH4_INDCS_PP_EN"": 1,
        #        "DS_PH4_CFLY_SENSE_EN"":1,,
        #        "DS_PH4_CFLY_EN_CHG"":1,,
        #        "DS_INDCS_BUCK_MODE"": 1,
        #        "DS_PH1_INDCS_PP_EN_D"": 1,
        #        "DS_PH1_CFLY_SENSE_EN_D"": 1,
        #        "DS_PH1_CFLY_EN_CHG_D"":1,,
        #        "DS_PH2_INDCS_PP_EN_D"": 1,
        #        "DS_PH2_CFLY_SENSE_EN_D"": 1,
        #        "DS_PH2_CFLY_EN_CHG_D"":1,,
        #        "DS_PH3_INDCS_PP_EN_D"": 1,
        #        "DS_PH3_CFLY_SENSE_EN_D"": 1,
        #        "DS_PH3_CFLY_EN_CHG_D"":1,,
        #        "DS_PH4_INDCS_PP_EN_D"": 1,
        #        "DS_PH4_CFLY_SENSE_EN_D"": 1,
        #        "DS_PH4_CFLY_EN_CHG_D"":1,,
        #        "DS_INDCS_CLR_OCP"": 1,
        #        "DS_PH1_INDCS_FORCE_AZ"": 1,
        #        "DS_PH1_INDCS_EN_BUF"": 1,
        #        "DS_PH2_INDCS_FORCE_AZ"": 1,
        #        "DS_PH2_INDCS_EN_BUF"": 1,
        #        "DS_PH3_INDCS_FORCE_AZ"": 1,
        #        "DS_PH3_INDCS_EN_BUF"": 1,
        #        "DS_PH4_INDCS_FORCE_AZ"": 1,
        #        "DS_PH4_INDCS_EN_BUF"": 1,
        #        "DS_PH1_INDCS_REPLICA_AON"":1,,
        #        "DS_PH1_INDCS_EN_OCP"": 1,
        #        "DS_PH1_INDCS_EN_ZC"": 1,
        #        "DS_PH2_INDCS_EN_OCP"": 1,
        #        "DS_PH2_INDCS_EN_ZC"": 1,
        #        "DS_PH3_INDCS_EN_OCP"": 1,
        #        "DS_PH3_INDCS_EN_ZC"": 1,
        #        "DS_PH4_INDCS_EN_OCP"": 1,
        #        "DS_PH4_INDCS_EN_ZC"": 1,
        #        "DS_INDCS_CLR_OCP"": 0,
        #        "DS_PH1_DRV_BOOST_PRCHG_LSH_EN"": 1,
        #        "DS_PH1_DRV_EN"": 1,
        #        "DS_PH1_INDCS_FORCE_AZ"": 0,
        #        "DS_PH1_DRV_EN_D"": 1,
        #        "DS_PH2_DRV_BOOST_PRCHG_LSH_EN"": 1,
        #        "DS_PH2_DRV_EN"": 1,
        #        "DS_PH2_INDCS_FORCE_AZ"": 0,
        #        "DS_PH2_DRV_EN_D"": 1,
        #        "DS_PH3_DRV_BOOST_PRCHG_LSH_EN"": 1,
        #        "DS_PH3_DRV_EN"": 1,
        #        "DS_PH3_INDCS_FORCE_AZ"": 0,
        #        "DS_PH3_DRV_EN_D"": 1,
        #        "DS_PH4_DRV_BOOST_PRCHG_LSH_EN"": 1,
        #        "DS_PH4_DRV_EN"": 1,
        #        "DS_PH4_INDCS_FORCE_AZ"": 0,
        #        "DS_PH4_DRV_EN_D"": 1,
        #         }
        # for fieldName,value in startup_fields.items()":
        #     for i in list(self.regmap['FIELD NAME'])":
                
        #         if fieldName in i":
        #             print('self.dut.',i.lstrip(),'.value =',value)

        self.dut.IVM.REG_PWRUP0_RW.DS_HVLDO_EN.value = 1   
        self.dut.IVM.REG_PWRUP0_RW.DS_LDO1P8_PDNB.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_REF_PDNB.value = 1   
        self.dut.IVM.REG_PWRUP0_RW.DS_AON_EN_DETACH.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_AON_EN_VDDSNS_OVP.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_AON_EN_VBUS_OVP.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_IFET_CP_SS_EN.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_IFET_CP_EN.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_NEGCP_EN.value = 1
        self.dut.IVM.REG_IFET_RW.DS_NEGCP_EN_SOFTSTART.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_IFET_EN.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_IFET_EN_DEL_DN.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_IFET_EN_DEL_DN.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_IFET_IBUS_EN.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_IFET_IBUS_EN_D.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_IFET_IBUS_EN_D.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_PH13_INDCS_EN_BUF.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_PH24_INDCS_EN_BUF.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH1_DRV_BST_EN.value = 1
        self.dut.IVM.REG_PWRUP2_RW.DS_PH1_DRV_BST12_EN.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH1_INDCS_PP_EN.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH1_INDCS_PP_EN_D.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_PH1_CFLY_SENSE_EN.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_PH1_CFLY_SENSE_EN_D.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_PH1_CFLY_EN_CHG.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_PH1_CFLY_EN_CHG_D.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH2_DRV_BST_EN.value = 1
        self.dut.IVM.REG_PWRUP2_RW.DS_PH2_DRV_BST12_EN.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH2_INDCS_PP_EN.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH2_INDCS_PP_EN_D.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_PH2_CFLY_SENSE_EN.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_PH2_CFLY_SENSE_EN_D.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_PH2_CFLY_EN_CHG.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_PH2_CFLY_EN_CHG_D.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH3_DRV_BST_EN.value = 1
        self.dut.IVM.REG_PWRUP2_RW.DS_PH3_DRV_BST12_EN.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH3_INDCS_PP_EN.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH3_INDCS_PP_EN_D.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_PH3_CFLY_SENSE_EN.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_PH3_CFLY_SENSE_EN_D.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_PH3_CFLY_EN_CHG.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_PH3_CFLY_EN_CHG_D.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH4_DRV_BST_EN.value = 1
        self.dut.IVM.REG_PWRUP2_RW.DS_PH4_DRV_BST12_EN.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH4_INDCS_PP_EN.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH4_INDCS_PP_EN_D.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_PH4_CFLY_SENSE_EN.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_PH4_CFLY_SENSE_EN_D.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_PH4_CFLY_EN_CHG.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_PH4_CFLY_EN_CHG_D.value = 1
        self.dut.IVM.REG_PWRUP2_RW.DS_INDCS_BUCK_MODE.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH1_INDCS_PP_EN_D.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_PH1_CFLY_SENSE_EN_D.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_PH1_CFLY_EN_CHG_D.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH2_INDCS_PP_EN_D.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_PH2_CFLY_SENSE_EN_D.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_PH2_CFLY_EN_CHG_D.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH3_INDCS_PP_EN_D.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_PH3_CFLY_SENSE_EN_D.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_PH3_CFLY_EN_CHG_D.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH4_INDCS_PP_EN_D.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_PH4_CFLY_SENSE_EN_D.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_PH4_CFLY_EN_CHG_D.value = 1
        self.dut.IVM.REG_PWRUP2_RW.DS_INDCS_CLR_OCP.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH1_INDCS_FORCE_AZ.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH2_INDCS_FORCE_AZ.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH3_INDCS_FORCE_AZ.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH4_INDCS_FORCE_AZ.value = 0
        self.dut.IVM.REG_PWRUP2_RW.DS_PH1_INDCS_REPLICA_AON.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH1_INDCS_EN_OCP.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH1_INDCS_EN_ZC.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH2_INDCS_EN_OCP.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH2_INDCS_EN_ZC.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH3_INDCS_EN_OCP.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH3_INDCS_EN_ZC.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH4_INDCS_EN_OCP.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH4_INDCS_EN_ZC.value = 1
        self.dut.IVM.REG_PWRUP2_RW.DS_PH1_DRV_BOOST_PRCHG_LSH_EN.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH1_DRV_EN.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH1_DRV_EN_D.value = 1
        self.dut.IVM.REG_PWRUP2_RW.DS_PH2_DRV_BOOST_PRCHG_LSH_EN.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH2_DRV_EN.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH2_DRV_EN_D.value = 1
        self.dut.IVM.REG_PWRUP2_RW.DS_PH3_DRV_BOOST_PRCHG_LSH_EN.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH3_DRV_EN.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH3_DRV_EN_D.value = 1
        self.dut.IVM.REG_PWRUP2_RW.DS_PH4_DRV_BOOST_PRCHG_LSH_EN.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH4_DRV_EN.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH4_DRV_EN_D.value = 1

    def boost_PowerUp(self):
        # boost_startup__fields = {
        # "DS_HVLDO_EN":1,
        # "DS_LDO1P8_PDNB":1,
        # "DS_REF_PDNB":1,
        # "DS_REF_TEMPADC_PDNB":1,
        # "DS_AON_EN_DETACH":0, 
        # "DS_AON_EN_VDDSNS_OVP":1, 
        # "DS_AON_EN_VBUS_OVP":1,
        # "DS_IFET_CP_SS_EN":1,
        # "DS_IFET_CP_EN":1,
        # "DS_IFET_CP_SS_EN":0,
        # "DS_NEGCP_EN":1,
        # "DS_PH1_DRV_BOOST_PRCHG_LSH_EN":1,
        # "DS_DRV_PRCHG_MODE_SEL":1,
        # "DS_PH1_DRV_BST_EN":1,
        # "DS_PH1_DRV_BST12_EN":1,
        # "DS_PH1_DRV_BST2_POR_BOOST":1,
        # "DS_PH1_DRV_BST2_WPU":1,
        # "DS_PH1_DRV_WPU_EN":1,
        # "DS_PH1_DRV_EN":1,
        # "DS_PH1_DRV_EN_D":1,
        # "DS_PH1_INDCS_PP_EN":1,
        # "DS_PH1_CFLY_SENSE_EN":1,
        # "DS_PH1_CFLY_EN_CHG":1,
        # "DS_PH1_DRV_WPU_EN":0,
        # "DS_DRV_PRCHG_MODE_SEL":0,
        # "DS_PH1_DRV_BST2_WPU":0,
        # "DS_INDCS_BUCK_MODE":0,
        # "DS_PH1_INDCS_PP_EN_D":1,
        # "DS_PH1_CFLY_SENSE_EN_D":1,
        # "DS_PH1_CFLY_EN_CHG_D":1,
        # "DS_PH1_INDCS_REPLICA_AON":1,
        # "DS_PH1_INDCS_FORCE_AZ":1,
        # "DS_PH1_INDCS_EN_BUF":1,
        # "DS_INDCS_CLR_OCP":1,
        # "DS_PH1_INDCS_EN_OCP":1,
        # "DS_PH1_INDCS_EN_ZC":1,
        # "DS_INDCS_CLR_OCP":0,
        # "DS_PH1_INDCS_FORCE_AZ":0,
        # "DS_IFET_EN":1,
        # "DS_IFET_EN_DEL_DN":1,
        # "DS_PH1_INDCS_FORCE_AZ":0,
        # "DS_PH2_DRV_BOOST_PRCHG_LSH_EN":1,
        # "DS_DRV_PRCHG_MODE_SEL":1,
        # "DS_PH2_DRV_BST_EN":1,
        # "DS_PH2_DRV_BST12_EN":1,
        # "DS_PH2_DRV_BST2_POR_BOOST":1,
        # "DS_PH2_DRV_BST2_WPU":1,
        # "DS_PH2_DRV_WPU_EN":1,
        # "DS_PH2_DRV_EN":1,
        # "DS_PH2_DRV_EN_D":1,
        # "DS_PH2_INDCS_PP_EN":1,
        # "DS_PH2_CFLY_SENSE_EN":1,
        # "DS_PH2_CFLY_EN_CHG":1,
        # "DS_PH2_DRV_WPU_EN":0,
        # "DS_DRV_PRCHG_MODE_SEL":0,
        # "DS_PH2_DRV_BST2_WPU":0,
        # "DS_INDCS_BUCK_MODE":0,
        # "DS_PH2_INDCS_PP_EN_D":1,
        # "DS_PH2_CFLY_SENSE_EN_D":1,
        # "DS_PH2_CFLY_EN_CHG_D":1,
        # "DS_PH1_INDCS_REPLICA_AON":1,
        # "DS_PH2_INDCS_FORCE_AZ":1,
        # "DS_PH2_INDCS_EN_BUF":1,
        # "DS_INDCS_CLR_OCP":1,
        # "DS_PH2_INDCS_EN_OCP":1,
        # "DS_PH2_INDCS_EN_ZC":1,
        # "DS_INDCS_CLR_OCP":0,
        # "DS_PH2_INDCS_FORCE_AZ":0,
        # "DS_IFET_EN":1,
        # "DS_IFET_EN_DEL_DN":1,
        # "DS_PH2_INDCS_FORCE_AZ":0,
        # "DS_PH3_DRV_BOOST_PRCHG_LSH_EN":1,
        # "DS_DRV_PRCHG_MODE_SEL":1,
        # "DS_PH3_DRV_BST_EN":1,
        # "DS_PH3_DRV_BST12_EN":1,
        # "DS_PH3_DRV_BST2_POR_BOOST":1,
        # "DS_PH3_DRV_BST2_WPU":1,
        # "DS_PH3_DRV_WPU_EN":1,
        # "DS_PH3_DRV_EN":1,
        # "DS_PH3_DRV_EN_D":1,
        # "DS_PH3_INDCS_PP_EN":1,
        # "DS_PH3_CFLY_SENSE_EN":1,
        # "DS_PH3_CFLY_EN_CHG":1,
        # "DS_PH3_DRV_WPU_EN":0,
        # "DS_DRV_PRCHG_MODE_SEL":0,
        # "DS_PH3_DRV_BST2_WPU":0,
        # "DS_INDCS_BUCK_MODE":0,
        # "DS_PH3_INDCS_PP_EN_D":1,
        # "DS_PH3_CFLY_SENSE_EN_D":1,
        # "DS_PH3_CFLY_EN_CHG_D":1,
        # "DS_PH1_INDCS_REPLICA_AON":1,
        # "DS_PH3_INDCS_FORCE_AZ":1,
        # "DS_PH3_INDCS_EN_BUF":1,
        # "DS_INDCS_CLR_OCP":1,
        # "DS_PH3_INDCS_EN_OCP":1,
        # "DS_PH3_INDCS_EN_ZC":1,
        # "DS_INDCS_CLR_OCP":0,
        # "DS_PH3_INDCS_FORCE_AZ":0,
        # "DS_IFET_EN":1,
        # "DS_IFET_EN_DEL_DN":1,
        # "DS_PH3_INDCS_FORCE_AZ":0,
        # "DS_PH4_DRV_BOOST_PRCHG_LSH_EN":1,
        # "DS_DRV_PRCHG_MODE_SEL":1,
        # "DS_PH4_DRV_BST_EN":1,
        # "DS_PH4_DRV_BST12_EN":1,
        # "DS_PH4_DRV_BST2_POR_BOOST":1,
        # "DS_PH4_DRV_BST2_WPU":1,
        # "DS_PH4_DRV_WPU_EN":1,
        # "DS_PH4_DRV_EN":1,
        # "DS_PH4_DRV_EN_D":1,
        # "DS_PH4_INDCS_PP_EN":1,
        # "DS_PH4_CFLY_SENSE_EN":1,
        # "DS_PH4_CFLY_EN_CHG":1,
        # "DS_PH4_DRV_WPU_EN":0,
        # "DS_DRV_PRCHG_MODE_SEL":0,
        # "DS_PH4_DRV_BST2_WPU":0,
        # "DS_INDCS_BUCK_MODE":0,
        # "DS_PH4_INDCS_PP_EN_D":1,
        # "DS_PH4_CFLY_SENSE_EN_D":1,
        # "DS_PH4_CFLY_EN_CHG_D":1,
        # "DS_PH1_INDCS_REPLICA_AON":1,
        # "DS_PH4_INDCS_FORCE_AZ":1,
        # "DS_PH4_INDCS_EN_BUF":1,
        # "DS_INDCS_CLR_OCP":1,
        # "DS_PH4_INDCS_EN_OCP":1,
        # "DS_PH4_INDCS_EN_ZC":1,
        # "DS_INDCS_CLR_OCP":0,
        # "DS_PH4_INDCS_FORCE_AZ":0,
        # "DS_IFET_EN":1,
        # "DS_IFET_EN_DEL_DN":1,
        # "DS_PH4_INDCS_FORCE_AZ":0,
        # }
        # for fieldName,value in boost_startup__fields.items():
        #     for i in list(self.regmap['FIELD NAME']):
                
        #         if fieldName in i.lstrip():
        #             print('self.dut.',i.lstrip(),'.value =',value)
        self.dut.IVM.REG_PWRUP0_RW.DS_HVLDO_EN.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_LDO1P8_PDNB.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_REF_PDNB.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_AON_EN_DETACH.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_AON_EN_VDDSNS_OVP.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_AON_EN_VBUS_OVP.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_IFET_CP_SS_EN.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_IFET_CP_EN.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_NEGCP_EN.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_PH1_INDCS_EN_BUF.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_PH1_INDCS_EN_BUF.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_PH13_INDCS_EN_BUF.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_PH24_INDCS_EN_BUF.value = 1
        self.dut.IVM.REG_IFET_RW.DS_NEGCP_EN_SOFTSTART.value = 1
        self.dut.IVM.REG_PWRUP2_RW.DS_PH1_DRV_BOOST_PRCHG_LSH_EN.value = 1
        self.dut.IVM.REG_PWRUP2_RW.DS_DRV_PRCHG_MODE_SEL.value = 0        
        self.dut.IVM.REG_PWRUP1_RW.DS_PH1_DRV_BST_EN.value = 1
        self.dut.IVM.REG_PWRUP2_RW.DS_PH1_DRV_BST12_EN.value = 1
        self.dut.IVM.REG_PWRUP2_RW.DS_PH1_DRV_BST2_POR_BOOST.value = 1    
        self.dut.IVM.REG_PWRUP2_RW.DS_PH1_DRV_BST2_WPU.value = 0
        self.dut.IVM.REG_PWRUP2_RW.DS_PH1_DRV_WPU_EN.value = 0 
        self.dut.IVM.REG_PWRUP1_RW.DS_PH1_DRV_EN.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH1_DRV_EN_D.value = 1 
        self.dut.IVM.REG_PWRUP1_RW.DS_PH1_DRV_EN_D.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH1_INDCS_PP_EN.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH1_INDCS_PP_EN_D.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_PH1_CFLY_SENSE_EN.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_PH1_CFLY_SENSE_EN_D.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_PH1_CFLY_EN_CHG.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_PH1_CFLY_EN_CHG_D.value = 1
        self.dut.IVM.REG_PWRUP2_RW.DS_INDCS_BUCK_MODE.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH1_INDCS_PP_EN_D.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_PH1_CFLY_SENSE_EN_D.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_PH1_CFLY_EN_CHG_D.value = 1
        self.dut.IVM.REG_PWRUP2_RW.DS_PH1_INDCS_REPLICA_AON.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH1_INDCS_FORCE_AZ.value = 0
        self.dut.IVM.REG_PWRUP2_RW.DS_INDCS_CLR_OCP.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH1_INDCS_EN_OCP.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH1_INDCS_EN_ZC.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_IFET_EN.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_IFET_EN_DEL_DN.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_IFET_EN_DEL_DN.value = 1
        self.dut.IVM.REG_PWRUP2_RW.DS_PH2_DRV_BOOST_PRCHG_LSH_EN.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH2_DRV_BST_EN.value = 1
        self.dut.IVM.REG_PWRUP2_RW.DS_PH2_DRV_BST12_EN.value = 1
        self.dut.IVM.REG_PWRUP2_RW.DS_PH2_DRV_BST2_POR_BOOST.value = 1
        self.dut.IVM.REG_PWRUP2_RW.DS_PH2_DRV_BST2_WPU.value = 0
        self.dut.IVM.REG_PWRUP2_RW.DS_PH2_DRV_WPU_EN.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH2_DRV_EN.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH2_DRV_EN_D.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH2_DRV_EN_D.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH2_INDCS_PP_EN.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH2_INDCS_PP_EN_D.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_PH2_CFLY_SENSE_EN.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_PH2_CFLY_SENSE_EN_D.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_PH2_CFLY_EN_CHG.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_PH2_CFLY_EN_CHG_D.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH2_INDCS_PP_EN_D.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_PH2_CFLY_SENSE_EN_D.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_PH2_CFLY_EN_CHG_D.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH2_INDCS_FORCE_AZ.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH2_INDCS_EN_OCP.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH2_INDCS_EN_ZC.value = 1
        self.dut.IVM.REG_PWRUP2_RW.DS_PH3_DRV_BOOST_PRCHG_LSH_EN.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH3_DRV_BST_EN.value = 1
        self.dut.IVM.REG_PWRUP2_RW.DS_PH3_DRV_BST12_EN.value = 1
        self.dut.IVM.REG_PWRUP2_RW.DS_PH3_DRV_BST2_POR_BOOST.value = 1
        self.dut.IVM.REG_PWRUP2_RW.DS_PH3_DRV_BST2_WPU.value = 0
        self.dut.IVM.REG_PWRUP2_RW.DS_PH3_DRV_WPU_EN.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH3_DRV_EN.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH3_DRV_EN_D.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH3_DRV_EN_D.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH3_INDCS_PP_EN.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH3_INDCS_PP_EN_D.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_PH3_CFLY_SENSE_EN.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_PH3_CFLY_SENSE_EN_D.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_PH3_CFLY_EN_CHG.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_PH3_CFLY_EN_CHG_D.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH3_INDCS_PP_EN_D.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_PH3_CFLY_SENSE_EN_D.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_PH3_CFLY_EN_CHG_D.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH3_INDCS_FORCE_AZ.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH3_INDCS_EN_OCP.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH3_INDCS_EN_ZC.value = 1
        self.dut.IVM.REG_PWRUP2_RW.DS_PH4_DRV_BOOST_PRCHG_LSH_EN.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH4_DRV_BST_EN.value = 1
        self.dut.IVM.REG_PWRUP2_RW.DS_PH4_DRV_BST12_EN.value = 1
        self.dut.IVM.REG_PWRUP2_RW.DS_PH4_DRV_BST2_POR_BOOST.value = 1
        self.dut.IVM.REG_PWRUP2_RW.DS_PH4_DRV_BST2_WPU.value = 0
        self.dut.IVM.REG_PWRUP2_RW.DS_PH4_DRV_WPU_EN.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH4_DRV_EN.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH4_DRV_EN_D.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH4_DRV_EN_D.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH4_INDCS_PP_EN.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH4_INDCS_PP_EN_D.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_PH4_CFLY_SENSE_EN.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_PH4_CFLY_SENSE_EN_D.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_PH4_CFLY_EN_CHG.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_PH4_CFLY_EN_CHG_D.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH4_INDCS_PP_EN_D.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_PH4_CFLY_SENSE_EN_D.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_PH4_CFLY_EN_CHG_D.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH4_INDCS_FORCE_AZ.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH4_INDCS_EN_OCP.value = 1
        self.dut.IVM.REG_PWRUP1_RW.DS_PH4_INDCS_EN_ZC.value = 1

    def buck_PowerDown(self):
#         buck_powerdown_startup__fields = {
#  "DS_PH1_DRV_EN_D":0,
# "DS_PH1_DRV_BOOST_PRCHG_LSH_EN":0,
# "DS_PH1_DRV_EN":0,
# "DS_PH1_INDCS_EN_OCP":0,
# "DS_PH1_INDCS_EN_ZC":0,
# "DS_PH1_INDCS_PP_EN_D":0,
# "DS_PH1_CFLY_SENSE_EN_D":0,
# "DS_PH1_CFLY_EN_CHG_D":0,
# "DS_PH1_INDCS_EN_BUF":0,
# "DS_PH1_INDCS_PP_EN":0,
# "DS_PH1_CFLY_SENSE_EN":0,
# "DS_PH1_CFLY_EN_CHG":0,
# "DS_PH1_DRV_BST_EN":0,
# "DS_PH1_DRV_BST12_EN":0,
# "DS_PH2_DRV_EN_D":0,
# "DS_PH2_DRV_BOOST_PRCHG_LSH_EN":0,
# "DS_PH2_DRV_EN":0,
# "DS_PH2_INDCS_EN_OCP":0,
# "DS_PH2_INDCS_EN_ZC":0,
# "DS_PH2_INDCS_PP_EN_D":0,
# "DS_PH2_CFLY_SENSE_EN_D":0,
# "DS_PH2_CFLY_EN_CHG_D":0,
# "DS_PH2_INDCS_EN_BUF":0,
# "DS_PH2_INDCS_PP_EN":0,
# "DS_PH2_CFLY_SENSE_EN":0,
# "DS_PH2_CFLY_EN_CHG":0,
# "DS_PH2_DRV_BST_EN":0,
# "DS_PH2_DRV_BST12_EN":0,
# "DS_PH3_DRV_EN_D":0,
# "DS_PH3_DRV_BOOST_PRCHG_LSH_EN":0,
# "DS_PH3_DRV_EN":0,
# "DS_PH3_INDCS_EN_OCP":0,
# "DS_PH3_INDCS_EN_ZC":0,
# "DS_PH3_INDCS_PP_EN_D":0,
# "DS_PH3_CFLY_SENSE_EN_D":0,
# "DS_PH3_CFLY_EN_CHG_D":0,
# "DS_PH3_INDCS_EN_BUF":0,
# "DS_PH3_INDCS_PP_EN":0,
# "DS_PH3_CFLY_SENSE_EN":0,
# "DS_PH3_CFLY_EN_CHG":0,
# "DS_PH3_DRV_BST_EN":0,
# "DS_PH3_DRV_BST12_EN":0,
# "DS_PH4_DRV_EN_D":0,
# "DS_PH4_DRV_BOOST_PRCHG_LSH_EN":0,
# "DS_PH4_DRV_EN":0,
# "DS_PH4_INDCS_EN_OCP":0,
# "DS_PH4_INDCS_EN_ZC":0,
# "DS_PH4_INDCS_PP_EN_D":0,
# "DS_PH4_CFLY_SENSE_EN_D":0,
# "DS_PH4_CFLY_EN_CHG_D":0,
# "DS_PH4_INDCS_EN_BUF":0,
# "DS_PH4_INDCS_PP_EN":0,
# "DS_PH4_CFLY_SENSE_EN":0,
# "DS_PH4_CFLY_EN_CHG":0,
# "DS_PH4_DRV_BST_EN":0,
# "DS_PH4_DRV_BST12_EN":0,
# "DS_IFET_IBUS_EN":0,
# "DS_IFET_IBUS_EN_D":0,
# "DS_IFET_EN":0,
# "DS_IFET_EN_DEL_DN":1,
# "DS_IFET_EN_DEL_DN":0,
# "DS_NEGCP_EN":0,
# "DS_IFET_CP_EN ":0,
# "DS_IFET_CP_PD_EN":1,
# "DS_IFET_CP_PD_EN":0,
# "DS_REF_TEMPADC_PDNB":0,
# "DS_AON_EN_DETACH":0, 
# "DS_AON_EN_VDDSNS_OVP":0, 
# "DS_AON_EN_VBUS_OVP":0,
# "DS_REF_PDNB":0,
# "DS_LDO1P8_PDNB":0,
# "DS_HVLDO_EN":0,
#         }

#         for fieldName,value in buck_powerdown_startup__fields.items():
#             for i in list(self.regmap['FIELD NAME']):
                
#                 if fieldName in i.lstrip():
#                     print(f'self.dut.{i}.value = {value}')
        self.dut.IVM.REG_PWRUP1_RW.DS_PH1_DRV_EN_D.value = 0
        self.dut.IVM.REG_PWRUP2_RW.DS_PH1_DRV_BOOST_PRCHG_LSH_EN.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH1_DRV_EN.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH1_DRV_EN_D.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_PH13_INDCS_EN_BUF.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_PH24_INDCS_EN_BUF.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH1_INDCS_EN_OCP.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH1_INDCS_EN_ZC.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH1_INDCS_PP_EN_D.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_PH1_CFLY_SENSE_EN_D.value = 0       
        self.dut.IVM.REG_PWRUP0_RW.DS_PH1_CFLY_EN_CHG_D.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_PH1_INDCS_EN_BUF.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_PH1_INDCS_EN_BUF.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH1_INDCS_PP_EN.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH1_INDCS_PP_EN_D.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_PH1_CFLY_SENSE_EN.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_PH1_CFLY_SENSE_EN_D.value = 0       
        self.dut.IVM.REG_PWRUP0_RW.DS_PH1_CFLY_EN_CHG.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_PH1_CFLY_EN_CHG_D.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH1_DRV_BST_EN.value = 0
        self.dut.IVM.REG_PWRUP2_RW.DS_PH1_DRV_BST12_EN.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH2_DRV_EN_D.value = 0
        self.dut.IVM.REG_PWRUP2_RW.DS_PH2_DRV_BOOST_PRCHG_LSH_EN.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH2_DRV_EN.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH2_DRV_EN_D.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH2_INDCS_EN_OCP.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH2_INDCS_EN_ZC.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH2_INDCS_PP_EN_D.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_PH2_CFLY_SENSE_EN_D.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_PH2_CFLY_EN_CHG_D.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH2_INDCS_PP_EN.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH2_INDCS_PP_EN_D.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_PH2_CFLY_SENSE_EN.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_PH2_CFLY_SENSE_EN_D.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_PH2_CFLY_EN_CHG.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_PH2_CFLY_EN_CHG_D.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH2_DRV_BST_EN.value = 0
        self.dut.IVM.REG_PWRUP2_RW.DS_PH2_DRV_BST12_EN.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH3_DRV_EN_D.value = 0
        self.dut.IVM.REG_PWRUP2_RW.DS_PH3_DRV_BOOST_PRCHG_LSH_EN.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH3_DRV_EN.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH3_DRV_EN_D.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH3_INDCS_EN_OCP.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH3_INDCS_EN_ZC.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH3_INDCS_PP_EN_D.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_PH3_CFLY_SENSE_EN_D.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_PH3_CFLY_EN_CHG_D.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH3_INDCS_PP_EN.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH3_INDCS_PP_EN_D.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_PH3_CFLY_SENSE_EN.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_PH3_CFLY_SENSE_EN_D.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_PH3_CFLY_EN_CHG.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_PH3_CFLY_EN_CHG_D.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH3_DRV_BST_EN.value = 0
        self.dut.IVM.REG_PWRUP2_RW.DS_PH3_DRV_BST12_EN.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH4_DRV_EN_D.value = 0
        self.dut.IVM.REG_PWRUP2_RW.DS_PH4_DRV_BOOST_PRCHG_LSH_EN.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH4_DRV_EN.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH4_DRV_EN_D.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH4_INDCS_EN_OCP.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH4_INDCS_EN_ZC.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH4_INDCS_PP_EN_D.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_PH4_CFLY_SENSE_EN_D.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_PH4_CFLY_EN_CHG_D.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH4_INDCS_PP_EN.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH4_INDCS_PP_EN_D.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_PH4_CFLY_SENSE_EN.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_PH4_CFLY_SENSE_EN_D.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_PH4_CFLY_EN_CHG.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_PH4_CFLY_EN_CHG_D.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH4_DRV_BST_EN.value = 0
        self.dut.IVM.REG_PWRUP2_RW.DS_PH4_DRV_BST12_EN.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_IFET_IBUS_EN.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_IFET_IBUS_EN_D.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_IFET_IBUS_EN_D.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_IFET_EN.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_IFET_EN_DEL_DN.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_IFET_EN_DEL_DN.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_NEGCP_EN.value = 0
        self.dut.IVM.REG_IFET_RW.DS_NEGCP_EN_SOFTSTART.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_IFET_CP_EN.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_IFET_CP_PD_EN.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_IFET_CP_PD_EN.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_AON_EN_DETACH.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_AON_EN_VDDSNS_OVP.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_AON_EN_VBUS_OVP.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_REF_PDNB.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_LDO1P8_PDNB.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_HVLDO_EN.value = 0
      
    def boost_PowerDown(self):
#         boost_powerdown_startup__fields = {
# "DS_PH1_INDCS_EN_OCP":0,
# "DS_PH1_INDCS_EN_ZC":0,
# "DS_PH1_INDCS_PP_EN":0,
# "DS_PH1_INDCS_PP_EN_D":0,
# "DS_PH1_INDCS_EN_BUF":0,
# "DS_PH1_CFLY_SENSE_EN":0,
# "DS_PH1_CFLY_SENSE_EN_D":0,
# "DS_PH1_CFLY_EN_CHG":0,
# "DS_PH1_CFLY_EN_CHG_D":0,
# "DS_PH1_DRV_EN":0,
# "DS_PH1_DRV_EN_D":0,
# "DS_PH1_DRV_BOOST_PRCHG_LSH_EN":0,
# "DS_PH1_DRV_BST_EN":0,
# "DS_PH1_DRV_BST12_EN":0,
# "DS_PH1_DRV_BST2_POR_BOOST":0,
# "DS_PH2_INDCS_EN_OCP":0,
# "DS_PH2_INDCS_EN_ZC":0,
# "DS_PH2_INDCS_PP_EN":0,
# "DS_PH2_INDCS_PP_EN_D":0,
# "DS_PH2_INDCS_EN_BUF":0,
# "DS_PH2_CFLY_SENSE_EN":0,
# "DS_PH2_CFLY_SENSE_EN_D":0,
# "DS_PH2_CFLY_EN_CHG":0,
# "DS_PH2_CFLY_EN_CHG_D":0,
# "DS_PH2_DRV_EN":0,
# "DS_PH2_DRV_EN_D":0,
# "DS_PH2_DRV_BOOST_PRCHG_LSH_EN":0,
# "DS_PH2_DRV_BST_EN":0,
# "DS_PH2_DRV_BST12_EN":0,
# "DS_PH2_DRV_BST2_POR_BOOST":0,
# "DS_PH3_INDCS_EN_OCP":0,
# "DS_PH3_INDCS_EN_ZC":0,
# "DS_PH3_INDCS_PP_EN":0,
# "DS_PH3_INDCS_PP_EN_D":0,
# "DS_PH3_INDCS_EN_BUF":0,
# "DS_PH3_CFLY_SENSE_EN":0,
# "DS_PH3_CFLY_SENSE_EN_D":0,
# "DS_PH3_CFLY_EN_CHG":0,
# "DS_PH3_CFLY_EN_CHG_D":0,
# "DS_PH3_DRV_EN":0,
# "DS_PH3_DRV_EN_D":0,
# "DS_PH3_DRV_BOOST_PRCHG_LSH_EN":0,
# "DS_PH3_DRV_BST_EN":0,
# "DS_PH3_DRV_BST12_EN":0,
# "DS_PH3_DRV_BST2_POR_BOOST":0,
# "DS_PH4_INDCS_EN_OCP":0,
# "DS_PH4_INDCS_EN_ZC":0,
# "DS_PH4_INDCS_PP_EN":0,
# "DS_PH4_INDCS_PP_EN_D":0,
# "DS_PH4_INDCS_EN_BUF":0,
# "DS_PH4_CFLY_SENSE_EN":0,
# "DS_PH4_CFLY_SENSE_EN_D":0,
# "DS_PH4_CFLY_EN_CHG":0,
# "DS_PH4_CFLY_EN_CHG_D":0,
# "DS_PH4_DRV_EN":0,
# "DS_PH4_DRV_EN_D":0,
# "DS_PH4_DRV_BOOST_PRCHG_LSH_EN":0,
# "DS_PH4_DRV_BST_EN":0,
# "DS_PH4_DRV_BST12_EN":0,
# "DS_PH4_DRV_BST2_POR_BOOST":0,
# "DS_IFET_IBUS_EN":0,
# "DS_IFET_IBUS_EN_D":0,
# "DS_IFET_EN":0,
# "DS_IFET_EN_DEL_DN":1,
# "DS_IFET_EN_DEL_DN":0,
# "DS_NEGCP_EN":0,
# "DS_IFET_CP_EN ":0,
# "DS_IFET_CP_PD_EN":1,
# "DS_IFET_CP_PD_EN":0,
# "DS_REF_TEMPADC_PDNB":0,
# "DS_AON_EN_DETACH":0, 
# "DS_AON_EN_VDDSNS_OVP":0, 
# "DS_AON_EN_VBUS_OVP":0,
# "DS_REF_PDNB":0,
# "DS_LDO1P8_PDNB":0,
# "DS_HVLDO_EN":0,

#         }

#         for fieldName,value in boost_powerdown_startup__fields.items():
#             for i in list(self.regmap['FIELD NAME']):
                
#                 if fieldName in i.lstrip():
#                     print(f'self.dut.{i}.value = {value}')
 
        self.dut.IVM.REG_PWRUP1_RW.DS_PH1_INDCS_EN_OCP.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH1_INDCS_EN_ZC.value = 0 
        self.dut.IVM.REG_PWRUP0_RW.DS_PH13_INDCS_EN_BUF.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_PH24_INDCS_EN_BUF.value = 0   
        self.dut.IVM.REG_PWRUP0_RW.DS_PH1_INDCS_EN_BUF.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_PH1_INDCS_EN_BUF.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH1_INDCS_PP_EN.value = 0    
        self.dut.IVM.REG_PWRUP1_RW.DS_PH1_INDCS_PP_EN_D.value = 0  
        self.dut.IVM.REG_PWRUP1_RW.DS_PH1_INDCS_PP_EN_D.value = 0  
        self.dut.IVM.REG_PWRUP0_RW.DS_PH1_CFLY_SENSE_EN.value = 0  
        self.dut.IVM.REG_PWRUP0_RW.DS_PH1_CFLY_SENSE_EN_D.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_PH1_CFLY_SENSE_EN_D.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_PH1_CFLY_EN_CHG.value = 0    
        self.dut.IVM.REG_PWRUP0_RW.DS_PH1_CFLY_EN_CHG_D.value = 0  
        self.dut.IVM.REG_PWRUP0_RW.DS_PH1_CFLY_EN_CHG_D.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH1_DRV_EN.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH1_DRV_EN_D.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH1_DRV_EN_D.value = 0
        self.dut.IVM.REG_PWRUP2_RW.DS_PH1_DRV_BOOST_PRCHG_LSH_EN.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH1_DRV_BST_EN.value = 0
        self.dut.IVM.REG_PWRUP2_RW.DS_PH1_DRV_BST12_EN.value = 0
        self.dut.IVM.REG_PWRUP2_RW.DS_PH1_DRV_BST2_POR_BOOST.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH2_INDCS_EN_OCP.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH2_INDCS_EN_ZC.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH2_INDCS_PP_EN.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH2_INDCS_PP_EN_D.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH2_INDCS_PP_EN_D.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_PH2_CFLY_SENSE_EN.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_PH2_CFLY_SENSE_EN_D.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_PH2_CFLY_SENSE_EN_D.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_PH2_CFLY_EN_CHG.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_PH2_CFLY_EN_CHG_D.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_PH2_CFLY_EN_CHG_D.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH2_DRV_EN.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH2_DRV_EN_D.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH2_DRV_EN_D.value = 0
        self.dut.IVM.REG_PWRUP2_RW.DS_PH2_DRV_BOOST_PRCHG_LSH_EN.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH2_DRV_BST_EN.value = 0
        self.dut.IVM.REG_PWRUP2_RW.DS_PH2_DRV_BST12_EN.value = 0
        self.dut.IVM.REG_PWRUP2_RW.DS_PH2_DRV_BST2_POR_BOOST.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH3_INDCS_EN_OCP.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH3_INDCS_EN_ZC.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH3_INDCS_PP_EN.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH3_INDCS_PP_EN_D.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH3_INDCS_PP_EN_D.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_PH3_CFLY_SENSE_EN.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_PH3_CFLY_SENSE_EN_D.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_PH3_CFLY_SENSE_EN_D.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_PH3_CFLY_EN_CHG.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_PH3_CFLY_EN_CHG_D.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_PH3_CFLY_EN_CHG_D.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH3_DRV_EN.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH3_DRV_EN_D.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH3_DRV_EN_D.value = 0
        self.dut.IVM.REG_PWRUP2_RW.DS_PH3_DRV_BOOST_PRCHG_LSH_EN.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH3_DRV_BST_EN.value = 0
        self.dut.IVM.REG_PWRUP2_RW.DS_PH3_DRV_BST12_EN.value = 0
        self.dut.IVM.REG_PWRUP2_RW.DS_PH3_DRV_BST2_POR_BOOST.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH4_INDCS_EN_OCP.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH4_INDCS_EN_ZC.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH4_INDCS_PP_EN.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH4_INDCS_PP_EN_D.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH4_INDCS_PP_EN_D.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_PH4_CFLY_SENSE_EN.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_PH4_CFLY_SENSE_EN_D.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_PH4_CFLY_SENSE_EN_D.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_PH4_CFLY_EN_CHG.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_PH4_CFLY_EN_CHG_D.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_PH4_CFLY_EN_CHG_D.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH4_DRV_EN.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH4_DRV_EN_D.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH4_DRV_EN_D.value = 0
        self.dut.IVM.REG_PWRUP2_RW.DS_PH4_DRV_BOOST_PRCHG_LSH_EN.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH4_DRV_BST_EN.value = 0
        self.dut.IVM.REG_PWRUP2_RW.DS_PH4_DRV_BST12_EN.value = 0
        self.dut.IVM.REG_PWRUP2_RW.DS_PH4_DRV_BST2_POR_BOOST.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_IFET_IBUS_EN.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_IFET_IBUS_EN_D.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_IFET_IBUS_EN_D.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_IFET_EN.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_IFET_EN_DEL_DN.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_IFET_EN_DEL_DN.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_NEGCP_EN.value = 0
        self.dut.IVM.REG_IFET_RW.DS_NEGCP_EN_SOFTSTART.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_IFET_CP_EN.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_IFET_CP_PD_EN.value = 1
        self.dut.IVM.REG_PWRUP0_RW.DS_IFET_CP_PD_EN.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_AON_EN_DETACH.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_AON_EN_VDDSNS_OVP.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_AON_EN_VBUS_OVP.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_REF_PDNB.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_LDO1P8_PDNB.value = 0
        self.dut.IVM.REG_PWRUP0_RW.DS_HVLDO_EN.value = 0

if __name__ == '__main__':
    Startup(None)

buck_startup =     [
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

for i in buck_startup:
    print(i)
    print(f"input('{i} ->')")
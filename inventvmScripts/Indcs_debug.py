from time import sleep
from Instruments_API import Instruments
class Inducs_Debug:

    def __init__(self,dut):
        self.dut = dut
        self.scope = Instruments().scope
        self.supply = Instruments().supply

    def SlewRate(self):
        input('Slew Rate measurement >')
        self.dut.IVM.REG_DRV_INDCS_RW.DS_INDCS_SAMPLE_DELAY.value = 0
        for i in range (0,4):
            self.dut.IVM.REG_DRV_INDCS_RW.DS_DRV_SLEW.value = i
            self.scope.single_Trigger__ON()
            input(f'Delay 0 , Slewrate {i}')
        self.dut.IVM.REG_DRV_INDCS_RW.DS_INDCS_SAMPLE_DELAY.value = 1
        for i in range (0,4):
            self.dut.IVM.REG_DRV_INDCS_RW.DS_DRV_SLEW.value = i
            input(f'Delay 1 , Slewrate {i}')
        self.dut.IVM.REG_DRV_INDCS_RW.DS_DRV_SLEW.value = 0
        self.dut.IVM.REG_DRV_INDCS_RW.DS_INDCS_SAMPLE_DELAY.value = 0

    def buck_OpenLoop(self,duty_cycle=0.5,vbath_th=4.5,ibat_th=1,ibus_th=3,phase=1):
        self.dut.IVM.REG_DRV_INDCS_RW.DS_PH1_INDCS_PROG_OCP.value = 4
        self.dut.IVM.REG_DRV_INDCS_RW.DS_PH2_INDCS_PROG_OCP.value = 4
        self.dut.IVM.REG_DRV_INDCS_RW.DS_PH3_INDCS_PROG_OCP.value = 4
        self.dut.IVM.REG_DRV_INDCS_RW.DS_PH4_INDCS_PROG_OCP.value = 4
        self.dut.startup_procedure()
        self.dut.block_apis.SIMULINK_MODEL.set_standby_en(1)
        self.dut.block_apis.SIMULINK_MODEL.set_vbat_buck_thld_V(vbath_th)
        self.dut.block_apis.SIMULINK_MODEL.set_ibat_buck_thld_A(ibat_th)
        self.dut.block_apis.SIMULINK_MODEL.set_ibus_buck_thld_A(ibus_th)
        self.dut.block_apis.SIMULINK_MODEL.set_alpha_override_en(True)
        self.dut.block_apis.SIMULINK_MODEL.set_alpha_override_value(0)
        self.dut.block_apis.SIMULINK_MODEL.set_d_override_value(duty_cycle)
        self.dut.block_apis.SIMULINK_MODEL.set_d_override_en(True)
        self.dut.SIMULINK_MODEL.GAIN_CONFIG1.VCFLY_GAIN.value = 0x7100
        self.dut.SIMULINK_MODEL.TEST_INNER_LOOP_PH_MGMT.PHASE_INDUCTOR_MAP.value = phase
        # self.dut.SIMULINK_MODEL.POWERSTATE_CFG.STANDBY_EN.value=1
        sleep(1)
        # self.dut.SIMULINK_MODEL.POWERSTATE_CFG.STANDBY_EN.value=0
        self.dut.block_apis.SIMULINK_MODEL.set_standby_en(0)
        self.dut.IVM.REG_PWRUP1_RW.DS_PH1_INDCS_EN_OCP.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH2_INDCS_EN_OCP.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH3_INDCS_EN_OCP.value = 0
        self.dut.IVM.REG_PWRUP1_RW.DS_PH4_INDCS_EN_OCP.value = 0
    
    def buck_Indcs_Debug(self,Vbus=5,Vbat=4,ibat=-0.2,duty_cycle=0.8,phase=0):

        self.buck_OpenLoop(duty_cycle=duty_cycle,phase=phase)
        self.supply.setVoltage(channel=1,voltage=Vbus)
        self.supply.setVoltage(channel=3,voltage=Vbat)
        print('Buck current ',self.supply.getCurrent(channel=3))
        input('buck Current Set >')
        
        while (self.supply.getCurrent(channel=3) > ibat):
            Vbat = Vbat - 0.005
            self.supply.setVoltage(channel=3,voltage=Vbat)
            sleep(0.01)
        input(f'Buck is running in phase {phase } with duty cycle {duty_cycle}  Curent {self.supply.getCurrent(channel=3)}> ')


        self.SlewRate()
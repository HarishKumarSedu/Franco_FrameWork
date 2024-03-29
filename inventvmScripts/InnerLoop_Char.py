from Instruments_API import Instruments
from MatrixAPI.MatrixSignal import Matrix 
from writeExcel import writeInExcel
from startup import Startup
from time import sleep,time,time_ns
import re
class InnerLoop:

    def __init__(self,dut,loadtrims) -> None:
        self.dut = dut 
        self.startup = Startup(dut=dut)
        self.supply = Instruments().supply
        self.scope = Instruments().scope
        self.multimeter = Instruments().multimeter
        self.voltmeter = Instruments().voltmeter
        self.multimeter.set_Voltage__NPLC(NPLC=1)
        self.matrix = Matrix()
        self.loadtrims = loadtrims

        '''
        
            Inductor Current sense ocp thershold checking in  the static conidtion 
            method : Inductor_OCP_static (Note : must pass High/Low string key word to activate the high side test or low side test in sheet argument )
            ex: self.Inductor_OCP_static(sheet='Device2_4phases_LowSide_85C_OCP')

            INDCS OCP reference 
            exampler : self.Indctor_OCP_Reference__Sweep(sheet='Device2_OCP_reference_25C') 
            Note Measure Reference in Test1 with respect to the GND
        '''
        # self.Inductor_OCP_static(sheet='Device1_4phases_LowSide_25C_OCP')
        # self.Indctor_OCP_Reference__Sweep(sheet='Device3_OCP_reference_85C')
        # input('Set 85C')
        # self.Inductor_OCP_static(sheet='Device1_4phases_LowSide_85C_OCP')
        # self.Inductor_OCP_static(sheet='Device2_4phases_LowSide_85C_OCP')
        # self.Indctor_OCP_Reference__Sweep(sheet='Device3_OCP_reference_0C')

        #Inductor current sense voltage sweep
        # self.Indcs_Sweep_static(sheet='Device3_indcsHigh_buck_25C')
        # input('buck 85C')
        # self.Indcs_Sweep_static(sheet='Device3_indcsHigh_buck_85C')
        # input('boost')
        # self.Indcs_Sweep_static(sheet='Device3_indcsHigh_boost_25C')
        # input('boost 85C')
        # self.Indcs_Sweep_static(sheet='Device3_indcsHigh_boost_85C')

        '''
            Zero current sweep 
        '''
        self.ZC_Sweep(sheet='Device3_ZC_HighSide_0C')
        sleep(1)
        self.ZC_Sweep(sheet='Device3_ZC_LowSide_0C')
        # input('85c')
        # self.ZC_Sweep(sheet='Device1_ZC_HighSide_85C')
        # sleep(1)
        # self.ZC_Sweep(sheet='Device1_ZC_LowSide_85C')
        # self.Indcs_Sweep___Switching()
    def InputCurr_Step(self):
        self.scope.set_HScale(scale='20E-3')
        self.scope.set_Channel__VScale(scale=0.2)
        self.scope.set_trigger__level(level=0.1)
        self.scope.set_trigger__mode(mode='NORM')
        self.scope.init_scopePosEdge__Trigger()
        # for i in range(1,8,1):
        for i in range(1,8,1):
            self.supply.setCurrent(channel=1,current=0)
            self.scope.scopeTriggercquire()
            while(self.scope.scopeAcquire_BUSY):
                sleep(0.01)
                self.supply.setCurrent(channel=1,current=0)
                sleep(0.01)
                self.supply.setCurrent(channel=1,current=-i)
            # sleep(0.01)
            # self.supply.setCurrent(channel=1,current=0)
            # sleep(0.1)
            print(self.scope.Measmp())
            sleep(0.1)
            # print(self.scope.Measmp(Meas='MEAS2'))
    
    def Inductor_OCP_static(self,sheet='Device1_4phases_HighSide_85C_OCP'):
            self.scope.set_HScale(scale='1E-3')
            self.scope.set_Channel__VScale(scale=0.2)
            self.scope.set_trigger__level(level=0.2)
            self.scope.set_trigger__mode(mode='NORM')
            self.scope.init_scopePosEdge__Trigger()
            sleep(0.1)
            
            self.startup.buck_PowerUp()
            self.loadtrims.loadTrims()
            self.supply.setCurrent(channel=1,current=0)
            sleep(0.2)
            self.scope.scopeTriggercquire(channel='CH1')
            if re.search('High',sheet):
                
                # phases = {0:'PH1S1'}
                phases = {0:'PH1S1',1:'PH2S1',2:'PH3S1',3:'PH4S1'}
                try :
                    loadCurrent = [[],[],[],[]]
                    OCPthershold = [[],[],[],[]]
                    IndcsVoltage = [[],[],[],[]]
                    error = [[],[],[],[]]
                    for phaseIndex,phase in phases.items() :
                        print(phase)
                        self.matrix.reset()
                        current = 4.5
                        sleep(0.1)
                        for i in range(0,5,1):
                            self.Phase_Select(phase,TestSignal=phaseIndex,current_index=i,DriverEnable=True)
                            sleep(0.2)
                            self.scope.scopeTriggercquire(channel='CH1')
                            print('i',i,'phase',phase)
                            sleep(0.2)
                            if abs(self.supply.getVoltage(channel=1)) > 2.5:
                                self.scope.scopeTriggercquire(channel='CH1')
                                # input('>>>>>>>>')
                                sleep(0.5)
                                while(self.scope.scopeAcquire_BUSY):
                                    self.supply.setCurrent(channel=1,current=-current)
                                    current=current+0.001
                                    if current > 8.1:
                                        break
                                    # end = time_ns() + 5000000
                                    # while True:
                                    #     if time_ns() > end:
                                    #         break
                                    sleep(0.001)
                                sleep(0.1)
                                loadCurrent[phaseIndex].append(abs(self.supply.getCurrent(channel=1)))
                                IndcsVoltage[phaseIndex].append(self.multimeter.meas_V())
                                OCPthershold[phaseIndex].append(5+i*0.5)
                                error[phaseIndex].append((((0.075*OCPthershold[phaseIndex][-1]) - IndcsVoltage[phaseIndex][-1])/(0.075*OCPthershold[phaseIndex][-1]))*100)
                                print('Current',loadCurrent[phaseIndex][-1],'Threshold',OCPthershold[phaseIndex][-1],'inductor Current Sense Voltage',IndcsVoltage[phaseIndex][-1],'Error %',error[phaseIndex][-1])
                                # current = current + 0.4
                                tempcurrent = current - 0.5
                                while current >= tempcurrent :
                                # while current >= 0 :
                                    self.supply.setCurrent(channel=1,current=-current)
                                    current=current-0.1
                                    sleep(0.0001)
                        while current >= 0 :
                            self.supply.setCurrent(channel=1,current=-current)
                            current=current-0.1
                            sleep(0.01)
                        self.Phase_Select(DriverEnable=False)
                    writeInExcel(sheet=sheet,filename='InnerLoop_Char\InnerLoop_Char3.xlsx',ph1_OCPthershold=OCPthershold[0],ph1_loadCurrent=loadCurrent[0],ph1_IndcsVoltage=IndcsVoltage[0],ph1_error=error[0], \
                                 ph2_OCPthershold=OCPthershold[1],ph2_loadCurrent=loadCurrent[1],ph2_IndcsVoltage=IndcsVoltage[1],ph2_error=error[1],ph3_OCPthershold=OCPthershold[2],ph3_loadCurrent=loadCurrent[2],ph3_IndcsVoltage=IndcsVoltage[2],ph3_error=error[2],\
                                 ph4_OCPthershold=OCPthershold[3],ph4_loadCurrent=loadCurrent[3],ph4_IndcsVoltage=IndcsVoltage[3],ph4_error=error[3],)
                except KeyboardInterrupt:
                    while current >= 0 :
                        self.supply.setCurrent(channel=1,current=-current)
                        current=current-0.01
                        sleep(0.01)
            if re.search('Low',sheet):
                # phases = {0:'PH4S4'}
                phases = {0:'PH1S4',1:'PH2S4',2:'PH3S4',3:'PH4S4'}
                try :
                    loadCurrent = [[],[],[],[]]
                    OCPthershold = [[],[],[],[]]
                    IndcsVoltage = [[],[],[],[]]
                    error = [[],[],[],[]]
                    for phaseIndex,phase in phases.items() :
                        print(phase)
                        self.matrix.reset()
                        current =4.5
                        self.Phase_Select(phase,TestSignal=phaseIndex,current_index=0,DriverEnable=True)
                        self.scope.scopeTriggercquire(channel='CH1')
                        sleep(0.1)
                        for i in range(0,5,1):
                            self.Phase_Select(phase,TestSignal=phaseIndex,current_index=i,DriverEnable=True)
                            sleep(0.1)
                            self.scope.scopeTriggercquire(channel='CH1')
                            sleep(0.1)
                            # input('>>>>>>')
                            # if abs(self.supply.getVoltage(channel=1)) <= 0:
                            if True:
                                while(self.scope.scopeAcquire_BUSY):
                                    self.supply.setCurrent(channel=1,current=current)
                                    current=current+0.001
                                    if current > 8.1:
                                        break
                                    # end = time_ns() + 5000000
                                    # while True:
                                    #     if time_ns() > end:
                                    #         break
                                    sleep(0.001)
                                sleep(1)
                                loadCurrent[phaseIndex].append(abs(self.supply.getCurrent(channel=1)))
                                IndcsVoltage[phaseIndex].append(self.multimeter.meas_V())
                                OCPthershold[phaseIndex].append(5+i*0.5)
                                error[phaseIndex].append((((0.075*OCPthershold[phaseIndex][-1]) - IndcsVoltage[phaseIndex][-1])/(0.075*OCPthershold[phaseIndex][-1]))*100)
                                print('Current',loadCurrent[phaseIndex][-1],'Threshold',OCPthershold[phaseIndex][-1],'inductor Current Sense Voltage',IndcsVoltage[phaseIndex][-1],'Error %',error[phaseIndex][-1])
                                tempcurrent = current - 0.3
                                while current >= tempcurrent :
                                    self.supply.setCurrent(channel=1,current=current)
                                    current=current-0.05
                                    sleep(0.0001)
                        while current >= 0 :
                            self.supply.setCurrent(channel=1,current=current)
                            current=current-0.01
                            sleep(0.01)
                        self.Phase_Select(DriverEnable=False)
                    writeInExcel(sheet=sheet,filename='InnerLoop_Char\InnerLoop_Char3.xlsx',ph1_OCPthershold=OCPthershold[0],ph1_loadCurrent=loadCurrent[0],ph1_IndcsVoltage=IndcsVoltage[0],ph1_error=error[0], \
                                 ph2_OCPthershold=OCPthershold[1],ph2_loadCurrent=loadCurrent[1],ph2_IndcsVoltage=IndcsVoltage[1],ph2_error=error[1],ph3_OCPthershold=OCPthershold[2],ph3_loadCurrent=loadCurrent[2],ph3_IndcsVoltage=IndcsVoltage[2],ph3_error=error[2],\
                                 ph4_OCPthershold=OCPthershold[3],ph4_loadCurrent=loadCurrent[3],ph4_IndcsVoltage=IndcsVoltage[3],ph4_error=error[3])
                except KeyboardInterrupt:
                    while current >= 0 :
                        self.supply.setCurrent(channel=1,current=current)
                        current=current-0.01
                        sleep(0.01)
    # sweep the High side and low side measure the induct current sense voltage 
    def Indcs_Sweep_static(self,sheet='Device1_4phases_indcs_High_sweep'):
            
            self.startup.buck_PowerUp()
            self.loadtrims.loadTrims()
            self.supply.setCurrent(channel=1,current=0)
            sleep(0.2)
            if re.search('High',sheet):
                
                # phases = {3:'PH4S1'}
                phases = {0:'PH1S1',1:'PH2S1',2:'PH3S1',3:'PH4S1'}
                try :
                    loadCurrent = [[],[],[],[]]
                    IndcsVoltage_th = [[],[],[],[]]
                    IndcsVoltage = [[],[],[],[]]
                    error = [[],[],[],[]]
                    for phaseIndex,phase in phases.items() :
                        print(phase)
                        self.matrix.reset()
                        current = 0.1
                        sleep(0.2)
                        self.Phase_Select(phase,TestSignal=phaseIndex,current_index=4,DriverEnable=True)
                        print('phase',phase)
                        sleep(0.1)
                        if abs(self.supply.getVoltage(channel=1)) > 2.5:
                            # input('>>>>>>')
                            while current < 7.61:
                                self.supply.setCurrent(channel=1,current=-current)
                                sleep(0.1)
                                loadCurrent[phaseIndex].append(abs(self.supply.getCurrent(channel=1)))
                                IndcsVoltage[phaseIndex].append(self.multimeter.meas_V())
                                IndcsVoltage_th[phaseIndex].append(0.075*current)
                                error[phaseIndex].append(((abs((IndcsVoltage[phaseIndex][-1])) - IndcsVoltage_th[phaseIndex][-1])/(IndcsVoltage_th[phaseIndex][-1]))*100)
                                current=current+0.1
                        while current >= 0 :
                            self.supply.setCurrent(channel=1,current=-current)
                            current=current-0.01
                            sleep(0.01)
                        self.Phase_Select(DriverEnable=False)
                    writeInExcel(sheet=sheet,filename='InnerLoop_Char\InnerLoop_HighSide.xlsx',ph1_IndcsVoltage_th=IndcsVoltage_th[0],ph1_loadCurrent=loadCurrent[0],ph1_IndcsVoltage=IndcsVoltage[0],ph1_error=error[0], \
                                 ph2_IndcsVoltage_th=IndcsVoltage_th[1],ph2_loadCurrent=loadCurrent[1],ph2_IndcsVoltage=IndcsVoltage[1],ph2_error=error[1],ph3_IndcsVoltage_th=IndcsVoltage_th[2],ph3_loadCurrent=loadCurrent[2],ph3_IndcsVoltage=IndcsVoltage[2],ph3_error=error[2],\
                                 ph4_IndcsVoltage_th=IndcsVoltage_th[3],ph4_loadCurrent=loadCurrent[3],ph4_IndcsVoltage=IndcsVoltage[3],ph4_error=error[3])
                except KeyboardInterrupt:
                    while current >= 0 :
                        self.supply.setCurrent(channel=1,current=-current)
                        current=current-0.01
                        sleep(0.01)
            if re.search('Low',sheet):
                # phases = {0:'PH4S4'}
                phases = {0:'PH1S4',1:'PH2S4',2:'PH3S4',3:'PH4S4'}
                try :
                    loadCurrent = [[],[],[],[]]
                    IndcsVoltage_th = [[],[],[],[]]
                    IndcsVoltage = [[],[],[],[]]
                    error = [[],[],[],[]]
                    for phaseIndex,phase in phases.items() :
                        print(phase)
                        self.matrix.reset()
                        current = 0.1
                        sleep(0.1)
                        self.Phase_Select(phase,TestSignal=phaseIndex,current_index=4,DriverEnable=True)
                        print('phase',phase)
                        sleep(0.1)
                        if True:
                            # input('>>>>>>')
                            while current < 7.61:
                                self.supply.setCurrent(channel=1,current=current)
                                sleep(0.05)
                                loadCurrent[phaseIndex].append(abs(self.supply.getCurrent(channel=1)))
                                IndcsVoltage[phaseIndex].append(self.multimeter.meas_V())
                                IndcsVoltage_th[phaseIndex].append(0.075*current)
                                error[phaseIndex].append(((abs((IndcsVoltage[phaseIndex][-1])) - IndcsVoltage_th[phaseIndex][-1])/(IndcsVoltage_th[phaseIndex][-1]))*100)
                                current=current+0.1
                        while current >= 0 :
                            self.supply.setCurrent(channel=1,current=current)
                            current=current-0.01
                            sleep(0.01)
                        self.Phase_Select(DriverEnable=False)
                        self.supply.setCurrent(channel=1,current=0)
                    writeInExcel(sheet=sheet,filename='InnerLoop_Char\InnerLoop_Indcs_Lowside1.xlsx',ph1_IndcsVoltage_th=IndcsVoltage_th[0],ph1_loadCurrent=loadCurrent[0],ph1_IndcsVoltage=IndcsVoltage[0],ph1_error=error[0], \
                                 ph2_IndcsVoltage_th=IndcsVoltage_th[1],ph2_loadCurrent=loadCurrent[1],ph2_IndcsVoltage=IndcsVoltage[1],ph2_error=error[1],ph3_IndcsVoltage_th=IndcsVoltage_th[2],ph3_loadCurrent=loadCurrent[2],ph3_IndcsVoltage=IndcsVoltage[2],ph3_error=error[2],\
                                 ph4_IndcsVoltage_th=IndcsVoltage_th[3],ph4_loadCurrent=loadCurrent[3],ph4_IndcsVoltage=IndcsVoltage[3],ph4_error=error[3])
                except KeyboardInterrupt:
                    while current >= 0 :
                        self.supply.setCurrent(channel=1,current=current)
                        current=current-0.01
                        sleep(0.01)
                    self.supply.setCurrent(channel=1,current=0)
    def Indcs_Sweep___Switching(self,sheet='Device1_4phases_indcs_switching'):
            
            self.loadtrims.loadTrims()
            self.supply.setCurrent(channel=1,current=0)
            sleep(0.2)

            phases = {0:'PH1S1',1:'PH2S1',2:'PH3S1',3:'PH4S1'}
            # phases = {1:'PH2S1',2:'PH3S1',3:'PH4S1'}
            try :

                IndcsVoltage = [[],[],[],[]]
                shuntVoltage = [[],[],[],[]]
                error = [[],[],[],[]]
                for phaseIndex,phase in phases.items() :
                    print(phase)
                    self.matrix.reset()
                    current = 0.1
                    self.matrix.force_Matrix__Switchx(phase)
                    sleep(1)
                    self.startup.buck_ClosedLoop(vbat=4,ibat=16,icmd_ph=6,No_phase=1,ibus=3.3,phase=phaseIndex)
                    sleep(5)
                    print('phase',phase)
                    input('>>>>>>')
                    sleep(1)
                    if abs(self.supply.getVoltage(channel=1)) > 2.5:
                        # input('>>>>>>')
                        while current < 5.1:
                            self.supply.setCurrent(channel=1,current=-current)
                            sleep(0.1)
                            IndcsVoltage[phaseIndex].append(self.multimeter.meas_V())
                            shuntVoltage[phaseIndex].append((self.voltmeter.meas_V())/(20))
                            current=current+0.1
                    while current >= 0 :
                        self.supply.setCurrent(channel=1,current=-current)
                        current=current-0.01
                        sleep(0.01)
                    # self.Phase_Select(DriverEnable=False)
                    self.dut.block_apis.SIMULINK_MODEL.set_standby_en(1)
                writeInExcel(sheet=sheet,filename='InnerLoop_Char\InnerLoop_Indcs_Switching.xlsx',\
                             ph1_IndcsVoltage = IndcsVoltage[0],ph1_shuntVoltage = shuntVoltage[0],\
                             ph2_IndcsVoltage = IndcsVoltage[1],ph2_shuntVoltage = shuntVoltage[1],\
                             ph3_IndcsVoltage = IndcsVoltage[2],ph3_shuntVoltage = shuntVoltage[2],\
                             ph4_IndcsVoltage = IndcsVoltage[3],ph4_shuntVoltage = shuntVoltage[3],\
                            )
            except (KeyboardInterrupt,IOError) as e:
                while current >= 0 :
                    self.supply.setCurrent(channel=1,current=-current)
                    current=current-0.01
                    sleep(0.01)
                self.dut.block_apis.SIMULINK_MODEL.set_standby_en(1)
            finally:
                while current >= 0 :
                    self.supply.setCurrent(channel=1,current=-current)
                    current=current-0.01
                    sleep(0.01)
                self.supply.setCurrent(channel=1,current=0)
                self.dut.block_apis.SIMULINK_MODEL.set_standby_en(1)


    #select the particlar phase according to the phase selection in the sequence 
    def Phase_Select(self,phase='PH1S1',Test1_block=3,TestSignal=0,current_index=0,DriverEnable=False):
        self.matrix.force_Matrix__Switchx(phase)
        sleep(0.2)
        if DriverEnable:
            if phase == 'PH1S1':
                self.dut.IVM.REG_DRV_INDCS_RW.DS_PH1_INDCS_PROG_OCP.value = current_index
                sleep(0.1)
                self.dut.IVM.REG_PWRUP1_RW.DS_PH1_INDCS_EN_OCP.value = 1
                self.dut.IVM.REG_VIS_MUX_RW.TST1_SEL.value =  TestSignal
                self.dut.IVM.REG_VIS_MUX_RW.TST1_BLOCK_SEL.value = Test1_block

                self.dut.IVM.REG_PWRUP2_RW.DS_INDCS_CLR_OCP.value = 1
                sleep(0.3)
                self.dut.IVM.REG_FORCE_RW.DS_PH1_INDCS_FORCE_SEL.value = 1
                self.dut.IVM.REG_FORCE_RW.DS_PH1_INDCS_FORCE_EN.value = 1
                self.dut.IVM.REG_TEST0_RW.DS_PH1_INDCS_TEST_SEL.value = 1
                self.dut.IVM.REG_TEST0_RW.DS_PH1_INDCS_TEST_EN.value = 1
                self.dut.IVM.REG_TEST0_RW.DS_PH1_DRV_TEST_HS.value = 1
                self.dut.IVM.REG_TEST0_RW.DS_PH1_DRV_TEST_EN.value = 1
                self.dut.IVM.REG_PWRUP2_RW.DS_INDCS_CLR_OCP.value = 0
            if phase == 'PH1S4':
                self.dut.IVM.REG_DRV_INDCS_RW.DS_PH1_INDCS_PROG_OCP.value = current_index
                sleep(0.1)
                self.dut.IVM.REG_PWRUP1_RW.DS_PH1_INDCS_EN_OCP.value = 1
                self.dut.IVM.REG_VIS_MUX_RW.TST1_SEL.value =  TestSignal
                self.dut.IVM.REG_VIS_MUX_RW.TST1_BLOCK_SEL.value = Test1_block

                self.dut.IVM.REG_PWRUP2_RW.DS_INDCS_CLR_OCP.value = 1
                sleep(0.3)
                self.dut.IVM.REG_FORCE_RW.DS_PH1_INDCS_FORCE_SEL.value = 0
                self.dut.IVM.REG_FORCE_RW.DS_PH1_INDCS_FORCE_EN.value = 1
                self.dut.IVM.REG_TEST0_RW.DS_PH1_DRV_TEST_HS.value = 0
                self.dut.IVM.REG_TEST0_RW.DS_PH1_DRV_TEST_EN.value = 1
                self.dut.IVM.REG_PWRUP2_RW.DS_INDCS_CLR_OCP.value = 0
            if phase == 'PH2S1':
                self.dut.IVM.REG_DRV_INDCS_RW.DS_PH2_INDCS_PROG_OCP.value = current_index
                self.dut.IVM.REG_PWRUP1_RW.DS_PH2_INDCS_EN_OCP.value = 1
                self.dut.IVM.REG_VIS_MUX_RW.TST1_SEL.value =  TestSignal
                self.dut.IVM.REG_VIS_MUX_RW.TST1_BLOCK_SEL.value = Test1_block

                self.dut.IVM.REG_PWRUP2_RW.DS_INDCS_CLR_OCP.value = 1
                sleep(0.2)
                self.dut.IVM.REG_FORCE_RW.DS_PH2_INDCS_FORCE_SEL.value = 1
                self.dut.IVM.REG_FORCE_RW.DS_PH2_INDCS_FORCE_EN.value = 1
                self.dut.IVM.REG_TEST0_RW.DS_PH2_INDCS_TEST_SEL.value = 1
                self.dut.IVM.REG_TEST0_RW.DS_PH2_INDCS_TEST_EN.value = 1
                self.dut.IVM.REG_TEST0_RW.DS_PH2_DRV_TEST_HS.value = 1
                self.dut.IVM.REG_TEST0_RW.DS_PH2_DRV_TEST_EN.value = 1
                self.dut.IVM.REG_PWRUP2_RW.DS_INDCS_CLR_OCP.value = 0
            if phase == 'PH2S4':
                self.dut.IVM.REG_DRV_INDCS_RW.DS_PH2_INDCS_PROG_OCP.value = current_index
                self.dut.IVM.REG_PWRUP1_RW.DS_PH2_INDCS_EN_OCP.value = 1
                self.dut.IVM.REG_VIS_MUX_RW.TST1_SEL.value =  TestSignal
                self.dut.IVM.REG_VIS_MUX_RW.TST1_BLOCK_SEL.value = Test1_block

                self.dut.IVM.REG_PWRUP2_RW.DS_INDCS_CLR_OCP.value = 1
                sleep(0.2)
                self.dut.IVM.REG_FORCE_RW.DS_PH2_INDCS_FORCE_SEL.value = 0
                self.dut.IVM.REG_FORCE_RW.DS_PH2_INDCS_FORCE_EN.value = 1
                self.dut.IVM.REG_TEST0_RW.DS_PH2_DRV_TEST_HS.value = 0
                self.dut.IVM.REG_TEST0_RW.DS_PH2_DRV_TEST_EN.value = 1
                self.dut.IVM.REG_PWRUP2_RW.DS_INDCS_CLR_OCP.value = 0
            if phase == 'PH3S1':
                self.dut.IVM.REG_DRV_INDCS_RW.DS_PH3_INDCS_PROG_OCP.value = current_index
                self.dut.IVM.REG_PWRUP1_RW.DS_PH3_INDCS_EN_OCP.value = 1
                self.dut.IVM.REG_VIS_MUX_RW.TST1_SEL.value =  TestSignal
                self.dut.IVM.REG_VIS_MUX_RW.TST1_BLOCK_SEL.value = Test1_block

                self.dut.IVM.REG_PWRUP2_RW.DS_INDCS_CLR_OCP.value = 1
                sleep(0.2)
                self.dut.IVM.REG_FORCE_RW.DS_PH3_INDCS_FORCE_SEL.value = 1
                self.dut.IVM.REG_FORCE_RW.DS_PH3_INDCS_FORCE_EN.value = 1
                self.dut.IVM.REG_TEST0_RW.DS_PH3_INDCS_TEST_SEL.value = 1
                self.dut.IVM.REG_TEST0_RW.DS_PH3_INDCS_TEST_EN.value = 1
                self.dut.IVM.REG_TEST0_RW.DS_PH3_DRV_TEST_HS.value = 1
                self.dut.IVM.REG_TEST0_RW.DS_PH3_DRV_TEST_EN.value = 1
                self.dut.IVM.REG_PWRUP2_RW.DS_INDCS_CLR_OCP.value = 0
            if phase == 'PH3S4':
                self.dut.IVM.REG_DRV_INDCS_RW.DS_PH3_INDCS_PROG_OCP.value = current_index
                self.dut.IVM.REG_PWRUP1_RW.DS_PH3_INDCS_EN_OCP.value = 1
                self.dut.IVM.REG_VIS_MUX_RW.TST1_SEL.value =  TestSignal
                self.dut.IVM.REG_VIS_MUX_RW.TST1_BLOCK_SEL.value = Test1_block
                self.dut.IVM.REG_PWRUP2_RW.DS_INDCS_CLR_OCP.value = 1
                sleep(0.2)
                self.dut.IVM.REG_FORCE_RW.DS_PH3_INDCS_FORCE_SEL.value = 0
                self.dut.IVM.REG_FORCE_RW.DS_PH3_INDCS_FORCE_EN.value = 1
                self.dut.IVM.REG_TEST0_RW.DS_PH3_DRV_TEST_HS.value = 0
                self.dut.IVM.REG_TEST0_RW.DS_PH3_DRV_TEST_EN.value = 1
                self.dut.IVM.REG_PWRUP2_RW.DS_INDCS_CLR_OCP.value = 0
            if phase == 'PH4S1':
                self.dut.IVM.REG_DRV_INDCS_RW.DS_PH4_INDCS_PROG_OCP.value = current_index
                self.dut.IVM.REG_PWRUP1_RW.DS_PH4_INDCS_EN_OCP.value = 1
                self.dut.IVM.REG_VIS_MUX_RW.TST1_SEL.value =  TestSignal
                self.dut.IVM.REG_VIS_MUX_RW.TST1_BLOCK_SEL.value = Test1_block
                self.dut.IVM.REG_PWRUP2_RW.DS_INDCS_CLR_OCP.value = 1
                sleep(0.2)
                self.dut.IVM.REG_FORCE_RW.DS_PH4_INDCS_FORCE_SEL.value = 1
                self.dut.IVM.REG_FORCE_RW.DS_PH4_INDCS_FORCE_EN.value = 1
                self.dut.IVM.REG_TEST0_RW.DS_PH4_INDCS_TEST_SEL.value = 1
                self.dut.IVM.REG_TEST0_RW.DS_PH4_INDCS_TEST_EN.value = 1
                self.dut.IVM.REG_TEST0_RW.DS_PH4_DRV_TEST_HS.value = 1
                self.dut.IVM.REG_TEST0_RW.DS_PH4_DRV_TEST_EN.value = 1
                self.dut.IVM.REG_PWRUP2_RW.DS_INDCS_CLR_OCP.value = 0
            if phase == 'PH4S4':
                self.dut.IVM.REG_DRV_INDCS_RW.DS_PH4_INDCS_PROG_OCP.value = current_index
                self.dut.IVM.REG_PWRUP1_RW.DS_PH4_INDCS_EN_OCP.value = 1
                self.dut.IVM.REG_VIS_MUX_RW.TST1_SEL.value =  TestSignal
                self.dut.IVM.REG_VIS_MUX_RW.TST1_BLOCK_SEL.value = Test1_block
                self.dut.IVM.REG_PWRUP2_RW.DS_INDCS_CLR_OCP.value = 1
                sleep(0.2)
                self.dut.IVM.REG_FORCE_RW.DS_PH4_INDCS_FORCE_SEL.value = 0
                self.dut.IVM.REG_FORCE_RW.DS_PH4_INDCS_FORCE_EN.value = 1
                self.dut.IVM.REG_TEST0_RW.DS_PH4_DRV_TEST_HS.value = 0
                self.dut.IVM.REG_TEST0_RW.DS_PH4_DRV_TEST_EN.value = 1
                self.dut.IVM.REG_PWRUP2_RW.DS_INDCS_CLR_OCP.value = 0
        else:
                self.matrix.reset()
                self.dut.IVM.REG_TEST0_RW.DS_PH1_INDCS_TEST_EN.value = 0
                self.dut.IVM.REG_TEST0_RW.DS_PH1_INDCS_TEST_SEL.value = 0
                self.dut.IVM.REG_TEST0_RW.DS_PH2_INDCS_TEST_EN.value = 0
                self.dut.IVM.REG_TEST0_RW.DS_PH2_INDCS_TEST_SEL.value = 0
                self.dut.IVM.REG_TEST0_RW.DS_PH3_INDCS_TEST_EN.value = 0
                self.dut.IVM.REG_TEST0_RW.DS_PH3_INDCS_TEST_SEL.value = 0
                self.dut.IVM.REG_TEST0_RW.DS_PH4_INDCS_TEST_EN.value = 0
                self.dut.IVM.REG_TEST0_RW.DS_PH4_INDCS_TEST_SEL.value = 0
                self.dut.IVM.REG_FORCE_RW.DS_PH1_INDCS_FORCE_EN.value = 0
                self.dut.IVM.REG_FORCE_RW.DS_PH1_INDCS_FORCE_SEL.value = 0
                self.dut.IVM.REG_TEST0_RW.DS_PH1_DRV_TEST_EN.value = 0
                self.dut.IVM.REG_TEST0_RW.DS_PH1_DRV_TEST_HS.value = 0
                self.dut.IVM.REG_FORCE_RW.DS_PH2_INDCS_FORCE_EN.value = 0
                self.dut.IVM.REG_FORCE_RW.DS_PH2_INDCS_FORCE_SEL.value = 0
                self.dut.IVM.REG_TEST0_RW.DS_PH2_DRV_TEST_EN.value = 0
                self.dut.IVM.REG_TEST0_RW.DS_PH2_DRV_TEST_HS.value = 0
                self.dut.IVM.REG_FORCE_RW.DS_PH3_INDCS_FORCE_EN.value = 0
                self.dut.IVM.REG_FORCE_RW.DS_PH3_INDCS_FORCE_SEL.value = 0
                self.dut.IVM.REG_TEST0_RW.DS_PH3_DRV_TEST_EN.value = 0
                self.dut.IVM.REG_TEST0_RW.DS_PH3_DRV_TEST_HS.value = 0
                self.dut.IVM.REG_FORCE_RW.DS_PH4_INDCS_FORCE_EN.value = 0
                self.dut.IVM.REG_FORCE_RW.DS_PH4_INDCS_FORCE_SEL.value = 0
                self.dut.IVM.REG_TEST0_RW.DS_PH4_DRV_TEST_EN.value = 0
                self.dut.IVM.REG_TEST0_RW.DS_PH4_DRV_TEST_HS.value = 0
                self.dut.IVM.REG_VIS_MUX_RW.TST2_SEL.value =  0
                self.dut.IVM.REG_VIS_MUX_RW.TST2_BLOCK_SEL.value = 0
    # Measure the inductor current sense ocp thershold 700mV+75mV(per 1A)
    def Indctor_OCP_Reference__Sweep(self,sheet='device2_reference'):
        self.startup.buck_PowerUp()
        self.loadtrims.loadTrims()
        input('>>>>>>>>>')
        phases = {0:'PH1S1',1:'PH2S1',2:'PH3S1',3:'PH4S1'}
        try :
            ocp_th = [[],[],[],[]]
            ocp_ref_th = [[],[],[],[]]
            ocp_ref_meas = [[],[],[],[]]
            error = [[],[],[],[]]
            test_phase = 0xe
            for phaseIndex,phase in phases.items() :
                print(phase)
                self.matrix.reset()
                sleep(0.1)
                print('phase',phase)
                sleep(0.1)
                self.dut.IVM.REG_TEST0_RW.DS_TEST1_VIS_SEL.value = test_phase
                self.dut.IVM.REG_TEST0_RW.DS_TEST1_VIS_EN.value = 1
                for i in range(0,5,1):
                    self.Phase_Select(phase,TestSignal=phaseIndex,current_index=i,DriverEnable=True)
                    sleep(0.1)
                    ocp_th[phaseIndex].append(5+0.5*i)
                    ocp_ref_th[phaseIndex].append(ocp_th[phaseIndex][-1]*0.075)
                    ocp_ref_meas[phaseIndex].append(self.voltmeter.meas_V()- 0.7)
                    error[phaseIndex].append(((ocp_ref_meas[phaseIndex][-1] - ocp_ref_th[phaseIndex][-1])/ocp_ref_th[phaseIndex][-1])*100)
                test_phase=test_phase-1
            writeInExcel(sheet=sheet,filename='InnerLoop_Char\InnerLoop_Reference_0C.xlsx',ph1_ocp_th = ocp_th[0],ph1_ocp_ref_th=ocp_ref_th[0],ph1_ocp_ref_meas=ocp_ref_meas[0],ph1_error=error[0],\
                          ph2_ocp_th = ocp_th[1],ph2_ocp_ref_th=ocp_ref_th[1],ph2_ocp_ref_meas=ocp_ref_meas[1],ph2_error=error[1],\
                          ph3_ocp_th = ocp_th[2],ph3_ocp_ref_th=ocp_ref_th[2],ph3_ocp_ref_meas=ocp_ref_meas[2],ph3_error=error[2],\
                          ph4_ocp_th = ocp_th[3],ph4_ocp_ref_th=ocp_ref_th[3],ph4_ocp_ref_meas=ocp_ref_meas[3],ph4_error=error[3])
        except KeyboardInterrupt:
            self.Phase_Select(DriverEnable=False)

    def ZC_Sweep(self,sheet='High'):

        self.scope.set_HScale(scale='800E-9')
        self.scope.set_Channel__VScale(scale=0.2)
        self.scope.set_trigger__level(level=0.2)
        self.scope.set_trigger__mode(mode='NORM')
        self.scope.init_scopePosEdge__Trigger()
        sleep(0.1)
        self.startup.buck_PowerUp()
        self.loadtrims.loadTrims()
        self.supply.setCurrent(channel=3,current=0)
        sleep(0.2)
        self.scope.scopeTrigger_Acquire(channel='CH1')
        phases = {0:'PH1S1',1:'PH2S1',2:'PH3S1',3:'PH4S1'}
        if re.search('Low',sheet):
            phases = {0:'PH1S4',1:'PH2S4',2:'PH3S4',3:'PH4S4'}
        input('Check Temperature >>>>>>>>')
        # phases = {0:'PH1S1'}
        try :
            zc_th = [[],[],[],[]]
            zc_meas = [[],[],[],[]]
            zc_stepsize = [[],[],[],[]]
            error = [[],[],[],[]]
            for phaseIndex,phase in phases.items() :

                print(phase,len(phases))
                self.matrix.reset()
                print(f'Operating Phase {phase} and the Phase Index {phaseIndex}')
                self.supply.setVoltage(channel=3,voltage=4.5)
                self.supply.outp_ON(channel=4)
                sleep(0.1)
                self.Phase_Select(phase,Test1_block=4,TestSignal=phaseIndex,current_index=0,DriverEnable=True)
                sleep(0.1)
                self.supply.outp_OFF(channel=4)
                sleep(0.1)
                self.scope.scopeTrigger_Acquire()
                sleep(1)
                if True:
                    for j in range(0,24,4):
                        self.Zc_select(phase=phase,zc_threshold=j)
                        # if i >= 32:
                        #     zc_th[phaseIndex].append(0.0322*32 - i*0.0322)
                        # else:
                        zc_th[phaseIndex].append( j*0.0322)
                        current= -(abs(zc_th[phaseIndex][-1]) + 0.2)
                        sleep(0.1)
                        self.supply.setCurrent(channel=3,current=current)
                        self.supply.outp_ON(channel=3)
                        sleep(0.1)
                        self.scope.scopeTrigger_Acquire()
                        sleep(0.5)
                        # print('first loop')
                        while(self.scope.scopeAcquire_BUSY):
                                sleep(0.005)
                                self.supply.setCurrent(channel=3,current=current)
                                current=current+0.001
                                # if current > (abs(zc_th[phaseIndex][-1])*2 + 0.3):
                                #     break
                        zc_meas[phaseIndex].append(-1*self.supply.getCurrent(channel=3))
                        self.supply.setCurrent(channel=3,current=0)
                        if abs(zc_th[phaseIndex][-1]) == 0:
                            error[phaseIndex].append(zc_meas[phaseIndex][0])
                        else:
                            error[phaseIndex].append(((abs(zc_meas[phaseIndex][-1]) - abs(zc_th[phaseIndex][-1]))/abs(zc_th[phaseIndex][-1]))*100)

                        if len(zc_meas[phaseIndex]) > 1 :
                            step_size = (zc_meas[phaseIndex][-1] - zc_meas[phaseIndex][-2])/4
                            if abs(step_size) < 0.1:
                                zc_stepsize[phaseIndex].append(step_size)
                            else:
                                if zc_th[phaseIndex][-1] == 0:
                                    zc_stepsize[phaseIndex].append(zc_meas[phaseIndex][-1])

                        else:
                                zc_stepsize[phaseIndex].append(zc_meas[phaseIndex][0])
                        print(f'ZC Threshold {zc_th[phaseIndex][-1]} Triggered Curret {zc_meas[phaseIndex][-1]}, zc step size {zc_stepsize[phaseIndex][-1]},error {error[phaseIndex][-1]}')

                    for i in range(32,56,4):
                        self.Zc_select(phase=phase,zc_threshold=i)
                        if i >= 32:
                            zc_th[phaseIndex].append(0.0322*32 - i*0.0322)
                        else:
                            zc_th[phaseIndex].append( i*0.0322)
                        current= -0.2-zc_th[phaseIndex][-1]
                        sleep(0.1)
                        self.supply.setCurrent(channel=3,current=current)
                        self.supply.outp_ON(channel=3)
                        sleep(0.1)
                        self.scope.scopeTrigger_Acquire()
                        sleep(0.5)
                        while(self.scope.scopeAcquire_BUSY):
                                sleep(0.005)
                                self.supply.setCurrent(channel=3,current=current)
                                current=current+0.001
                                # if current > (abs(zc_th[phaseIndex][-1])*2 + 0.3):
                                #     break
                        zc_meas[phaseIndex].append(-1*self.supply.getCurrent(channel=3))
                        self.supply.setCurrent(channel=3,current=0)
                        if abs(zc_th[phaseIndex][-1]) == 0:
                            error[phaseIndex].append(zc_meas[phaseIndex][0])
                        else:
                            error[phaseIndex].append(((abs(zc_meas[phaseIndex][-1]) - abs(zc_th[phaseIndex][-1]))/abs(zc_th[phaseIndex][-1]))*100)

                        if len(zc_meas[phaseIndex]) > 1 :
                            step_size = (zc_meas[phaseIndex][-1] - zc_meas[phaseIndex][-2])/4
                            if abs(step_size) < 0.1:
                                zc_stepsize[phaseIndex].append(step_size)
                            else:
                                if zc_th[phaseIndex][-1] == 0:
                                    zc_stepsize[phaseIndex].append(zc_meas[phaseIndex][-1])

                        else:
                                zc_stepsize[phaseIndex].append(zc_meas[phaseIndex][0])
                        
                    

                       
                        print(f'ZC Threshold {zc_th[phaseIndex][-1]} Triggered Curret {zc_meas[phaseIndex][-1]}, zc step size {zc_stepsize[phaseIndex][-1]},error {error[phaseIndex][-1]}')
                    self.Phase_Select(DriverEnable=False)
                    if len(zc_stepsize[phaseIndex]) == len(zc_meas[phaseIndex]):
                        print(f'Phase {phase} Zc measurement Done ')
            writeInExcel(sheet=sheet,filename='InnerLoop_Char\InnerLoop_ZC_0C.xlsx',\
                         ph1_zc_th=zc_th[0],ph1_zc_meas = zc_meas[0],ph1_zc_stepsize = zc_stepsize[0],ph1_error = error[0],\
                         ph2_zc_th=zc_th[1],ph2_zc_meas = zc_meas[1],ph2_zc_stepsize = zc_stepsize[1],ph2_error = error[1],\
                         ph3_zc_th=zc_th[2],ph3_zc_meas = zc_meas[2],ph3_zc_stepsize = zc_stepsize[2],ph3_error = error[2],\
                         ph4_zc_th=zc_th[3],ph4_zc_meas = zc_meas[3],ph4_zc_stepsize = zc_stepsize[3],ph4_error = error[3],\
                            )
        except KeyboardInterrupt:
            self.supply.setCurrent(channel=3,current=0)
            pass 

    def Zc_select(self,phase='PH1S1',zc_threshold=0):

        if phase == 'PH1S1':
           self.dut.IVM.REG_TRIM10_RW.DS_PH1_INDCS_TRIM_ZC_S1.value=zc_threshold
        if phase == 'PH1S4':
           self.dut.IVM.REG_TRIM10_RW.DS_PH1_INDCS_TRIM_ZC_S4.value=zc_threshold
        if phase == 'PH2S1':
           self.dut.IVM.REG_TRIM8_RW.DS_PH2_INDCS_TRIM_ZC_S1.value=zc_threshold
        if phase == 'PH2S4':
           self.dut.IVM.REG_TRIM8_RW.DS_PH2_INDCS_TRIM_ZC_S4.value=zc_threshold
        if phase == 'PH3S1':
           self.dut.IVM.REG_TRIM6_RW.DS_PH3_INDCS_TRIM_ZC_S1.value=zc_threshold
        if phase == 'PH3S4':
           self.dut.IVM.REG_TRIM6_RW.DS_PH3_INDCS_TRIM_ZC_S4.value=zc_threshold
        if phase == 'PH4S1':
           self.dut.IVM.REG_TRIM4_RW.DS_PH4_INDCS_TRIM_ZC_S1.value=zc_threshold
        if phase == 'PH4S4':
           self.dut.IVM.REG_TRIM4_RW.DS_PH4_INDCS_TRIM_ZC_S4.value=zc_threshold
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
        # self.multimeter.set_meter_External__Positivetrigger___Voltage()
        # self.multimeter.set_meter_TriggerSlope__Positve()
        # self.multimeter.set_meter__Trigger___Delay(delay=0)
        self.multimeter.set_Voltage__NPLC(NPLC=1)
        self.matrix = Matrix()
        self.loadtrims = loadtrims
        # self.InputCurr_Step()
        # self.Inductor_OCP_static(sheet='High_1')
        # self.Indcs_Sweep_static(sheet='Device1_4phases_indcs_Low_sweep')
        # input('Turn on Temperature for 85C')
        # self.Inductor_OCP_static(sheet='Device2_4phases_HighSide_85C_OCP')
        # self.Inductor_OCP_static__HighSide(sheet='Device3_HighSide_85C_OCP')
        # input('Switch Termials for low Side  25C')
        # self.Inductor_OCP_static__LowSide(sheet='Device3_LOWSide_25C_OCP')
        # input('Switch Termials and Turn on Temperature for low Side  85C')
        # self.Inductor_OCP_static__LowSide(sheet='Device3_LOWSide_85C_OCP')
        # self.Inductor_OCP_4Phase__static___HighSide()
        self.Indctor_OCP_Reference__Sweep(sheet='device2_reference')

    def InputCurr_Step(self):
        self.scope.set_HScale(scale='20E-3')
        self.scope.set_Channel__VScale(scale=0.2)
        self.scope.set_trigger__level(level=0.1)
        self.scope.set_trigger__mode(mode='NORM')
        self.scope.init_scopePosEdge__Trigger()
        # for i in range(1,8,1):
        for i in range(1,8,1):
            self.supply.setCurrent(channel=1,current=0)
            self.scope.scopeTrigger_Acquire()
            while(self.scope.scopeAcquire_BUSY):
                sleep(0.01)
                self.supply.setCurrent(channel=1,current=0)
                sleep(0.01)
                self.supply.setCurrent(channel=1,current=-i)
            # sleep(0.01)
            # self.supply.setCurrent(channel=1,current=0)
            # sleep(0.1)
            print(self.scope.Meas_Amp())
            sleep(0.1)
            # print(self.scope.Meas_Amp(Meas='MEAS2'))
    
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
            self.scope.scopeTrigger_Acquire(channel='CH1')
            if re.search('High',sheet):
                
                phases = {0:'PH1S1'}
                # phases = {0:'PH1S1',1:'PH2S1',2:'PH3S1',3:'PH4S1'}
                try :
                    loadCurrent = [[],[],[],[]]
                    OCPthershold = [[],[],[],[]]
                    IndcsVoltage = [[],[],[],[]]
                    error = [[],[],[],[]]
                    for phaseIndex,phase in phases.items() :
                        print(phase)
                        self.matrix.reset()
                        current = 4.0
                        sleep(0.1)
                        for i in range(0,5,1):
                            self.Phase_Select(phase,TestSignal=phaseIndex,current_index=i,DriverEnable=True)
                            print('i',i,'phase',phase)
                            sleep(0.1)
                            if abs(self.supply.getVoltage(channel=1)) > 2.5:
                                self.scope.scopeTrigger_Acquire(channel='CH1')
                                input('>>>>>>')
                                while(self.scope.scopeAcquire_BUSY):
                                    self.supply.setCurrent(channel=1,current=-current)
                                    current=current+0.001
                                    if current > 7.5:
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
                                tempcurrent = current - 0.1
                                while current >= tempcurrent :
                                    self.supply.setCurrent(channel=1,current=-current)
                                    current=current-0.1
                                    sleep(0.0001)
                        while current >= 0 :
                            self.supply.setCurrent(channel=1,current=-current)
                            current=current-0.5
                            sleep(0.01)
                        self.Phase_Select(DriverEnable=False)
                    writeInExcel(sheet=sheet,filename='InnerLoop_Char\InnerLoop_Char2.xlsx',ph1_OCPthershold=OCPthershold[0],ph1_loadCurrent=loadCurrent[0],ph1_IndcsVoltage=IndcsVoltage[0],ph1_error=error[0], \
                                 ph2_OCPthershold=OCPthershold[1],ph2_loadCurrent=loadCurrent[1],ph2_IndcsVoltage=IndcsVoltage[1],ph2_error=error[1],ph3_OCPthershold=OCPthershold[2],ph3_loadCurrent=loadCurrent[2],ph3_IndcsVoltage=IndcsVoltage[2],ph3_error=error[2],\
                                 ph4_OCPthershold=OCPthershold[3],ph4_loadCurrent=loadCurrent[3],ph4_IndcsVoltage=IndcsVoltage[3],ph4_error=error[3])
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
                        current =4.0
                        sleep(0.1)
                        for i in range(0,5,1):
                            self.Phase_Select(phase,TestSignal=phaseIndex,current_index=i,DriverEnable=True)

                            self.scope.scopeTrigger_Acquire(channel='CH1')
                            sleep(0.1)
                            # input('>>>>>>')
                            # if abs(self.supply.getVoltage(channel=1)) <= 0:
                            if True:
                                while(self.scope.scopeAcquire_BUSY):
                                    self.supply.setCurrent(channel=1,current=current)
                                    current=current+0.001
                                    if current > 7.5:
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
                    writeInExcel(sheet=sheet,filename='InnerLoop_Char\InnerLoop_Char2.xlsx',ph1_OCPthershold=OCPthershold[0],ph1_loadCurrent=loadCurrent[0],ph1_IndcsVoltage=IndcsVoltage[0],ph1_error=error[0], \
                                 ph2_OCPthershold=OCPthershold[1],ph2_loadCurrent=loadCurrent[1],ph2_IndcsVoltage=IndcsVoltage[1],ph2_error=error[1],ph3_OCPthershold=OCPthershold[2],ph3_loadCurrent=loadCurrent[2],ph3_IndcsVoltage=IndcsVoltage[2],ph3_error=error[2],\
                                 ph4_OCPthershold=OCPthershold[3],ph4_loadCurrent=loadCurrent[3],ph4_IndcsVoltage=IndcsVoltage[3],ph4_error=error[3])
                except KeyboardInterrupt:
                    while current >= 0 :
                        self.supply.setCurrent(channel=1,current=current)
                        current=current-0.01
                        sleep(0.01)
    def Indcs_Sweep_static(self,sheet='Device1_4phases_indcs_High_sweep'):
            
            self.startup.buck_PowerUp()
            self.loadtrims.loadTrims()
            self.supply.setCurrent(channel=1,current=0)
            sleep(0.2)
            if re.search('High',sheet):
                
                phases = {2:'PH3S1'}
                # phases = {0:'PH1S1',1:'PH2S1',2:'PH3S1',3:'PH4S1'}
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
                        if abs(self.supply.getVoltage(channel=1)) > 2.5:
                            # input('>>>>>>')
                            while current < 7.61:
                                self.supply.setCurrent(channel=1,current=-current)
                                sleep(0.05)
                                loadCurrent[phaseIndex].append(abs(self.supply.getCurrent(channel=1)))
                                IndcsVoltage[phaseIndex].append(self.multimeter.meas_V())
                                IndcsVoltage_th[phaseIndex].append(0.075*current)
                                error[phaseIndex].append((((IndcsVoltage[phaseIndex][-1]) - IndcsVoltage_th[phaseIndex][-1])/(IndcsVoltage_th[phaseIndex][-1]))*100)
                                current=current+0.1
                        while current >= 0 :
                            self.supply.setCurrent(channel=1,current=-current)
                            current=current-0.01
                            sleep(0.01)
                        self.Phase_Select(DriverEnable=False)
                    writeInExcel(sheet=sheet,filename='InnerLoop_Char\InnerLoop_Char2.xlsx',ph1_IndcsVoltage_th=IndcsVoltage_th[0],ph1_loadCurrent=loadCurrent[0],ph1_IndcsVoltage=IndcsVoltage[0],ph1_error=error[0], \
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
                                error[phaseIndex].append((((IndcsVoltage[phaseIndex][-1]) - IndcsVoltage_th[phaseIndex][-1])/(IndcsVoltage_th[phaseIndex][-1]))*100)
                                current=current+0.1
                        while current >= 0 :
                            self.supply.setCurrent(channel=1,current=current)
                            current=current-0.01
                            sleep(0.01)
                        self.Phase_Select(DriverEnable=False)
                    writeInExcel(sheet=sheet,filename='InnerLoop_Char\InnerLoop_Char2.xlsx',ph1_IndcsVoltage_th=IndcsVoltage_th[0],ph1_loadCurrent=loadCurrent[0],ph1_IndcsVoltage=IndcsVoltage[0],ph1_error=error[0], \
                                 ph2_IndcsVoltage_th=IndcsVoltage_th[1],ph2_loadCurrent=loadCurrent[1],ph2_IndcsVoltage=IndcsVoltage[1],ph2_error=error[1],ph3_IndcsVoltage_th=IndcsVoltage_th[2],ph3_loadCurrent=loadCurrent[2],ph3_IndcsVoltage=IndcsVoltage[2],ph3_error=error[2],\
                                 ph4_IndcsVoltage_th=IndcsVoltage_th[3],ph4_loadCurrent=loadCurrent[3],ph4_IndcsVoltage=IndcsVoltage[3],ph4_error=error[3])
                except KeyboardInterrupt:
                    while current >= 0 :
                        self.supply.setCurrent(channel=1,current=current)
                        current=current-0.01
                        sleep(0.01)

    def Inductor_OCP_4Phase__static___HighSide(self,sheet='Device1_HighSide_25C_OCP'):
        self.scope.set_HScale(scale='1E-3')
        self.scope.set_Channel__VScale(scale=0.2)
        self.scope.set_trigger__level(level=0.2)
        self.scope.set_trigger__mode(mode='NORM')
        self.scope.init_scopePosEdge__Trigger()
        sleep(0.1)
        self.startup.buck_PowerUp()
        self.loadtrims.loadTrims()
        self.supply.setCurrent(channel=1,current=0)

        phases = {0:'PH1S1',1:'PH2S1',2:'PH3S1',3:'PH4S1'}

        try :
            for phaseIndex,phase in phases.items() :
                for i in range(0,5,1):
                    self.Phase_Select(phase,TestSignal=phaseIndex,current_index=i,DriverEnable=True)
                    self.scope.scopeTrigger_Acquire(channel='CH1')
                    self.supply.arb_Trapezoid__Current(channel=1,initial_Current=0,end_Current=-(5+i*0.5+0.2),initial_Time=0,raise_Time=0.5,top_Time=0.01,fall_Time=0.5,end_Time=0)
                    print('Press RUN/STOP')
                    self.supply.arb_Trigger()
                    index=0
                    while(self.scope.scopeAcquire_BUSY):
                        index=index+1
                    # input('>')
                    # print(f'Measured voltage {self.multimeter.fetch_meter__Reading()}')
                self.Phase_Select(DriverEnable=False)
        except KeyboardInterrupt:
            pass

    def Phase_Select(self,phase='PH1S1',TestSignal=0,current_index=0,DriverEnable=False):
        self.matrix.force_Matrix__Switchx(phase)
        sleep(0.2)
        if DriverEnable:
            if phase == 'PH1S1':
                self.dut.IVM.REG_DRV_INDCS_RW.DS_PH1_INDCS_PROG_OCP.value = current_index
                sleep(0.1)
                self.dut.IVM.REG_PWRUP1_RW.DS_PH1_INDCS_EN_OCP.value = 1
                self.dut.IVM.REG_VIS_MUX_RW.TST1_SEL.value =  TestSignal
                self.dut.IVM.REG_VIS_MUX_RW.TST1_BLOCK_SEL.value = 0x3
                self.dut.IVM.REG_PWRUP2_RW.DS_INDCS_CLR_OCP.value = 1
                sleep(0.2)
                self.dut.IVM.REG_FORCE_RW.DS_PH1_INDCS_FORCE_SEL.value = 1
                self.dut.IVM.REG_FORCE_RW.DS_PH1_INDCS_FORCE_EN.value = 1
                self.dut.IVM.REG_TEST0_RW.DS_PH1_INDCS_TEST_SEL.value = 1
                self.dut.IVM.REG_TEST0_RW.DS_PH1_INDCS_TEST_EN.value = 1
                self.dut.IVM.REG_TEST0_RW.DS_PH1_DRV_TEST_HS.value = 1
                self.dut.IVM.REG_TEST0_RW.DS_PH1_DRV_TEST_EN.value = 1
                self.dut.IVM.REG_PWRUP2_RW.DS_INDCS_CLR_OCP.value = 0
            if phase == 'PH1S4':
                self.dut.IVM.REG_DRV_INDCS_RW.DS_PH1_INDCS_PROG_OCP.value = current_index
                self.dut.IVM.REG_PWRUP1_RW.DS_PH1_INDCS_EN_OCP.value = 1
                self.dut.IVM.REG_VIS_MUX_RW.TST1_SEL.value =  TestSignal
                self.dut.IVM.REG_VIS_MUX_RW.TST1_BLOCK_SEL.value = 0x3
                self.dut.IVM.REG_PWRUP2_RW.DS_INDCS_CLR_OCP.value = 1
                sleep(0.2)
                self.dut.IVM.REG_FORCE_RW.DS_PH1_INDCS_FORCE_SEL.value = 0
                self.dut.IVM.REG_FORCE_RW.DS_PH1_INDCS_FORCE_EN.value = 1
                self.dut.IVM.REG_TEST0_RW.DS_PH1_DRV_TEST_HS.value = 0
                self.dut.IVM.REG_TEST0_RW.DS_PH1_DRV_TEST_EN.value = 1
                self.dut.IVM.REG_PWRUP2_RW.DS_INDCS_CLR_OCP.value = 0
            if phase == 'PH2S1':
                self.dut.IVM.REG_DRV_INDCS_RW.DS_PH2_INDCS_PROG_OCP.value = current_index
                self.dut.IVM.REG_PWRUP1_RW.DS_PH2_INDCS_EN_OCP.value = 1
                self.dut.IVM.REG_VIS_MUX_RW.TST1_SEL.value =  TestSignal
                self.dut.IVM.REG_VIS_MUX_RW.TST1_BLOCK_SEL.value = 0x3
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
                self.dut.IVM.REG_VIS_MUX_RW.TST1_BLOCK_SEL.value = 0x3
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
                self.dut.IVM.REG_VIS_MUX_RW.TST1_BLOCK_SEL.value = 0x3
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
                self.dut.IVM.REG_VIS_MUX_RW.TST1_BLOCK_SEL.value = 0x3
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
                self.dut.IVM.REG_VIS_MUX_RW.TST1_BLOCK_SEL.value = 0x3
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
                self.dut.IVM.REG_VIS_MUX_RW.TST1_BLOCK_SEL.value = 0x3
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

    def Indctor_OCP_Reference__Sweep(self,sheet='device2_reference'):
        self.startup.buck_PowerUp()
        self.loadtrims.loadTrims()
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
                current = 0.1
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
                    ocp_ref_meas[phaseIndex].append(self.multimeter.meas_V()- 0.7)
                    error[phaseIndex].append(((ocp_ref_meas[phaseIndex][-1] - ocp_ref_th[phaseIndex][-1])/ocp_ref_th[phaseIndex][-1])*100)
                test_phase=test_phase-1
            writeInExcel(sheet='reference',filename='InnerLoop_Char\InnerLoop_Char2.xlsx',ph1_ocp_th = ocp_th[0],ph1_ocp_ref_th=ocp_ref_th[0],ph1_ocp_ref_meas=ocp_ref_meas[0],ph1_error=error[0],\
                          ph2_ocp_th = ocp_th[1],ph2_ocp_ref_th=ocp_ref_th[1],ph2_ocp_ref_meas=ocp_ref_meas[1],ph2_error=error[1],\
                          ph3_ocp_th = ocp_th[2],ph3_ocp_ref_th=ocp_ref_th[2],ph3_ocp_ref_meas=ocp_ref_meas[2],ph3_error=error[2],\
                          ph4_ocp_th = ocp_th[3],ph4_ocp_ref_th=ocp_ref_th[3],ph4_ocp_ref_meas=ocp_ref_meas[3],ph4_error=error[3])
        except KeyboardInterrupt:
            self.Phase_Select(DriverEnable=False)

if __name__ =='__main__':
    pass 

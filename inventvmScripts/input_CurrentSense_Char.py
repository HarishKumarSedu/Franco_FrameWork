from Instruments_API import Instruments
from writeExcel import writeInExcel
from startup import Startup
from time import sleep

class InputCurrSense:

    def __init__(self,dut) -> None:
        self.dut=dut
        self.startup = Startup(dut=dut)
        self.supply = Instruments().supply
        self.scope = Instruments().scope
        self.multimeter = Instruments().multimeter
        self.voltmeter = Instruments().voltmeter
        self.multimeter.set_Voltage__NPLC(NPLC=1)
        # self.InputCurr_Step()
        # self.Input_CurrentSweep_dynamic()
        # self.Input_CS_Dynamic()
        self.InputCS_DC__Sweep(sheet='Device2_ibus_switching_3.3A_25C')
        input('85C')
        self.InputCS_DC__Sweep(sheet='Device2_ibus_switching_3.3A_85C')

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
    
    def Input_CurrentSweep_switching(self,sheet='Device3_85C_ibus_sweep_3.3A'):
        curr = 0
        self.supply.setCurrent(channel=1,current=-0.1)
        ibat_set  = []
        ibus_set = []
        external_ibus_cal = []
        external_ibus_voltage = []
        ibus_sns_ibus_cal = []
        ibus_sns_voltage = []
        ibus_sns_voltage = []
        error=[]
        try:
            while self.supply.getCurrent(channel=4) < 3.310:
                curr=curr+0.1
                self.supply.setCurrent(channel=1,current=-curr)
                sleep(1)
                ibat_set.append(abs(self.supply.getCurrent(channel=1)))
                ibus_set.append(self.supply.getCurrent(channel=4))
                # external_ibus_voltage.append(self.scope.Meas_Mean(Meas='MEAS2')- 3.5e-3)
                # external_ibus_cal.append(external_ibus_voltage[-1]/(10*0.025))
                ibus_sns_voltage.append(self.scope.Meas_Mean(Meas='MEAS1'))
                ibus_sns_ibus_cal.append((ibus_sns_voltage[-1]*2976)/(500))
                err = ((ibus_sns_ibus_cal[-1]-ibus_set[-1])/ibus_set[-1])*100
                if abs(err) > 2 and len(error) > 5:
                    print('error',err)
                    error.append(sum(error[-4:])/(len(error)-5))
                else:
                    error.append(err)

                # input('Single >>>>>>')
                print('ibus Current in A',self.supply.getCurrent(channel=4) )
            writeInExcel(sheet=sheet,filename='Input_CurrentSense\Input_CurrentSense_Char.xlsx',ibat_set=ibat_set,ibus_set=ibus_set,ibus_sns_voltage=ibus_sns_voltage,ibus_sns_ibus_cal=ibus_sns_ibus_cal,error=error)
            while curr >= 0:
                curr = curr - 0.1
                self.supply.setCurrent(channel=1,current=-curr)
                sleep(0.1)
            self.supply.setCurrent(channel=1,current=0)
        except:
            while curr <= 0:
                curr = curr - 0.1
                self.supply.setCurrent(channel=1,current=-curr)
                sleep(0.1)
    
    def Input_CS_Dynamic(self):
        try:
            ibus_ch1_offset = 0.0075
            external_ch4_offset = 0.0115
            currprobe_ch3_offset = 0.0035
            curr= 0
            ibatPeak_set = []
            ibus_mean = []
            external_ibus_cal = []
            external_ibus_voltage = []
            ibus_sns_ibus_cal = []
            ibus_sns_voltage = []
            ibus_sns_voltage = []

            self.startup.buck_PowerUp()
            self.dut.IVM.REG_TEST0_RW.DS_PH4_DRV_TEST_HS.value = 1
            self.dut.IVM.REG_TEST0_RW.DS_PH4_DRV_TEST_EN.value = 1
            sleep(1)
            if self.supply.getVoltage(channel=1) > 4.0:
                while curr < 6.1:
                    curr=curr+0.1
                    # input('>>>>>>>>')
                    self.supply.arb_Trapezoid__Current(channel=1,initial_Current=0,end_Current=-curr,initial_Time=0,raise_Time=1e-3,top_Time=0,fall_Time=1e-3,end_Time=0,count=6,LastOFF=0)
                    input('>>>>>>>>')
                    self.scope.scopeTrigger_Acquire()
                    sleep(1)
                    while True:
                        if not self.scope.scopeAcquire_BUSY :
                            break
                        else:
                            pass
                    ibatPeak_set.append(curr)
                    ibus_mean.append(self.scope.Meas_Mean(Meas='MEAS3')- currprobe_ch3_offset)
                    external_ibus_voltage.append(self.scope.Meas_Mean(Meas='MEAS2')- external_ch4_offset)
                    external_ibus_cal.append(external_ibus_voltage[-1]/(10*0.025))
                    ibus_sns_voltage.append(self.scope.Meas_Mean(Meas='MEAS1') - ibus_ch1_offset)
                    ibus_sns_ibus_cal.append((ibus_sns_voltage[-1]*2976)/(500))

                    print(f'ibatPeak_set : {ibatPeak_set[-1]} ibus_mean :{ibus_mean[-1]} external_ibus_cal:{external_ibus_cal[-1]} ibus_sns_ibus_cal: {ibus_sns_ibus_cal[-1]}')

            writeInExcel(sheet='Device1',filename='Input_CurrentSense\Input_CurrentSense_dynamic.xlsx',ibatPeak_set=ibatPeak_set,ibus_mean=ibus_mean,ibus_sns_voltage=ibus_sns_voltage,ibus_sns_ibus_cal=ibus_sns_ibus_cal,external_ibus_voltage=external_ibus_voltage,external_ibus_cal=external_ibus_cal)
        except KeyboardInterrupt:
            writeInExcel(sheet='Device1',filename='Input_CurrentSense\Input_CurrentSense_dynamic.xlsx',ibatPeak_set=ibatPeak_set,ibus_mean=ibus_mean,ibus_sns_voltage=ibus_sns_voltage,ibus_sns_ibus_cal=ibus_sns_ibus_cal,external_ibus_voltage=external_ibus_voltage,external_ibus_cal=external_ibus_cal)
            pass
        
    def InputCS_DC__Sweep(self,sheet='Device1_ibus_DCSweep_3.3A_25C'):
        try:
            current= 0
            self.supply.setVoltage(channel=4,voltage=5)
            self.supply.setCurrent(channel=1,current=current)
            # self.startup.buck_PowerUp()
            # sleep(0.1)
            # self.dut.IVM.REG_TEST0_RW.DS_PH1_DRV_TEST_EN.value = 1
            # self.dut.IVM.REG_TEST0_RW.DS_PH1_DRV_TEST_HS.value = 1
            self.startup.buck_ClosedLoop(vbat=4,ibat=16,icmd_ph=6,No_phase=1,ibus=3.3,phase=0)
            sleep(0.1)
            ibus_sns_voltage =[]
            ibus_sns_current =[]
            ibus_sns_gm =[]
            ibus=[]
            shunt_voltage=[]
            shunt_current=[]
            error=[]
            if self.supply.getVoltage(channel=1) > 2:
                while current < 3.6:
                    self.supply.setCurrent(channel=1,current=-current)
                    sleep(0.02)
                    ibus.append(self.supply.getCurrent(channel=4))
                    shunt_voltage.append(self.multimeter.meas_V())
                    shunt_current.append(shunt_voltage[-1]/0.025)
                    ibus_sns_voltage.append(self.voltmeter.meas_V())
                    ibus_sns_gm.append(((shunt_current[-1]*500)/ibus_sns_voltage[-1]))
                    current=current+0.02
                ibus_avg_gm = sum(ibus_sns_gm)/len(ibus_sns_gm)

                for i in range(0,len(ibus_sns_gm)):
                    ibus_sns_current.append((ibus_sns_voltage[i]*ibus_avg_gm)/500)
                    error.append(((ibus_sns_current[i]-shunt_current[i])/shunt_current[i])*100)
                writeInExcel(sheet=sheet,filename='Input_CurrentSense\Input_CurrentSense_switching.xlsx',ibus=ibus,shunt_voltage=shunt_voltage,\
                             shunt_current=shunt_current,ibus_sns_voltage=ibus_sns_voltage,ibus_sns_gm=ibus_sns_gm,\
                                ibus_sns_current=ibus_sns_current,error=error)
                while current>=0:
                    current=current-0.1
                    sleep(0.1)
                    self.supply.setCurrent(channel=1,current=-current)
                self.supply.setCurrent(channel=1,current=0)
            self.dut.IVM.REG_TEST0_RW.DS_PH1_DRV_TEST_EN.value = 0
            self.dut.IVM.REG_TEST0_RW.DS_PH1_DRV_TEST_HS.value = 0
        except KeyboardInterrupt:
                while current>=0:
                    current=current-0.1
                    sleep(0.1)
                    self.supply.setCurrent(channel=1,current=-current)
                self.supply.setCurrent(channel=1,current=0)



                    

if __name__ =='__main__':
    InputCurrSense()
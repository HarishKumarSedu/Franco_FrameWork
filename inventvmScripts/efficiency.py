from Instruments_API import Instruments
from writeExcel import writeInExcel
from startup import Startup
from time import sleep
class Efficiency:

    def __init__(self,dut) -> None:
        self.dut = dut
        self.startup = Startup(dut=dut)
        self.supply = Instruments().supply
        # self.Bat = Instruments().Battery
        # self.supply.setCurrent(channel=1,current=0)
        # self.Bat.rest()
        # self.Bat.setCurrent_Priority()
        # # self.Bat.setCurrent_Limit(current=-1)
        # self.Bat.setVoltage_Limit(voltage=4.3)
        # # self.Bat.setVoltage(voltage=4)
        # self.Bat.setCurrent(current=0)

        self.voltmeter = Instruments().voltmeter
        self.multimeter = Instruments().multimeter
        self.supply.outp_ON(channel=4)
        self.supply.outp_ON(channel=1)
        self.phase_Effieciency_1(phase=0,phase_thld=2,No_phase=1,vbus=9.0,loop_current_limit=-3.1,sheet='114_ph1_vbus9V_25C')
        sleep(0.1)
        self.phase_Effieciency_1(phase=1,phase_thld=2,No_phase=1,vbus=9.0,loop_current_limit=-3.1,sheet='114_ph2__vbus9V_25C')
        sleep(0.1)
        self.phase_Effieciency_1(phase=2,phase_thld=2,No_phase=1,vbus=9.0,loop_current_limit=-3.1,sheet='114_ph3_vbus9V_25C')
        sleep(0.1)
        self.phase_Effieciency_1(phase=3,phase_thld=2,No_phase=1,vbus=9.0,loop_current_limit=-3.1,sheet='114_ph4__vbus9V_25C')
        sleep(0.1)
        self.phase_Effieciency_1(phase=0,phase_thld=2,No_phase=2,vbus=9.0,loop_current_limit=-6.1,sheet='114_ph12_vbus9V_25C')
        sleep(0.1)
        self.phase_Effieciency_1(phase=2,phase_thld=2,No_phase=2,vbus=9.0,loop_current_limit=-6.1,sheet='114_ph34_vbus9V_25C')
        
        sleep(0.1)
        self.phase_Effieciency_1(phase=0,phase_thld=2,No_phase=1,vbus=15.0,loop_current_limit=-3.1,sheet='114_ph1_vbus15V_25C')
        sleep(0.1)
        self.phase_Effieciency_1(phase=1,phase_thld=2,No_phase=1,vbus=15.0,loop_current_limit=-3.1,sheet='114_ph2__vbus15V_25C')
        sleep(0.1)
        self.phase_Effieciency_1(phase=2,phase_thld=2,No_phase=1,vbus=15.0,loop_current_limit=-3.1,sheet='114_ph3_vbus15V_25C')
        sleep(0.1)
        self.phase_Effieciency_1(phase=3,phase_thld=2,No_phase=1,vbus=15.0,loop_current_limit=-3.1,sheet='114_ph4__vbus15V_25C')
        sleep(0.1)
        self.phase_Effieciency_1(phase=0,phase_thld=2,No_phase=2,vbus=15.0,loop_current_limit=-6.1,sheet='114_ph12_vbus15V_25C')
        sleep(0.1)
        self.phase_Effieciency_1(phase=2,phase_thld=2,No_phase=2,vbus=15.0,loop_current_limit=-6.1,sheet='114_ph34_vbus15V_25C')
        
        # self.phase_Effieciency_1(phase=0,phase_thld=2,No_phase=2,vbus=15.0,loop_current_limit=-6.1,sheet='dummy')
        # sleep(0.1)
        # self.phase_Effieciency_1(phase=2,phase_thld=2,No_phase=2,vbus=15.0,loop_current_limit=-6.1,sheet='dummy')
        
        self.supply.outp_OFF(channel=1)
        if self.supply.getVoltage(channel=4) >= 9:
            self.supply.setVoltage(channel=4,voltage=5)
        self.supply.outp_OFF(channel=4)
       

    def phase_Effieciency(self,phase=0,vbus=5.0,loop_current_limit=-3.005,sheet='ph1_vbat_4V_vbus_5V',):
        print(sheet)
        self.supply.setVoltage(channel=4,voltage=vbus)
        self.startup.buck_ClosedLoop(vbat=4,ibat=14.0,No_phase=3,icmd_ph=3.2,phase=phase)
        self.dut.IVM.REG_DRV_INDCS_RW.DS_DRV_SLEW.value = 1
        if vbus > 8 :
            self.dut.IVM.REG_DRV_INDCS_RW.DS_DRV_SLEW.value = 3
        sleep(0.1)
        ibat_set = -6.0
        self.supply.setCurrent(channel=1,current=ibat_set)
        vbat_V = []
        vbus_V = []
        ibus_A = []
        ibat_A = []
        efficiency = []
        try :
            if self.supply.getCurrent(channel=1) < -0.01:
                while self.supply.getCurrent(channel=1) < 0:
                    # vbat_V.append(self.supply.getVoltage(channel=1))
                    vbat_V.append(self.voltmeter.meas_V())
                    ibat_A.append(abs(self.supply.getCurrent(channel=1)))
                    vbus_V.append(self.supply.getVoltage(channel=4))
                    ibus_A.append(self.supply.getCurrent(channel=4))
                    efficiency.append(((vbat_V[-1]*ibat_A[-1])/(vbus_V[-1]*ibus_A[-1]))*100)
                    # sleep(0.01)
                    ibat_set = ibat_set + 0.1
                    self.supply.setCurrent(channel=1,current=ibat_set)
                self.supply.setCurrent(channel=1,current=0)
                self.dut.block_apis.SIMULINK_MODEL.set_standby_en(1)
                writeInExcel(sheet=sheet,filename='effieciency\effiecincy1.xlsx',vbat_V=vbat_V,ibat_A=ibat_A,vbus_V=vbus_V,ibus_A=ibus_A,efficiency=efficiency)
        except KeyboardInterrupt:
            pass

    def phase_Effieciency_1(self,phase=0,phase_thld=0,vbus=5.0,No_phase=1,loop_current_limit=-3.005,sheet='ph1_vbat_4V_vbus_5V',):
        print(sheet)
        # self.supply.outp_OFF(channel=1)
        # self.startup.buck_ClosedLoop(vbat=4,ibat=16,icmd_ph=6,No_phase=1,ibus=3.3,phase=1)
        voltage=3.99
        self.supply.setVoltage(channel=1,voltage=voltage)
        self.supply.setVoltage(channel=4,voltage=9)
        self.startup.buck_ClosedLoop(vbat=4,ibat=16.0,No_phase=No_phase,ibus=3.3,icmd_ph=6.0,phase=phase)
        sleep(1)
        self.dut.IVM.REG_DRV_INDCS_RW.DS_DRV_SLEW.value = 1
        if vbus > 8 :
            self.dut.IVM.REG_DRV_INDCS_RW.DS_DRV_SLEW.value = 3

        self.supply.setCurrent(channel=1,current=-0.1)
        volt=9
        if vbus >= 9 :
            self.supply.setVoltage(channel=4,voltage=volt)
            while volt < vbus:
                volt=volt+0.1
                self.supply.setVoltage(channel=4,voltage=volt)
                sleep(0.01)
            self.supply.setVoltage(channel=4,voltage=vbus)
        self.dut.SIMULINK_MODEL.TEST_INNER_LOOP_PH_MGMT.TEST_PHASE_ADD_THLD.value = phase_thld
        # input('Check Temperature >>>>>>>>>>>>>>')
        # while True:
        #     sleep(0.1)
        #     print(int(self.dut.IVM_TEMPMON.TEMP_STS.TEMP_STS.value))
        sleep(1)
        ibat_set = 0
        # self.Bat.setCurrent(current=-0.1)
        # self.Bat.outp_ON()
        self.supply.outp_ON(channel=1)
        sleep(0.1)
        vbat_V = []
        vbus_V = []
        ibus_A = []
        ibat_A = []
        efficiency = []
        temp=[]
        try :
            # if self.Bat.getCurrent() < -0.01:
            if self.supply.getCurrent(channel=1) < -0.01:
                # while self.Bat.getCurrent() > loop_current_limit:
                while self.supply.getCurrent(channel=1) >= loop_current_limit:

                    while (sum([abs(self.supply.getCurrent(channel=1))  for _ in range(0,4)])/4) <= ibat_set: 
                        sleep(0.005)
                        voltage = voltage - 0.0001
                    # self.Bat.setCurrent(current=-ibat_set)
                        self.supply.setVoltage(channel=1,voltage=voltage)
                    vbat_V.append(self.multimeter.meas_V())
                    ibat_A.append(abs(self.supply.getCurrent(channel=1)))
                    # vbus_V.append(self.voltmeter.meas_V())
                    vbus_V.append(self.supply.getVoltage(channel=4))
                    ibus_A.append(self.supply.getCurrent(channel=4))
                    efficiency.append(((vbat_V[-1]*ibat_A[-1])/(vbus_V[-1]*ibus_A[-1]))*100)
                    ibat_set = ibat_set+0.05
                    # if abs(self.supply.getCurrent(channel=1)) >= 6.0:
                    #     input('>>>>>>>')
                    sleep(0.01)

                writeInExcel(sheet=sheet,filename='effieciency\effiecincy_cap_deci2.xlsx',vbat_V=vbat_V,ibat_A=ibat_A,vbus_V=vbus_V,ibus_A=ibus_A,efficiency=efficiency)
                while voltage <= 3.98:
                    voltage = voltage + 0.001
                    self.supply.setVoltage(channel=1,voltage=voltage)
                    sleep(0.01)
                # self.supply.setCurrent(channel=1,current=0)
                self.supply.setVoltage(channel=4,voltage=vbus)
                self.supply.setVoltage(channel=1,voltage=4)
                self.supply.setVoltage(channel=1,voltage=4)
                self.dut.block_apis.SIMULINK_MODEL.set_standby_en(1)
        except KeyboardInterrupt:
            while voltage <= 3.98:
                voltage = voltage + 0.001
                self.supply.setVoltage(channel=1,voltage=voltage)
                sleep(0.01)

            self.supply.setVoltage(channel=1,voltage=4)
    
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
        # self.writeExcel = writeInExcel()
        # sleep(0.1)
        # self.phase_Effieciency(phase=0,sheet='ph1_vbat_4V_vbus_5V')
        # sleep(0.1)
        # self.phase_Effieciency(phase=1,sheet='ph2_vbat_4V_vbus_5V')
        # sleep(0.1)
        # self.phase_Effieciency(phase=2,sheet='ph3_vbat_4V_vbus_5V')
        # sleep(0.1)
        # self.phase_Effieciency(phase=3,sheet='ph4_vbat_4V_vbus_5V')
        # sleep(0.1)
        # self.phase_Effieciency_1(phase=0,phase_thld=2,No_phase=1,vbus=9.0,loop_current_limit=-3.005,sheet='device2_ph1_vbat4V_vbus9V_25C')
        # sleep(0.1)
        # self.phase_Effieciency_1(phase=1,phase_thld=2,No_phase=1,vbus=9.0,loop_current_limit=-3.005,sheet='device2_ph2_vbat4V_vbus9V_25C')
        # sleep(0.1)
        self.phase_Effieciency_1(phase=2,phase_thld=2,No_phase=2,vbus=9.0,loop_current_limit=-6.005,sheet='device2_ph34_vbat4V_vbus9V_25C')
        sleep(0.1)
        # self.phase_Effieciency_1(phase=3,phase_thld=2,No_phase=1,vbus=9.0,loop_current_limit=-3.005,sheet='device2_ph4_vbat_4V_vbus9V_25C')
        # sleep(0.1)
        # self.phase_Effieciency_1(phase=0,phase_thld=2,No_phase=1,vbus=15.0,loop_current_limit=-3.005,sheet='ph1_vbat_4V_vbus_15V')
        # sleep(0.1)
        # self.phase_Effieciency_1(phase=1,phase_thld=2,No_phase=1,vbus=15.0,loop_current_limit=-3.005,sheet='ph2_vbat_4V_vbus_15V')
        # sleep(0.1)
        # self.phase_Effieciency_1(phase=2,phase_thld=2,No_phase=1,vbus=15.0,loop_current_limit=-3.005,sheet='ph3_vbat_4V_vbus_15V')
        # sleep(0.1)
        # self.phase_Effieciency_1(phase=3,phase_thld=2,No_phase=1,vbus=15.0,loop_current_limit=-3.005,sheet='ph4_vbat_4V_vbus_15V')
        # sleep(0.1)
       

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
        input('Check Temperature >>>>>>>>>>>>>>')
        sleep(1)
        ibat_set = 0
        # self.dut.SIMULINK_MODEL.TEST_INNER_LOOP_PH_MGMT.TEST_PHASE_ADD_THLD.value = phase_thld
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
                while self.supply.getCurrent(channel=1) > loop_current_limit:
                # while self.supply.getCurrent(channel=1) > -3.001:
                    # vbat_V.append(self.supply.getVoltage(channel=1))
                    # vbat_V.append(self.voltmeter.meas_V())
                    vbat_V.append(self.supply.getVoltage(channel=1))
                    # ibat_A.append(abs(self.Bat.getCurrent()))
                    ibat_A.append(abs(self.supply.getCurrent(channel=1)))
                    vbus_V.append(self.supply.getVoltage(channel=4))
                    ibus_A.append(self.supply.getCurrent(channel=4))
                    efficiency.append(((vbat_V[-1]*ibat_A[-1])/(vbus_V[-1]*ibus_A[-1]))*100)
                    ibat_set = ibat_set + 0.1
                    # self.Bat.setCurrent(current=-ibat_set)
                    self.supply.setCurrent(channel=1,current=-ibat_set)
                    sleep(0.02)
                # self.Bat.setCurrent(current=loop_current_limit/2)
                # sleep(0.5)
                # self.Bat.setCurrent(current=loop_current_limit/4)
                # sleep(0.5)
                # self.Bat.setCurrent(current=loop_current_limit/8)
                # sleep(0.5)
                # self.Bat.setCurrent(current=0)
                # input('>>>>>>>>>>>>>>>>>>>')
                writeInExcel(sheet=sheet,filename='effieciency\effiecincy_5.xlsx',vbat_V=vbat_V,ibat_A=ibat_A,vbus_V=vbus_V,ibus_A=ibus_A,efficiency=efficiency)
                while ibat_set >= 0:
                    ibat_set = ibat_set - 0.1
                    self.supply.setCurrent(channel=1,current=-ibat_set)
                    sleep(0.01)
                    # self.supply.setVoltage(channel=4,voltage=volt)

                # self.supply.setCurrent(channel=3,current=loop_current_limit/2)
                # sleep(0.5)
                # self.supply.setCurrent(channel=3,current=loop_current_limit/4)
                # sleep(0.5)
                # self.supply.setCurrent(channel=3,current=loop_current_limit/8)
                # sleep(0.5)
                self.supply.setCurrent(channel=1,current=0)
                self.supply.setVoltage(channel=4,voltage=vbus)
                self.dut.block_apis.SIMULINK_MODEL.set_standby_en(1)
        except KeyboardInterrupt:
            self.supply.setCurrent(channel=3,current=-0.1)
            while ibat_set >= 0:
                ibat_set = ibat_set - 0.1
                self.supply.setCurrent(channel=1,current=-ibat_set)
                sleep(0.01)
            self.supply.setCurrent(channel=1,current=0)

        
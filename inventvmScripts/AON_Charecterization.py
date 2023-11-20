from time import sleep
from Instruments_API import Instruments 
from startup import Startup
from VBUS_OVP_Trim import vbus_Ovp_Trim
class AONChar:

    def __init__(self,dut) -> None:
        self.dut = dut
        self.startup = Startup(dut=dut)
        self.instruments = Instruments()
        self.scope = Instruments().scope
        self.supply = Instruments().supply
        self.voltmeter = Instruments().voltmeter
        self.supply.setVoltage(channel=1,voltage=4) # vbat 
        self.supply.setVoltage(channel=4,voltage=5) # Vbus 
        self.supply.outp_ON(channel=1)
        self.supply.outp_ON(channel=4)
        # self.startup.buck_PowerUp()
        # vbus_ovp = vbus_Ovp_Trim(dut=self.dut,Instruments=self.instruments)
        # vbus_ovp. vbus_Ovp_Test__SetUp()
        # print(vbus_ovp. vbus_Ovp_results())

        self.supply.setVoltage(channel=1,voltage=4) # vbat 
        self.supply.setVoltage(channel=4,voltage=5) # Vbus 
        self.supply.outp_ON(channel=1)
        self.supply.outp_ON(channel=4)
        # self.startup.buck_PowerUp()
        # sleep(0.1)
        self.dut.IVM.REG_PWRUP2_RW.TEMP_ENABLE.value = 1
        input('80C>>>>>>>>>>>>>')
        # while True:
        #     temp = int(self.dut.IVM_TEMPMON.TEMP_STS.TEMP_STS.value) 
        #     print(f'Temperature {temp}')
        #     if temp >= 75:
        #         input('80C>>>>>>>>>>>>>')
        #         break 
        self.hvldo_por()
        # self.vdd_sns_uvlo()
        # self.vbus_uvlo()
        # self.vdd_sns_ovp() 
        # # self.vbus_ovp()
        # self.vbus_detach()
        # self.vdd_sns_por()
        # self.vbus_por()
        # self.vdd_io_por()
    
    def vdd_sns_uvlo(self):
        self.startup.buck_PowerUp()
        self.dut.IVM.REG_VIS_MUX_RW.TST1_SEL.value = 2
        self.scope.set_HScale(scale='800E-9')
        self.scope.set_Channel__VScale(scale=0.2)
        self.scope.set_trigger__level(level=0.2)
        self.scope.set_trigger__mode(mode='NORM')
        self.scope.init_scopePosEdge__Trigger()
        sleep(0.1)
        self.scope.scopeTrigger_Acquire()
        volt=4
        sleep(0.1)
        while(self.scope.scopeAcquire_BUSY):
            sleep(0.01)
            self.supply.setVoltage(channel=1,voltage=volt)
            volt=volt-0.001
            if volt < 1 :
                break
        print(f'vdd_sns_uvlo Raising Voltage {self.supply.getVoltage(channel=1)}')
        sleep(0.1)
        self.scope.init_scopeNegEdge__Trigger()
        sleep(0.1)
        self.scope.scopeTrigger_Acquire()
        sleep(0.1)
        # volt=1
        while(self.scope.scopeAcquire_BUSY):
            sleep(0.01)
            self.supply.setVoltage(channel=1,voltage=volt)
            volt=volt+0.001
            if volt > 4 :
                break
        print(f'vdd_sns_uvlo Falling Voltage {self.supply.getVoltage(channel=1)}')
        self.supply.setVoltage(channel=4,voltage=5)
        self.supply.setVoltage(channel=1,voltage=4)

    def vdd_sns_ovp(self):
        self.startup.buck_PowerUp()
        self.dut.IVM.REG_VIS_MUX_RW.TST1_SEL.value = 3
        self.scope.set_HScale(scale='800E-9')
        self.scope.set_Channel__VScale(scale=0.2)
        self.scope.set_trigger__level(level=0.1)
        self.scope.set_trigger__mode(mode='NORM')
        self.scope.init_scopePosEdge__Trigger()
        sleep(0.1)
        self.scope.scopeTrigger_Acquire()
        volt=4
        sleep(0.1)
        while(self.scope.scopeAcquire_BUSY):
            sleep(0.01)
            self.supply.setVoltage(channel=1,voltage=volt)
            volt=volt+0.001
            if volt > 4.8 :
                break
        print(f'vdd_sns_OVP Raising Voltage {self.supply.getVoltage(channel=1)}')
        sleep(0.1)
        self.scope.init_scopeNegEdge__Trigger()
        sleep(0.1)
        self.scope.scopeTrigger_Acquire()
        sleep(0.1)
        volt=4.8
        while(self.scope.scopeAcquire_BUSY):
            sleep(0.01)
            self.supply.setVoltage(channel=1,voltage=volt)
            volt=volt- 0.001
            if volt < 4 :
                break
        print(f'vdd_sns_OVP Falling Voltage {self.supply.getVoltage(channel=1)}')
        self.supply.setVoltage(channel=4,voltage=5)
        self.supply.setVoltage(channel=1,voltage=4)

    def vbus_ovp(self):
        self.startup.buck_PowerUp()
        self.dut.IVM.REG_VIS_MUX_RW.TST1_SEL.value = 6
        self.scope.set_HScale(scale='800E-9')
        self.scope.set_Channel__VScale(scale=0.2)
        self.scope.set_trigger__level(level=0.1)
        self.scope.set_trigger__mode(mode='NORM')
        self.scope.init_scopePosEdge__Trigger()
        sleep(0.1)
        self.scope.scopeTrigger_Acquire()
        volt=21
        sleep(0.1)
        while(self.scope.scopeAcquire_BUSY):
            sleep(0.01)
            self.supply.setVoltage(channel=4,voltage=volt)
            volt=volt+0.001
            if volt > 23 :
                break
        print(f'vbus_OVP Raising Voltage {self.supply.getVoltage(channel=4)}')
        sleep(0.1)
        self.scope.init_scopeNegEdge__Trigger()
        sleep(0.1)
        self.scope.scopeTrigger_Acquire()
        sleep(0.1)
        volt=22.5
        while(self.scope.scopeAcquire_BUSY):
            sleep(0.01)
            self.supply.setVoltage(channel=4,voltage=volt)
            volt=volt- 0.001
            if volt < 20 :
                break
        print(f'vbus_OVP Falling Voltage {self.supply.getVoltage(channel=4)}')
        self.supply.setVoltage(channel=4,voltage=5)
        self.supply.setVoltage(channel=1,voltage=4)

    def hvldo_por(self):
        # self.startup.buck_PowerUp()
        self.dut.IVM.REG_PWRUP0_RW.DS_HVLDO_EN.value = 1
        self.dut.IVM.REG_VIS_MUX_RW.TST1_BLOCK_SEL.value = 1
        self.dut.IVM.REG_VIS_MUX_RW.TST1_SEL.value = 4
        input('>>>>>>>>>>>>')
        self.scope.set_HScale(scale='800E-9')
        self.scope.set_Channel__VScale(scale=0.02)
        self.scope.set_trigger__level(level=0.01)
        self.scope.set_trigger__mode(mode='NORM')
        self.scope.init_scopeNegEdge__Trigger()
        sleep(0.1)
        self.scope.scopeTrigger_Acquire()
        volt=2.3
        sleep(0.1)
        while(self.scope.scopeAcquire_BUSY):
            sleep(0.01)
            hvldo_por = self.voltmeter.meas_V()
            self.supply.setVoltage(channel=1,voltage=volt)
            volt=volt-0.001
            if volt < 0.9 :
                break
        print(f'HV ldo por voltage {hvldo_por}')
        self.supply.setVoltage(channel=1,voltage=4)

    def vbus_uvlo(self):
        self.startup.buck_PowerUp()
        self.dut.IVM.REG_VIS_MUX_RW.TST1_SEL.value = 5
        self.scope.set_HScale(scale='800E-9')
        self.scope.set_Channel__VScale(scale=0.2)
        self.scope.set_trigger__level(level=0.1)
        self.scope.set_trigger__mode(mode='NORM')
        self.scope.init_scopePosEdge__Trigger()
        sleep(0.1)
        self.scope.scopeTrigger_Acquire()
        volt=5
        sleep(0.1)
        while(self.scope.scopeAcquire_BUSY):
            sleep(0.01)
            self.supply.setVoltage(channel=4,voltage=volt)
            volt=volt-0.001
            if volt < 1 :
                break
        print(f'vbus_uvlo Raising Voltage {self.supply.getVoltage(channel=4)}')
        sleep(0.1)
        self.scope.init_scopeNegEdge__Trigger()
        sleep(0.1)
        self.scope.scopeTrigger_Acquire()
        sleep(0.1)
        # volt=1
        while(self.scope.scopeAcquire_BUSY):
            sleep(0.01)
            self.supply.setVoltage(channel=4,voltage=volt)
            volt=volt+0.001
            if volt > 4 :
                break
        print(f'vbus_uvlo Falling Voltage {self.supply.getVoltage(channel=4)}')
        self.supply.setVoltage(channel=4,voltage=5)
        self.supply.setVoltage(channel=1,voltage=4)

    def vbus_detach(self):
        self.startup.buck_PowerUp()
        self.dut.IVM.REG_VIS_MUX_RW.TST1_SEL.value = 7
        self.scope.set_HScale(scale='800E-9')
        self.scope.set_Channel__VScale(scale=0.2)
        self.scope.set_trigger__level(level=0.1)
        self.scope.set_trigger__mode(mode='NORM')
        self.scope.init_scopePosEdge__Trigger()
        sleep(0.1)
        self.scope.scopeTrigger_Acquire()
        volt=5
        sleep(0.1)
        while(self.scope.scopeAcquire_BUSY):
            sleep(0.01)
            self.supply.setVoltage(channel=4,voltage=volt)
            volt=volt-0.001
            if volt < 1 :
                break
        print(f'vbus detach Raising Voltage {self.supply.getVoltage(channel=4)}')
        sleep(0.1)
        self.scope.init_scopeNegEdge__Trigger()
        sleep(0.1)
        self.scope.scopeTrigger_Acquire()
        sleep(0.1)
        # volt=1
        while(self.scope.scopeAcquire_BUSY):
            sleep(0.01)
            self.supply.setVoltage(channel=4,voltage=volt)
            volt=volt+0.001
            if volt > 4 :
                break
        print(f'vbus detach Falling Voltage {self.supply.getVoltage(channel=4)}')
        self.supply.setVoltage(channel=4,voltage=5)
        self.supply.setVoltage(channel=1,voltage=4)

    def vbus_por(self):
        self.supply.setVoltage(channel=1,voltage=0)
        self.supply.setVoltage(channel=4,voltage=1)
        self.scope.set_HScale(scale='800E-9')
        self.scope.set_Channel__VScale(scale=0.2)
        self.scope.set_trigger__level(level=0.9)
        self.scope.set_trigger__level(level=0.1)
        self.scope.set_trigger__mode(mode='NORM')
        self.scope.init_scopePosEdge__Trigger(channel='CH4')
        sleep(0.1)
        self.scope.scopeTrigger_Acquire(channel='CH4')
        sleep(0.1)
        volt=1
        while(self.scope.scopeAcquire_BUSY):
            sleep(0.01)
            self.supply.setVoltage(channel=4,voltage=volt)
            volt=volt+0.001
            if volt > 4 :
                break
        print(f'vbus_por  Voltage {self.supply.getVoltage(channel=4)}')
        self.supply.setVoltage(channel=4,voltage=5)
        self.supply.setVoltage(channel=1,voltage=4)

    def vdd_sns_por(self):
        self.supply.setVoltage(channel=1,voltage=1)
        self.supply.setVoltage(channel=4,voltage=0)
        self.scope.set_HScale(scale='800E-9')
        self.scope.set_Channel__VScale(scale=0.2)
        self.scope.set_trigger__level(level=0.9)
        self.scope.set_trigger__mode(mode='NORM')
        self.scope.init_scopePosEdge__Trigger(channel='CH4')
        sleep(0.1)
        self.scope.scopeTrigger_Acquire(channel='CH4')
        sleep(0.1)
        volt=1
        while(self.scope.scopeAcquire_BUSY):
            sleep(0.01)
            self.supply.setVoltage(channel=1,voltage=volt)
            volt=volt+0.001
            if volt > 4 :
                break
        print(f'vdd_sns_por  Voltage {self.supply.getVoltage(channel=1)}')
        self.supply.setVoltage(channel=4,voltage=5)
        self.supply.setVoltage(channel=1,voltage=4)

    def vdd_io_por(self):
        self.supply.setVoltage(channel=4,voltage=5)
        self.startup.buck_PowerUp()
        input('VDDIO POR detach the J15 and connect the channel 1 >>>>>>>>>>>>>>>>>>>>>>>>>>')
        self.supply.setVoltage(channel=1,voltage=1)
        self.scope.set_HScale(scale='800E-9')
        self.scope.set_Channel__VScale(scale=0.2)
        self.scope.set_trigger__level(level=0.9)
        self.scope.set_trigger__mode(mode='NORM')
        self.scope.init_scopePosEdge__Trigger(channel='CH4')
        sleep(0.1)
        self.scope.scopeTrigger_Acquire(channel='CH4')
        sleep(0.1)
        volt=1
        while(self.scope.scopeAcquire_BUSY):
            sleep(0.01)
            self.supply.setVoltage(channel=3,voltage=volt)
            volt=volt+0.001
            if volt > 4 :
                break
        input(f'vdd_io_por  Voltage {self.supply.getVoltage(channel=3)}')
        self.supply.setVoltage(channel=4,voltage=5)
        self.supply.setVoltage(channel=1,voltage=4)

  
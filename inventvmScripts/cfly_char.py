
from time import sleep
from Instruments_API import Instruments
from writeExcel import writeInExcel
import pyvisa as visa 
from cfly_charging_discharging import Cfly_chg_dshg
from startup import Startup
from MatrixAPI.MatrixSignal import Matrix 

class CflyChar:

    def __init__(self,dut) -> None:
        self.dut=dut
        self.startup = Startup(dut=dut)
        self.cfly_chg = Cfly_chg_dshg(dut=dut)
        self.startup = Startup(dut=dut)
        self.supply = Instruments().supply
        # self.scope = Instruments().scope
        self.multimeter = Instruments().multimeter
        self.voltmeter = Instruments().voltmeter
        self.matrix = Matrix()

        sleep(1)

        self.cfly_sweep(sheet='device3_cflysns_0C')

    def cfly_sweep(self,filename='cfly_sense_measure/cfly_sense_0C.xlsx',sheet='device1_cflysns_0C'):
        phases = {0:'PH1S1',1:'PH2S1',2:'PH3S1',3:'PH4S1'}
        cfly_SNS=[[],[],[],[] ]
        cfly_force=[[],[],[],[] ]
        error=[[],[],[],[] ]
        self.startup.buck_PowerUp()
        input('>>>>>>>>>')
        sleep(0.1)
        try:
            for phaseIndex, phase in phases.items():
                vbus=2.5
                self.supply.setVoltage(channel=4,voltage=vbus)
                
                self.phase_select(phase=phase,chg=True)
                print(f'{phase:~^40}')
                # if phase == 'PH3S1':
                #      input('>>>>>')
                sleep(0.1)
                while vbus <= 15.1:
                    self.supply.setVoltage(channel=4,voltage=vbus)
                    sleep(0.03)
                    vbus+=0.1
                    cfly_force[phaseIndex].append(self.supply.getVoltage(channel=4)) 
                    cfly_SNS[phaseIndex].append(self.multimeter.meas_V()) 
                    error[phaseIndex].append((((cfly_force[phaseIndex][-1]/10)-cfly_SNS[phaseIndex][-1])/(cfly_force[phaseIndex][-1]/10))*100) 
                self.supply.setVoltage(channel=4,voltage=2.5)
                self.phase_select(chg=False)
            
            writeInExcel(sheet=sheet,filename=filename,\
                         ph1_cfly_force=cfly_force[0],ph1_cfly_meas=cfly_SNS[0],ph1_cfly_error=error[0],\
                         ph2_cfly_force=cfly_force[1],ph2_cfly_meas=cfly_SNS[1],ph2_cfly_error=error[1],\
                         ph3_cfly_force=cfly_force[2],ph3_cfly_meas=cfly_SNS[2],ph3_cfly_error=error[2],\
                         ph4_cfly_force=cfly_force[3],ph4_cfly_meas=cfly_SNS[3],ph4_cfly_error=error[3],\
                            )
        except KeyboardInterrupt:
                self.supply.setVoltage(channel=4,voltage=2.5)
                self.phase_select(chg=False)
        finally:
                self.supply.setVoltage(channel=4,voltage=2.5)

           
    
    def phase_select(self,phase='PH1S1',chg=False):
        self.matrix.force_Matrix__Switchx(phase)
        if chg:
            if phase=='PH1S1':
                print(f'{phase}')
                self.cfly_chg.ph1_cfly_charge()
            if phase=='PH2S1':
                self.cfly_chg.ph2_cfly_charge()
            if phase=='PH3S1':
                self.cfly_chg.ph3_cfly_charge()
            if phase=='PH4S1':
                self.cfly_chg.ph4_cfly_charge()
        else:
            self.cfly_chg.ph1_cfly_discharge( )
            self.cfly_chg.ph2_cfly_discharge( )
            self.cfly_chg.ph3_cfly_discharge( )
            self.cfly_chg.ph4_cfly_discharge( )
            self.matrix.reset()

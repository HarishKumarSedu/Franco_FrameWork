import time

import pyvisa as visa
from pyvisa.attributes import *
from pyvisa.constants import *

class dpo_2014B:

    def __init__(self, usb_id):
        rm = visa.ResourceManager()
        # rm.list_resources()
        self.scope = rm.open_resource(usb_id)
        self.scope.read_termination = '\n'
        self.scope.write_termination = '\n'

        # self.reset()

    def get_IDN(self):
        return (self.scope.query('*IDN?'))

    def reset(self):
        self.scope.write('*RST')     

    def get_error(self):
        return self.scope.query('SYST:ERR?')  
    
    def meas_Freq(self,Meas='MEAS1'):
        self.scope.write(f'MEASUrement:{Meas}:TYPE FREQUENCY')
        return float(self.scope.query('MEASUrement:MEAS1:VALUE?'))
    
    def set_trigger__mode(self,mode='AUTO'):
        # TRIGger:MAIn:MODe { AUTO | NORMal }
        self.scope.write(f'TRIGger:MAIn:MODe {mode}')

    def init_scopePosEdge__Trigger(self):
        self.scope.write(':TRIG:A:TYP EDG')
        self.scope.write(':TRIG:A:EDGE:SOU CH1')
        self.scope.write(':TRIG:A:EDGE:SLO RIS')
        self.scope.write('ACTONEV:EVENTTYP TRIG')
        self.scope.write(':ACTONEV:NUMACQ 1')
        self.scope.write(':ACTONEV:REPEATC 1')
        
    def init_scopeNegEdge__Trigger(self):
        self.scope.write(':TRIG:A:TYP EDG')
        self.scope.write(':TRIG:A:EDGE:SOU CH1')
        self.scope.write(':TRIG:A:EDGE:SLO FALL')
        self.scope.write('ACTONEV:EVENTTYP TRIG')
        self.scope.write(':ACTONEV:NUMACQ 1')
        self.scope.write(':ACTONEV:REPEATC 1')

    def single_Trigger__ON(self):
        self.scope.write('ACQuire:STATE ON')
    def single_Trigger__RUN(self):
        self.scope.write('ACQuire:STATE RUN')
    def set_Channel__VScale(self,channel=1,scale=0.05):
        self.scope.write(f'CH{str(channel)}:SCAle {str(scale)}')
    def get_Channel__VScale(self,channel=1):
        return float(self.scope.query(f'CH{str(channel)}:SCAle?'))
    def set_HScale(self,scale='400E-9'):
        self.scope.write(f'HORizontal:MAIn:SCAle {scale}')
    def get_HScale(self):
        return float(self.scope.query(f'HORizontal:MAIn:SCAle'))
    
    def set_autoSet(self):
        self.scope.write('AUTOSet EXECute')

    @property
    def acquireState(self):
        if float(self.scope.query('ACQuire:STATE?')) == 1.0:
            State = True 
        else :
            State = False 

        return State
    
    def get_trigger__level(self):
        return float(self.scope.query('TRIGger:MAIn:LEVel?')) 
    
    def get_trigger__level(self,level):
        self.scope.write(f'TRIGger:MAIn:LEVel {str(level)}')
        
if __name__ == '__main__':
    scope = dpo_2014B('USB0::0x0699::0x0456::C010843::INSTR')
    print(scope.meas_Freq())
    # print(scope.get_error())
    scope.set_trigger__mode(mode='NORM')
    time.sleep(1)
    scope.init_scopePosEdge__Trigger()
    time.sleep(1)
    scope.single_Trigger__ON()
    time.sleep(1)
    print('State',scope.acquireState)
    while scope.acquireState == True :
       print('rotate')
    # time.sleep(1)
    # scope.set_trigger__mode()
    # scope.single_Trigger__RUN()


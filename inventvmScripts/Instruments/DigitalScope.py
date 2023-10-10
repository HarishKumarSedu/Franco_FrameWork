import time

import pyvisa as visa
from pyvisa.attributes import *
from pyvisa.constants import *

class dpo_2014B:

    def __init__(self, usb_id):
        rm = visa.ResourceManager()
        # rm.list_resources()
        self.my_instr = rm.open_resource(usb_id)
        self.my_instr.read_termination = '\n'
        self.my_instr.write_termination = '\n'

        # self.reset()

    def get_IDN(self):
        return (self.my_instr.query('*IDN?'))

    def reset(self):
        self.my_instr.write('*RST')     

    def get_error(self):
        return self.my_instr.query('SYST:ERR?')  
    
    def meas_Freq(self,Meas='MEAS1'):
        self.my_instr.write(f'MEASUrement:{Meas}:TYPE FREQUENCY')
        return float(self.my_instr.query('MEASUrement:MEAS1:VALUE?'))

if __name__ == '__main__':
    scope = dpo_2014B('USB0::0x0699::0x0456::C010843::INSTR')
    print(scope.meas_Freq())
    # print(scope.get_error())
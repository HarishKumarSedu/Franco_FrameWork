import re
from time import sleep
import sys
 
# adding Folder_2/subfolder to the system path
sys.path.insert(0, 'C:/Users/Smplab/Documents/Franco/Inventvm/SW/inventvmScripts/MatrixAPI')
from relayMatrix import RelayMatrix1

class Matrix:

    def __init__(self) -> None:
        self.relayMatrix1 = RelayMatrix1(slaveAddress=0x20)
        
        # self.relayMatrix2 = RelayMatrix2(slaveAddress=0x21)
        # self.relayMatrix3 = RelayMatrix3(slaveAddress=0x22)
        self.reset()
    def reset(self):
        self.relayMatrix1.reset()
        
    # Force Signal Matrix Switch Turn on  
    def force_Matrix__Switchx(self,TrimFieldName):
        if re.search('LDO1.2 Trimming',TrimFieldName):
           self.reset()
           sleep(0.1)
           self.relayMatrix1.VDD_D(True)
           sleep(0.01)
           self.relayMatrix1.GND(True)
        if re.search('Aon BG vref 1.2V',TrimFieldName):
           self.reset()
           sleep(0.1)
           self.relayMatrix1.VDDA(True)
           sleep(0.01)
           self.relayMatrix1.GND(True)
        if re.search('Main BG Current Trimming',TrimFieldName):
           self.reset()
           sleep(0.1)
           self.relayMatrix1.GND(True)
        if re.search('PH13 IND CS Buffer',TrimFieldName):
           self.reset()
           sleep(0.1)
           self.relayMatrix1.ph13_indcs_buff_1(True)
           self.relayMatrix1.GND(True)
           sleep(0.2)
        if re.search('PH24 IND CS Buffer',TrimFieldName):
           self.reset()
           sleep(0.1)
           self.relayMatrix1.ph24_indcs_buff_1(True)
           self.relayMatrix1.GND(True)
           sleep(0.2)
        if re.search('PH1S1 IND CS Mirror trimming',TrimFieldName):
           self.reset()
           sleep(0.1)
           self.relayMatrix1.ph13_indcs_buff_2(True)
           self.relayMatrix1.ph1_IL_Out(True)
           sleep(0.2)
        if re.search('PH1S4 IND CS Mirror trimming',TrimFieldName):
           self.reset()
           sleep(0.1)
           self.relayMatrix1.ph13_indcs_buff_2(True)
           self.relayMatrix1.ph1_IL_Out(True)
           sleep(0.2)
        if re.search('PH1S1 IND CS Offset trimming',TrimFieldName):
           self.reset()
           sleep(0.1)
           self.relayMatrix1.ph13_indcs_buff_2(True)
           self.relayMatrix1.ph1_IL_Out(True)
           sleep(0.2)
        if re.search('PH1S4 IND CS Offset trimming',TrimFieldName):
           self.reset()
           sleep(0.1)
           self.relayMatrix1.ph13_indcs_buff_2(True)
           self.relayMatrix1.ph1_IL_Out(True)
           sleep(0.2)
        if re.search('PH1S1 IND CS Gain trimming',TrimFieldName):
           self.reset()
           sleep(0.1)
           self.relayMatrix1.ph13_indcs_buff_2(True)
           self.relayMatrix1.ph1_IL_Out(True)
           sleep(0.2)
        if re.search('PH1S4 IND CS Gain trimming',TrimFieldName):
           self.reset()
           sleep(0.1)
           self.relayMatrix1.ph13_indcs_buff_2(True)
           self.relayMatrix1.ph1_IL_Out(True)
           sleep(0.2)

if __name__=='__main__':
    Matrix()
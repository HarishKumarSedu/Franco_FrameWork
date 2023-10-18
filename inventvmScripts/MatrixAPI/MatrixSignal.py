import re
from time import sleep
import sys
 
# adding Folder_2/subfolder to the system path
sys.path.insert(0, 'C:/Users/Smplab/Documents/Franco/Inventvm/SW/inventvmScripts/MatrixAPI')
from relayMatrix import RelayMatrix1,RelayMatrix2
from PyMCP2221A import PyMCP2221A

class Matrix:

    def __init__(self) -> None:
        self.mcp2221A = PyMCP2221A.PyMCP2221A()
      #   self.mcp2221A.Reset()
        self.mcp2221A = PyMCP2221A.PyMCP2221A()
        self.mcp2221A.I2C_Init()

        self.relayMatrix1 = RelayMatrix1(slaveAddress=0x20,mcp=self.mcp2221A)
        self.relayMatrix2 = RelayMatrix2(slaveAddress=0x22,mcp=self.mcp2221A)
      #   # self.reset()
         
    def reset(self):
        self.relayMatrix1.reset()
        self.relayMatrix2.reset()
      #   self.mcp2221A.Reset()
        
    # Force Signal Matrix Switch Turn on  
    def force_Matrix__Switchx(self,TrimFieldName):
        if re.search('LDO1.2 Trimming',TrimFieldName):
           # self.reset()
           sleep(0.1)
           self.relayMatrix1.VDD_D(True)
           sleep(0.01)
           self.relayMatrix1.GND(True)
        if re.search('Aon BG vref 1.2V',TrimFieldName):
           # self.reset()
           sleep(0.1)
           self.relayMatrix1.VDDA(True)
           sleep(0.01)
           self.relayMatrix1.GND(True)
        if re.search('Main BG Current Trimming',TrimFieldName):
           # self.reset()
           sleep(0.1)
           self.relayMatrix1.GND(True)
        if re.search('PH13 IND CS Buffer',TrimFieldName):
           # self.reset()
           sleep(0.1)
           self.relayMatrix1.ph13_indcs_buff_1(True)
           self.relayMatrix1.GND(True)
           sleep(0.2)
        if re.search('PH24 IND CS Buffer',TrimFieldName):
           # self.reset()
           sleep(0.1)
           self.relayMatrix1.ph24_indcs_buff_1(True)
           self.relayMatrix1.GND(True)
           sleep(0.2)
        if re.search('PH1S1 IND CS',TrimFieldName):
           # self.reset()
           sleep(0.1)
           self.relayMatrix1.ph13_indcs_buff_2(True)
           self.relayMatrix1.ph1_IL_Out(True)
           sleep(0.2)
        if re.search('PH1S4 IND CS',TrimFieldName):
           # self.reset()
           sleep(0.1)
           self.relayMatrix1.ph13_indcs_buff_2(True)
           self.relayMatrix1.ph1_IL_Out(True)
           sleep(0.2)
        if re.search('PH2S1 IND CS',TrimFieldName):
           # self.reset()
           sleep(0.1)
           self.relayMatrix1.ph24_indcs_buff_2(True)
           self.relayMatrix2.ph2_IL_Out(True)
           sleep(0.2)
        if re.search('PH2S4 IND CS',TrimFieldName):
           # self.reset()
           sleep(0.1)
           self.relayMatrix1.ph24_indcs_buff_2(True)
           self.relayMatrix2.ph2_IL_Out(True)
           sleep(0.2)
        if re.search('PH2S1 IND CS',TrimFieldName):
           # self.reset()
           sleep(0.1)
           self.relayMatrix1.ph24_indcs_buff_2(True)
           self.relayMatrix2.ph2_IL_Out(True)
           sleep(0.2)
        if re.search('PH2S4 IND CS',TrimFieldName):
           # self.reset()
           sleep(0.1)
           self.relayMatrix1.ph24_indcs_buff_2(True)
           self.relayMatrix2.ph2_IL_Out(True)
           sleep(0.2)
        if re.search('PH3S1 IND CS',TrimFieldName):
           # self.reset()
           sleep(0.1)
           self.relayMatrix1.ph13_indcs_buff_2(True)
           self.relayMatrix2.ph3_IL_Out(True)
           sleep(0.2)
        if re.search('PH3S4 IND CS',TrimFieldName):
           # self.reset()
           sleep(0.1)
           self.relayMatrix1.ph13_indcs_buff_2(True)
           self.relayMatrix2.ph3_IL_Out(True)
           sleep(0.2)
        if re.search('PH4S1 IND CS',TrimFieldName):
           # self.reset()
           sleep(0.1)
           self.relayMatrix1.ph24_indcs_buff_2(True)
           self.relayMatrix2.ph4_IL_Out(True)
           sleep(0.2)
        if re.search('PH4S4 IND CS',TrimFieldName):
           # self.reset()
           sleep(0.1)
           self.relayMatrix1.ph24_indcs_buff_2(True)
           self.relayMatrix2.ph4_IL_Out(True)
           sleep(0.2)

if __name__=='__main__':
    matrix = Matrix()
   #  matrix.reset()
    matrix.relayMatrix1.ph13_indcs_buff_2(True)
    matrix.relayMatrix1.ph1_IL_Out(True)
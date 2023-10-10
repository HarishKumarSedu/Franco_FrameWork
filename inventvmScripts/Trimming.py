import sys 
import os 
import pandas as pd 
import json 
import re 

# import module
from datetime import datetime
from Instruments_API import Instruments
from MatrixAPI.MatrixSignal import Matrix 
from DCO_Trim import DCO_Trim
from AON_Bg_Vref_1p2V_Trim import Aon_Bg_Vref_1p2V_Trim
from AON_Vref_0p6V_Trim import Aon_Vref_0p6V_Trim
from AON_Vref_1p2V_Trim import Aon_Vref_1p2V_Trim
from Ldo_1p2V_Trim import Ldo_1p2V_Trim
from Main_Bg_Trim import Main_Bg_Trim

class Trim(object):
    """
    This is a class called Trimming. It has an __init__ method that takes a list of DFTs as input. It sets the DFT attribute to the input and calls the trimming_Instructions__Parse method. 
    """

    def __init__(self,test_station,DFT_path:str) -> None:
        self.test_station = test_station # franco dut object 
        self.dut = self.test_station.eeb.franco
        self.instruments = Instruments()
        self.matrix = Matrix()

        with open(DFT_path) as f:
            self.DFT = json.load(f)

        self.trimming__Parse()
        
    def trimming__Parse(self):
        for trim in self.DFT:
            # if re.search('DCO',trim.get('Trimming_Name ')):
            #     dco = DCO_Trim(dut=self.dut,DFT=trim,Instruments=self.instruments)
            #     dco.dco_Test__SetUp()
            #     print(dco.dco_results())

            # if re.search('Aon BG vref 1.2V',trim.get('Trimming_Name ')):
            #     self.matrix.force_Matrix__Switchx(trim.get('Trimming_Name '))
            #     aon_Bg_Vref_1p2 = Aon_Bg_Vref_1p2V_Trim(dut=self.dut,DFT=trim,Instruments=self.instruments)
            #     aon_Bg_Vref_1p2.Aon_Bg_Vref_1p2V_Test__SetUp()
            #     print(aon_Bg_Vref_1p2.Aon_Bg_Vref_1p2V_results())
            #     pass
            if re.search('Aon vref 0.6V',trim.get('Trimming_Name ')):
                # self.matrix.force_Matrix__Switchx(trim.get('Trimming_Name '))
                aon_Vref_0p6 = Aon_Vref_0p6V_Trim(dut=self.dut,DFT=trim,Instruments=self.instruments)
                aon_Vref_0p6.Aon_Vref_0p6V_Test__SetUp()
                print(aon_Vref_0p6.Aon_Vref_0p6V_results())
                pass
            # if re.search('Aon ldo_vref_1p2 trimming',trim.get('Trimming_Name ')):
            #     aon_Vref_1p2 = Aon_Vref_1p2V_Trim(dut=self.dut,DFT=trim,Instruments=self.instruments)
            #     aon_Vref_1p2.Aon_Vref_1p2V_Test__SetUp()
            #     print(aon_Vref_1p2.Aon_Vref_1p2V_results())
            #     pass
            # if re.search('LDO1.2 Trimming',trim.get('Trimming_Name ')):
            #     self.matrix.force_Matrix__Switchx(trim.get('Trimming_Name '))
            #     ldo_1p2 = Ldo_1p2V_Trim(dut=self.dut,DFT=trim,Instruments=self.instruments)
            #     ldo_1p2.Ldo_1p2V_Test__SetUp()
            #     print(ldo_1p2.Ldo_1p2V_results())
            #     pass
            # if re.search('Main BG Current Trimming',trim.get('Trimming_Name ')):
            #     main_bg = Main_Bg_Trim(dut=self.dut,DFT=trim,Instruments=self.instruments)
            #     main_bg.Main_Bg_Test__SetUp()
            #     print(main_bg.Main_Bg_results())
                # pass
                

if __name__ == '__main__':
    try:
        trimming = Trim(test_station=None,DFT_path='data/DFTInstructions_new.json')
    except KeyboardInterrupt:
        pass
    # try :
    #     with open('data/DFTInstructions_new.json') as f:
    #         DFT = json.load(f)
    #     trimming = Trim(DFT=DFT)
    # except KeyboardInterrupt:
    #     pass

      
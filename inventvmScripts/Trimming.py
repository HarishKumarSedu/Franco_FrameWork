import sys 
import os 
import pandas as pd 
import json 
import re
from time import sleep

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
from PH13_IndCs_Buff_Trim import Ph13_IndCs_Buff_Trim
from PH24_IndCs_Buff_Trim import Ph24_IndCs_Buff_Trim
from PH1S1_Indcs_Mirror_Trim import Ph1S1_Indcs_Mirror_Trim
from PH1S1_Indcs_Offset_Trim import Ph1S1_Indcs_Offset_Trim
from PH1S1_Indcs_ZC_Trim import Ph1S1_Indcs_ZC_Trim
from PH1S1_Indcs_Gain_Trim import Ph1S1_Indcs_Gain_Trim


class Trim(object):
    """
    This is a class called Trimming. It has an __init__ method that takes a list of DFTs as input. It sets the DFT attribute to the input and calls the trimming_Instructions__Parse method. 
    """

    def __init__(self,test_station,DFT_path:str) -> None:
        self.test_station = test_station # franco dut object 
        self.dut = self.test_station.eeb.franco
        self.instruments = Instruments()
        self.matrix = Matrix()

        self.trim_results = {}
        with open(DFT_path) as f:
            self.DFT = json.load(f)

        self.trimming__Parse()
        
    def trimming__Parse(self):
        try:
            chip_index_start=int(input('Enter Chip Index Start >'))
            # chip_index_start=1
            chip_index = chip_index_start
            while(True):
                input('Insert Chip >')
                trim_result = []
                for trim in self.DFT:
                    self.instruments.supply.outp_ON(channel=1)
                    self.instruments.supply.outp_OFF(channel=3)
                    if False:
                        pass
                    elif re.search('DCO',trim.get('Trimming_Name ')):
                        print(trim.get('Trimming_Name '))
                        dco = DCO_Trim(dut=self.dut,DFT=trim,Instruments=self.instruments)
                        dco.dco_Test__SetUp()
                        result = dco.dco_results()
                        print(result)
                        trim_result.append(result)
                        
                    elif re.search('Aon BG vref 1.2V',trim.get('Trimming_Name ')):
                        print(trim.get('Trimming_Name '))
                        self.matrix.force_Matrix__Switchx(trim.get('Trimming_Name '))
                        aon_Bg_Vref_1p2 = Aon_Bg_Vref_1p2V_Trim(dut=self.dut,DFT=trim,Instruments=self.instruments)
                        aon_Bg_Vref_1p2.Aon_Bg_Vref_1p2V_Test__SetUp()
                        result=aon_Bg_Vref_1p2.Aon_Bg_Vref_1p2V_results()
                        print(result)
                        trim_result.append(result)
                        
                    elif re.search('Aon vref 0.6V',trim.get('Trimming_Name ')):
                        print(trim.get('Trimming_Name '))
                        self.matrix.reset()
                        # self.matrix.force_Matrix__Switchx(trim.get('Trimming_Name '))
                        aon_Vref_0p6 = Aon_Vref_0p6V_Trim(dut=self.dut,DFT=trim,Instruments=self.instruments)
                        aon_Vref_0p6.Aon_Vref_0p6V_Test__SetUp()
                        # input('Connect TEST1 to 1.2v and let it discharge to 0.6v >')
                        result=aon_Vref_0p6.Aon_Vref_0p6V_results()
                        print(result)
                        trim_result.append(result)
                        
                    elif re.search('Aon ldo_vref_1p2 trimming',trim.get('Trimming_Name ')):
                        print(trim.get('Trimming_Name '))
                        aon_Vref_1p2 = Aon_Vref_1p2V_Trim(dut=self.dut,DFT=trim,Instruments=self.instruments)
                        aon_Vref_1p2.Aon_Vref_1p2V_Test__SetUp()
                        result=aon_Vref_1p2.Aon_Vref_1p2V_results()
                        print(result)
                        trim_result.append(result)
                    
                    elif re.search('LDO1.2 Trimming',trim.get('Trimming_Name ')):
                        print(trim.get('Trimming_Name '))
                        self.matrix.force_Matrix__Switchx(trim.get('Trimming_Name '))
                        ldo_1p2 = Ldo_1p2V_Trim(dut=self.dut,DFT=trim,Instruments=self.instruments)
                        ldo_1p2.Ldo_1p2V_Test__SetUp()
                        result=ldo_1p2.Ldo_1p2V_results()
                        print(result)
                        trim_result.append(result)
                        
                    if re.search('Main BG Current Trimming',trim.get('Trimming_Name ')):
                        self.matrix.force_Matrix__Switchx(trim.get('Trimming_Name '))
                        input('Connect TEST1 to Current meter for Main BG Current Trimming >')
                        main_bg = Main_Bg_Trim(dut=self.dut,DFT=trim,Instruments=self.instruments)
                        main_bg.Main_Bg_Test__SetUp()
                        result=main_bg.Main_Bg_results()
                        print(result)
                        trim_result.append(result)

                    elif re.search('PH13 IND CS Buffer',trim.get('Trimming_Name ')):

                        print(trim.get('Trimming_Name '))
                        self.matrix.force_Matrix__Switchx(trim.get('Trimming_Name '))
                        ph13_indcs_buff = Ph13_IndCs_Buff_Trim(dut=self.dut,DFT=trim,Instruments=self.instruments)
                        ph13_indcs_buff.Ph13_IndCs_Buff_Test__SetUp()
                        result=ph13_indcs_buff.Ph13_IndCs_Buff_results()
                        print(result)
                        trim_result.append(result)
                        
                    elif re.search('PH24 IND CS Buffer',trim.get('Trimming_Name ')):

                        print(trim.get('Trimming_Name '))
                        self.matrix.force_Matrix__Switchx(trim.get('Trimming_Name '))
                        ph24_indcs_buff = Ph24_IndCs_Buff_Trim(dut=self.dut,DFT=trim,Instruments=self.instruments)
                        ph24_indcs_buff.Ph24_IndCs_Buff_Test__SetUp()
                        result=ph24_indcs_buff.Ph24_IndCs_Buff_results()
                        print(result)
                        trim_result.append(result)
                        
                    elif re.search('PH1S1 IND CS Mirror trimming',trim.get('Trimming_Name ')):

                        print(trim.get('Trimming_Name '))
                        self.matrix.force_Matrix__Switchx(trim.get('Trimming_Name '))
                        ph1s1_indcs_mirror = Ph1S1_Indcs_Mirror_Trim(dut=self.dut,DFT=trim,Instruments=self.instruments)
                        ph1s1_indcs_mirror.Ph1S1_Indcs_Mirror_Test__SetUp()
                        result=ph1s1_indcs_mirror.Ph1S1_Indcs_Mirror_results()
                        print(result)
                        trim_result.append(result)
                        
                    elif re.search('PH1S1 IND CS Offset trimming',trim.get('Trimming_Name ')):

                        print(trim.get('Trimming_Name '))
                        self.matrix.force_Matrix__Switchx(trim.get('Trimming_Name '))
                        ph1s1_indcs_offset = Ph1S1_Indcs_Offset_Trim(dut=self.dut,DFT=trim,Instruments=self.instruments)
                        ph1s1_indcs_offset.Ph1S1_Indcs_Offset_Test__SetUp()
                        result=ph1s1_indcs_offset.Ph1S1_Indcs_Offset_results()
                        print(result)
                        trim_result.append(result)
                        
                    elif re.search('PH1S1 IND CS Gain trimming',trim.get('Trimming_Name ')):

                        print(trim.get('Trimming_Name '))
                        self.matrix.force_Matrix__Switchx(trim.get('Trimming_Name '))
                        ph1s1_indcs_gain = Ph1S1_Indcs_Gain_Trim(dut=self.dut,DFT=trim,Instruments=self.instruments)
                        ph1s1_indcs_gain.Ph1S1_Indcs_Gain_Test__SetUp()
                        result=ph1s1_indcs_gain.Ph1S1_Indcs_Gain_results()
                        print(result)
                        trim_result.append(result)

                    elif re.search('PH1S1 ZC Comparator trimming',trim.get('Trimming_Name ')):
                        print(trim.get('Trimming_Name '))
                        self.matrix.force_Matrix__Switchx(trim.get('Trimming_Name '))
                        ph1s1_indcs_zc = Ph1S1_Indcs_ZC_Trim(dut=self.dut,DFT=trim,Instruments=self.instruments)
                        ph1s1_indcs_zc.Ph1S1_Indcs_ZC_Test__SetUp()
                        result=ph1s1_indcs_zc.Ph1S1_Indcs_ZC_results()
                        print(result)
                        trim_result.append(result)
                        
                    elif re.search('PH1S4 IND CS Mirror trimming',trim.get('Trimming_Name ')):

                        print(trim.get('Trimming_Name '))
                        self.matrix.force_Matrix__Switchx(trim.get('Trimming_Name '))
                        ph1s1_indcs_mirror = Ph1S1_Indcs_Mirror_Trim(dut=self.dut,DFT=trim,Instruments=self.instruments)
                        ph1s1_indcs_mirror.Ph1S1_Indcs_Mirror_Test__SetUp()
                        result=ph1s1_indcs_mirror.Ph1S1_Indcs_Mirror_results()
                        print(result)
                        trim_result.append(result)
                        
                    elif re.search('PH1S4 IND CS Offset trimming',trim.get('Trimming_Name ')):
                        print(trim.get('Trimming_Name '))
                        self.matrix.force_Matrix__Switchx(trim.get('Trimming_Name '))
                        ph1s1_indcs_offset = Ph1S1_Indcs_Offset_Trim(dut=self.dut,DFT=trim,Instruments=self.instruments)
                        ph1s1_indcs_offset.Ph1S1_Indcs_Offset_Test__SetUp()
                        result=ph1s1_indcs_offset.Ph1S1_Indcs_Offset_results()
                        print(result)
                        trim_result.append(result)
                        
                    elif re.search('PH1S4 IND CS Gain trimming',trim.get('Trimming_Name ')):
                        print(trim.get('Trimming_Name '))
                        self.matrix.force_Matrix__Switchx(trim.get('Trimming_Name '))
                        ph1s1_indcs_gain = Ph1S1_Indcs_Gain_Trim(dut=self.dut,DFT=trim,Instruments=self.instruments)
                        ph1s1_indcs_gain.Ph1S1_Indcs_Gain_Test__SetUp()
                        result=ph1s1_indcs_gain.Ph1S1_Indcs_Gain_results()
                        print(result)
                        trim_result.append(result)
                    elif re.search('PH1S4 ZC Comparator trimming',trim.get('Trimming_Name ')):
                        print(trim.get('Trimming_Name '))
                        self.matrix.force_Matrix__Switchx(trim.get('Trimming_Name '))
                        ph1s1_indcs_zc = Ph1S1_Indcs_ZC_Trim(dut=self.dut,DFT=trim,Instruments=self.instruments)
                        ph1s1_indcs_zc.Ph1S1_Indcs_ZC_Test__SetUp()
                        result=ph1s1_indcs_zc.Ph1S1_Indcs_ZC_results()
                        print(result)
                        trim_result.append(result)
                
                self.trim_results.update({
                        chip_index:trim_result
                    })
                chip_index=chip_index+1
        except KeyboardInterrupt :
            # self.dut.copy_trims_to_eeprom()
            self.instruments.supply.outp_OFF(channel=1)
            self.instruments.supply.outp_OFF(channel=3)
            self.matrix.reset()
            resultsfilename = f'TrimmingResults_{str(chip_index_start)}_{str(chip_index-1)}'
            with open(f'json/{resultsfilename}.json', 'w', encoding='utf-8') as f:
                json.dump(self.trim_results, f, ensure_ascii=False, indent=4)
            

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

      
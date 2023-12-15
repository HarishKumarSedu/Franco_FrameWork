import sys 
import os 
import pandas as pd 
import json 
import re
from time import sleep,time,ctime

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
from VDD_SNS_OVP_Trim import Vdd_Sns_Ovp_Trim
from PH13_IndCs_Buff_Trim import Ph13_IndCs_Buff_Trim
from PH24_IndCs_Buff_Trim import Ph24_IndCs_Buff_Trim
from PHxSy_Indcs_Mirror_Trim import PhxSy_Indcs_Mirror_Trim
from PHxSy_Indcs_Offset_Trim import PhxSy_Indcs_Offset_Trim
from PHxSy_Indcs_ZC_Trim import PhxSy_Indcs_ZC_Trim
from PHxSy_Indcs_Gain_Trim import PhxSy_Indcs_Gain_Trim
from startup import Startup
from Franco_Test__APIs import FrancoAPIS

class Trim(object):
    """
    This is a class called Trimming. It has an __init__ method that takes a list of DFTs as input. It sets the DFT attribute to the input and calls the trimming_Instructions__Parse method. 
    """

    def __init__(self,test_station,DFT_path:str,loadTrim) -> None:
        self.test_station = test_station # franco dut object 
        self.loadTrim = loadTrim
        self.dut = self.test_station.eeb.franco
        self.instruments = Instruments()
        self.matrix = Matrix()
        self.startup = Startup(dut=self.dut)
        self.apis = FrancoAPIS(dut=self.dut)
        self.trim_results = {}
        with open(DFT_path) as f:
            self.DFT = json.load(f)

        self.trimming__Parse()
        
    def trimming__Parse(self):
        try:
            chip_index_start=int(input('Enter Chip Index Start >'))
            # chip_index_start=1616
            chip_index = chip_index_start
            # self.loadTrim.loadTrims()
            while(True):
                # self.matrix.reset()
                input('Insert Chip >')
                start_time = time()
                trim_result = []
                self.instruments.supply.outp_OFF(channel=1)
                for trim in self.DFT:
                    self.matrix.reset()
                    self.instruments.supply.outp_OFF(channel=3)
                    self.instruments.supply.outp_OFF(channel=4)
                    sleep(0.1)
                    self.instruments.supply.outp_ON(channel=1)
                    # self.instruments.supply.setVoltage(channel=1,voltage=5)
                    if False:
                        pass
                    elif re.search('DCO',trim.get('Trimming_Name ')):
                        print(trim.get('Trimming_Name '))
                        dco = DCO_Trim(dut=self.dut,DFT=trim,Instruments=self.instruments)
                        dco.dco_Test__SetUp()
                        result = dco.dco_results()
                        print(result)
                        trim_result.append(result)
                        self.writeData(chip_Index=chip_index_start,trim_results=trim_result)
                    elif re.search('Aon BG vref 1.2V',trim.get('Trimming_Name ')):
                        print(trim.get('Trimming_Name '))
                        self.matrix.force_Matrix__Switchx(trim.get('Trimming_Name '))
                        aon_Bg_Vref_1p2 = Aon_Bg_Vref_1p2V_Trim(dut=self.dut,DFT=trim,Instruments=self.instruments)
                        aon_Bg_Vref_1p2.Aon_Bg_Vref_1p2V_Test__SetUp()
                        result=aon_Bg_Vref_1p2.Aon_Bg_Vref_1p2V_results()
                        print(result)
                        trim_result.append(result)
                        self.writeData(chip_Index=chip_index_start,trim_results=trim_result)
                    # elif re.search('Aon vref 0.6V',trim.get('Trimming_Name ')):
                    #     print(trim.get('Trimming_Name '))
                    #     # self.matrix.force_Matrix__Switchx(trim.get('Trimming_Name '))
                    #     aon_Vref_0p6 = Aon_Vref_0p6V_Trim(dut=self.dut,DFT=trim,Instruments=self.instruments)
                    #     aon_Vref_0p6.Aon_Vref_0p6V_Test__SetUp()
                    #     # input('Connect TEST1 to 1.2v and let it discharge to 0.6v >')
                    #     result=aon_Vref_0p6.Aon_Vref_0p6V_results()
                    #     print(result)
                    #     trim_result.append(result)
                    #     self.writeData(chip_Index=chip_index_start,trim_results=trim_result)
                    elif re.search('Aon ldo_vref_1p2 trimming',trim.get('Trimming_Name ')):
                        print(trim.get('Trimming_Name '))
                        aon_Vref_1p2 = Aon_Vref_1p2V_Trim(dut=self.dut,DFT=trim,Instruments=self.instruments)
                        aon_Vref_1p2.Aon_Vref_1p2V_Test__SetUp()
                        result=aon_Vref_1p2.Aon_Vref_1p2V_results()
                        print(result)
                        trim_result.append(result)
                        self.writeData(chip_Index=chip_index_start,trim_results=trim_result)
                    elif re.search('LDO1.2 Trimming',trim.get('Trimming_Name ')):
                        print(trim.get('Trimming_Name '))
                        self.matrix.force_Matrix__Switchx(trim.get('Trimming_Name '))
                        ldo_1p2 = Ldo_1p2V_Trim(dut=self.dut,DFT=trim,Instruments=self.instruments)
                        ldo_1p2.Ldo_1p2V_Test__SetUp()
                        result=ldo_1p2.Ldo_1p2V_results()
                        print(result)
                        trim_result.append(result)
                        self.writeData(chip_Index=chip_index_start,trim_results=trim_result)
                    elif re.search('Main BG Current Trimming',trim.get('Trimming_Name ')):
                        self.matrix.force_Matrix__Switchx(trim.get('Trimming_Name '))
                        input('Connect TEST1 to Current meter for Main BG Current Trimming >')
                        main_bg = Main_Bg_Trim(dut=self.dut,DFT=trim,Instruments=self.instruments)
                        main_bg.Main_Bg_Test__SetUp()
                        result=main_bg.Main_Bg_results()
                        print(result)
                        trim_result.append(result)
                        self.writeData(chip_Index=chip_index_start,trim_results=trim_result)
                    elif re.search('Aon vddsns_ovp trimming',trim.get('Trimming_Name ')):
                        vdd_sns_ovp = Vdd_Sns_Ovp_Trim(dut=self.dut,DFT=trim,Instruments=self.instruments)
                        vdd_sns_ovp. Vdd_Sns_Ovp_Test__SetUp()
                        result=vdd_sns_ovp. Vdd_Sns_Ovp_results()
                        print(result)
                        trim_result.append(result)
                        self.writeData(chip_Index=chip_index_start,trim_results=trim_result)
                    elif re.search('PH13 IND CS Buffer',trim.get('Trimming_Name ')):
                        print(trim.get('Trimming_Name '))
                        self.startup.buck_PowerUp()
                        self.matrix.force_Matrix__Switchx(trim.get('Trimming_Name '))
                        ph13_indcs_buff = Ph13_IndCs_Buff_Trim(dut=self.dut,DFT=trim,Instruments=self.instruments)
                        ph13_indcs_buff.Ph13_IndCs_Buff_Test__SetUp()
                        result=ph13_indcs_buff.Ph13_IndCs_Buff_results()
                        print(result)
                        trim_result.append(result)
                        self.writeData(chip_Index=chip_index_start,trim_results=trim_result)
                        self.startup.buck_PowerDown()
                    elif re.search('PH24 IND CS Buffer',trim.get('Trimming_Name ')):
                        print(trim.get('Trimming_Name '))
                        self.startup.buck_PowerUp()
                        self.matrix.force_Matrix__Switchx(trim.get('Trimming_Name '))
                        ph24_indcs_buff = Ph24_IndCs_Buff_Trim(dut=self.dut,DFT=trim,Instruments=self.instruments)
                        ph24_indcs_buff.Ph24_IndCs_Buff_Test__SetUp()
                        result=ph24_indcs_buff.Ph24_IndCs_Buff_results()
                        print(result)
                        trim_result.append(result)
                        self.writeData(chip_Index=chip_index_start,trim_results=trim_result)
                        self.startup.buck_PowerDown()
                    # elif re.search('PH',trim.get('Trimming_Name ')):
                    #     # sleep(1)
                    #     # self.instruments.supply.outp_OFF(channel=1)
                    #     self.instruments.supply.setVoltage(channel=1,voltage=0)
                    #     sleep(0.1)
                    #     # self.instruments.supply.outp_ON(channel=1)
                    #     self.instruments.supply.setVoltage(channel=1,voltage=5)
                    #     sleep(0.1)
                    #     # self.loadTrim.loadTrims()
                    #     for reg in trim_result :
                    #         if reg :
                    #             self.apis.write_register(register=reg.get('Register'))

                    #     if re.search('IND CS Mirror trimming',trim.get('Trimming_Name ')):
                    #             # input('IND CS Mirror Trimming >')
                    #         if re.search('PH4',trim.get('Trimming_Name ')):
                    #             pass
                    #         else:
                    #             self.startup.buck_PowerUp()
                    #             # input('>')
                    #             sleep(0.1)
                    #             print(trim.get('Trimming_Name '))
                    #             self.matrix.force_Matrix__Switchx(trim.get('Trimming_Name '))
                    #             # sleep(1)
                    #             PhxSy_indcs_mirror = PhxSy_Indcs_Mirror_Trim(dut=self.dut,DFT=trim,Instruments=self.instruments)
                    #             PhxSy_indcs_mirror.PhxSy_Indcs_Mirror_Test__SetUp()
                    #             result=PhxSy_indcs_mirror.PhxSy_Indcs_Mirror_results()
                    #             print(result)
                    #             trim_result.append(result)
                    #             self.writeData(chip_Index=chip_index_start,trim_results=trim_result)
                    #             self.startup.buck_PowerDown()
                    #             # pass

                    #     elif re.search('IND CS Offset trimming',trim.get('Trimming_Name ')):
                    #         # if re.search('PH4',trim.get('Trimming_Name ')):
                    #         #     pass
                    #         # else:
                    #             self.startup.buck_PowerUp()
                    #             sleep(0.1)
                    #             print(trim.get('Trimming_Name '))
                    #             self.matrix.force_Matrix__Switchx(trim.get('Trimming_Name '))
                    #             # sleep(0.3)
                    #             PhxSy_indcs_offset = PhxSy_Indcs_Offset_Trim(dut=self.dut,DFT=trim,Instruments=self.instruments)
                    #             PhxSy_indcs_offset.PhxSy_Indcs_Offset_Test__SetUp()
                    #             result=PhxSy_indcs_offset.PhxSy_Indcs_Offset_results()
                    #             print(result)
                    #             trim_result.append(result)
                    #             self.writeData(chip_Index=chip_index_start,trim_results=trim_result)
                    #             self.startup.buck_PowerDown()
                    #     elif re.search('IND CS Gain trimming',trim.get('Trimming_Name ')):
                    #         # if re.search('PH4',trim.get('Trimming_Name ')):
                    #         #     pass
                    #         # else:
                    #             self.startup.buck_PowerUp()
                    #             sleep(0.1)
                    #             print(trim.get('Trimming_Name '))
                    #             self.matrix.force_Matrix__Switchx(trim.get('Trimming_Name '))
                    #             # sleep(0.3)
                    #             PhxSy_indcs_gain = PhxSy_Indcs_Gain_Trim(dut=self.dut,DFT=trim,Instruments=self.instruments)
                    #             PhxSy_indcs_gain.PhxSy_Indcs_Gain_Test__SetUp()
                    #             result=PhxSy_indcs_gain.PhxSy_Indcs_Gain_results()
                    #             print(result)
                    #             trim_result.append(result)
                    #             self.writeData(chip_Index=chip_index_start,trim_results=trim_result)
                    #             self.startup.buck_PowerDown()
                    #     elif re.search('ZC Comparator trimming',trim.get('Trimming_Name ')):
                    #         self.startup.buck_PowerUp()
                    #         sleep(0.1)
                    #         print(trim.get('Trimming_Name '))
                    #         self.matrix.force_Matrix__Switchx(trim.get('Trimming_Name '))
                    #         PhxSy_indcs_zc = PhxSy_Indcs_ZC_Trim(dut=self.dut,DFT=trim,Instruments=self.instruments)
                    #         PhxSy_indcs_zc.PhxSy_Indcs_ZC_Test__SetUp()
                    #         result=PhxSy_indcs_zc.PhxSy_Indcs_ZC_results()
                    #         print(result)
                    #         trim_result.append(result)
                    #         self.writeData(chip_Index=chip_index_start,trim_results=trim_result)
                    #         self.startup.buck_PowerDown()
                        
                    end_time = time()

                    print('*'*20)
                    print('TrimName',trim.get('Trimming_Name '),'StartingTime ',ctime(start_time),'Ending Time',ctime(end_time))
                    print('*'*20)

            

                self.dut.block_apis.SIMULINK_MODEL.set_standby_en(1)
                self.startup.buck_PowerDown()
                self.instruments.supply.outp_OFF(channel=1)
                self.instruments.supply.outp_OFF(channel=3)
                self.instruments.supply.outp_OFF(channel=4)
                self.trim_results.update({
                        chip_index:trim_result
                    })
                chip_index=chip_index+1
                resultsfilename = f'TrimmingResults_{str(chip_index-1)}_{str(chip_index-1)}'
                with open(f'json/{resultsfilename}.json', 'w', encoding='utf-8') as f:
                    print('................................')
                    json.dump(self.trim_results, f, ensure_ascii=False, indent=4)
                
        except KeyboardInterrupt :
            self.matrix.reset()
            # self.dut.copy_trims_to_eeprom()
            # self.startup.buck_PowerDown()
            self.dut.block_apis.SIMULINK_MODEL.set_standby_en(1)
            self.instruments.supply.outp_OFF(channel=1)
            self.instruments.supply.outp_OFF(channel=3)
            self.instruments.supply.outp_OFF(channel=4)
            
            # resultsfilename = f'TrimmingResults_{str(chip_index_start)}_{str(chip_index-1)}'
            # with open(f'json/{resultsfilename}.json', 'w', encoding='utf-8') as f:
            #     print('................................')
            #     json.dump(self.trim_results, f, ensure_ascii=False, indent=4)

    def writeData(self,trim_results,chip_Index):
            resultsfilename = f'TrimmingResults_{str(chip_Index)}_{str(chip_Index)}'
            with open(f'json/{resultsfilename}.json', 'w', encoding='utf-8') as f:
                print('................................')
                json.dump(trim_results, f, ensure_ascii=False, indent=4)
            

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

      
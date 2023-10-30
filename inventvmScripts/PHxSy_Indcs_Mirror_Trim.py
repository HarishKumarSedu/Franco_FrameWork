import re , pandas as pd , time
from Franco_Test__APIs import FrancoAPIS
from startup import Startup
class PhxSy_Indcs_Mirror_Trim:

    def __init__(self,dut,DFT,Instruments) -> None:
        self.DFT = DFT
        self.dut = dut
        self.apis = FrancoAPIS(dut=dut)
        self.startup = Startup(dut=dut)
        self.multimeter = Instruments.multimeter
        self.supply = Instruments.supply
        time.sleep(5)
        self.registers = []
        self.trim_code = []
        self.trim_results={}


    def PhxSy_Indcs_Mirror_Test__SetUp(self):
        # self.startup.cirrus_Startup() # Run the buck powerup 
        self.startup.IVM_Startup() # Run the buck powerup 
        # self.startup.buck_PowerUp() # Run the buck powerup 
        # set the powersupply @vsys with sinfel quadrent 
        # self.dut.IVM.REG_TEST0_RW.DS_PH1_DRV_TEST_HS.value=0
        # self.dut.IVM.REG_TEST0_RW.DS_PH1_DRV_TEST_EN.value=1
        # self.dut.IVM.REG_TEST0_RW.DS_PH1_DRV_TEST_EN.value=0
        # time.sleep(0.1)
        # print('self.dut.IVM.REG_TEST0_RW.DS_PH1_DRV_TEST_HS.value=1')
        # self.dut.IVM.REG_TEST0_RW.DS_PH1_DRV_TEST_HS.value=1
        # self.dut.IVM.REG_TEST0_RW.DS_PH1_DRV_TEST_EN.value=1
        # self.dut.IVM.REG_FORCE_RW.DS_PH1_INDCS_FORCE_EN.value=1
        # self.dut.IVM.REG_FORCE_RW.DS_PH1_INDCS_FORCE_SEL.value=1
        self.supply.outp_OFF(channel=3)
        self.supply.setCurrent_Priority(channel=3)
        self.multimeter.set_Voltage__NPLC(1)
        time.sleep(0.1)
        for Instruction in self.DFT.get("Instructions"):
            # parse Ldo_1p2V instruction register 
            if re.match(re.compile('0x'),Instruction):
                reg_data = self.apis.parse_registerAddress_from_string(Instruction)
                if reg_data:
                    self.registers.append(reg_data)
                    self.apis.write_register(register=reg_data)
            if re.search(re.compile('TrimSweep'),Instruction):
                # input('>')
                self.trim_register_data = self.apis.parse_trim_registerAddress_from_string(Instruction)


        # force the 0A
        self.supply.outp_OFF(channel=3)
        self.supply.setCurrent(channel=3,current=0)
        self.measure_values_0A = self.PhxSy_Indcs_Mirror_Values__Sweep()
        time.sleep(0.1)
        self.supply.setCurrent(channel=3,current=1)
        self.supply.outp_ON(channel=3)
        self.measure_values_1A=self.PhxSy_Indcs_Mirror_Values__Sweep()
        self.supply.outp_OFF(channel=3)
        time.sleep(0.1)
        self.supply.setCurrent(channel=3,current=-1)
        self.supply.outp_ON(channel=3)
        time.sleep(0.1)
        self.measure_values_m1A=self.PhxSy_Indcs_Mirror_Values__Sweep()
        time.sleep(0.1)
        self.supply.outp_OFF(channel=3)
        # print(self.measure_values_0A,self.measure_values_1A,self.measure_values_m1A)
        
        self.PhxSy_Indcs_Mirror_Limit__Check()

    def PhxSy_Indcs_Mirror_Values__Sweep(self):
        measure_values=[]
        self.trim_code.clear()
        if self.trim_register_data:
            for value in range(0,2**(self.trim_register_data.get('RegisterMSB') - self.trim_register_data.get('RegisterLSB') +1),1):
                self.apis.write_register(register=self.trim_register_data,write_value=value)
                self.trim_code.append(value)
                time.sleep(0.05)
                measure_values.append(self.multimeter.meas_V()) # get the frequency values from multimeter
        # self.PhxSy_Indcs_Mirror_Limit__Check()
        return measure_values
    
    def PhxSy_Indcs_Mirror_Limit__Check(self):
        # limits are not in percentage
        vout=[]
        vout_abs=[]
        typical = 0.075
        # print('self.measure_values_1A[i] ',len(self.measure_values_1A ),'self.measure_values_0A[i]',self.measure_values_0A,'self.measure_values_m1A[i]',len(self.trim_code))
        for i in range(0,len(self.trim_code)):
            vout.append((self.measure_values_1A[i] - 2*self.measure_values_0A[i]+self.measure_values_m1A[i] ))
            vout_abs.append(abs(vout[i]))

        error_min = min(vout_abs)
        error_min__Index =vout_abs.index(error_min)
        self.trim_register_data.update({
                    "RegisterValue":self.trim_code[error_min__Index]
                })
        self.apis.write_register(register=self.trim_register_data)

        # Apply 1A and get the vout 
        time.sleep(0.1)
        # if re.search('S4',self.DFT.get('Trimming_Name ')):
        #     self.supply.setCurrent(channel=3,current=-1)
        # else:
        #     self.supply.setCurrent(channel=3,current=1)

        if re.search('S4',self.DFT.get('Trimming_Name ')):
            # input('Gain Trim finished >')
            self.supply.outp_ON(channel=3)
            self.supply.setCurrent(channel=3,current=1) 
            time.sleep(0.5)
            vout_m1A = abs(self.multimeter.meas_V()) 
            # input(f'vout 1A {vout_1A}')
            time.sleep(0.5)
            self.supply.setCurrent(channel=3,current=-1) 
            time.sleep(0.5)
            vout_1A = abs(self.multimeter.meas_V()) 
            # input(f'vout -1A {vout_m1A}')
        else:
            # input('Gain Trim finished >')
            self.supply.outp_ON(channel=3)
            self.supply.setCurrent(channel=3,current=1) 
            time.sleep(0.5)
            vout_1A = abs(self.multimeter.meas_V()) 
            # input(f'vout 1A {vout_1A}')
            time.sleep(0.5)
            self.supply.setCurrent(channel=3,current=-1) 
            time.sleep(0.5)
            vout_m1A = abs(self.multimeter.meas_V()) 
            # input(f'vout -1A {vout_m1A}')
        time.sleep(0.5)
        self.supply.setCurrent(channel=3,current=0) 
        time.sleep(0.5)
        vout_0A = abs(self.multimeter.meas_V()) 
        # input(f'vout 0A {vout_0A}')
        time.sleep(0.5)
 
        self.supply.outp_OFF(channel=3)
        # input('Mirror Trim finiesd >')
        if re.search('S4',self.DFT.get('Trimming_Name ')):
            vout = vout_m1A
        else:
            vout = vout_1A
        limit_max = vout + vout*0.16
        limit_min = vout - vout*0.16
        print('Limit max',limit_max,'limit min',limit_min,'Vout_1A',vout_1A,'Vout_m1A',vout_m1A,'Vout_0A',vout_0A,'error min',error_min)
        if vout > limit_min and vout < limit_max :
        # if True :

            # self.trim_register_data.update({
            #         "RegisterValue":self.trim_code[error_min__Index]
            #     })
            # self.apis.write_register(register=self.trim_register_data)

            self.trim_results = {
                "Name" : self.DFT.get('Trimming_Name '),
                "Register":self.trim_register_data,
                "Vout_1A":vout_1A,
                "Vout_m1A":vout_m1A,
                "Vout_0A":vout_0A,
                "MeasureValue":vout_1A,
                "typical":typical,
                "MinError":abs(typical - vout_1A),
                "Trim":True
            }
        else:
            self.trim_register_data.update({
                    "RegisterValue":self.trim_code[error_min__Index]
                })
            self.apis.write_register(register=self.trim_register_data)

            self.trim_results = {
                "Name" : self.DFT.get('Trimming_Name '),
                "Register":self.trim_register_data,
                "MeasureValue":vout_1A,
                "typical":typical,
                "MinError":abs(typical - vout_1A),
                "Trim":False
            }

        for register in self.registers:
            self.apis.write_register(register=register,write_value=0)
        # self.startup.cirrus_PowerDown()
        self.startup.IVM_Powerdown()


    def PhxSy_Indcs_Mirror_results (self):
        return self.trim_results

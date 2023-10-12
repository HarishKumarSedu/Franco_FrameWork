import re , pandas as pd , time
from Franco_Test__APIs import FrancoAPIS
from startup import Startup
class Ph1S1_Indcs_Mirror_Trim:

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


    def Ph1S1_Indcs_Mirror_Test__SetUp(self):
        self.startup.buck_PowerUp() # Run the buck powerup 
        # set the powersupply @vsys with sinfel quadrent 
        self.supply.outp_OFF(channel=3)
        self.supply.setCurrent_Priority(channel=3)
        for Instruction in self.DFT.get("Instructions"):
            # parse Ldo_1p2V instruction register 
            if re.match(re.compile('0x'),Instruction):
                reg_data = self.apis.parse_registerAddress_from_string(Instruction)
                if reg_data:
                    self.registers.append(reg_data)
                    self.apis.write_register(register=reg_data)
            if re.search(re.compile('TrimSweep'),Instruction):
                self.trim_register_data = self.apis.parse_trim_registerAddress_from_string(Instruction)
        # force the 0A
        self.supply.outp_OFF(channel=3)
        self.supply.setCurrent(channel=3,current=0)
        self.measure_values_0A = self.Ph1S1_Indcs_Mirror_Values__Sweep()
        time.sleep(0.1)
        self.supply.setCurrent(channel=3,current=1)
        self.supply.outp_ON(channel=3)
        time.sleep(0.1)
        self.measure_values_1A=self.Ph1S1_Indcs_Mirror_Values__Sweep()
        self.supply.outp_OFF(channel=3)
        self.supply.setCurrent(channel=3,current=-1)
        self.supply.outp_ON(channel=3)
        time.sleep(0.1)
        self.measure_values_m1A=self.Ph1S1_Indcs_Mirror_Values__Sweep()
        self.supply.outp_OFF(channel=3)
        # print(self.measure_values_0A,self.measure_values_1A,self.measure_values_m1A)
        
        self.Ph1S1_Indcs_Mirror_Limit__Check()

    def Ph1S1_Indcs_Mirror_Values__Sweep(self):
        measure_values=[]
        self.trim_code.clear()
        if self.trim_register_data:
            for value in range(0,2**(self.trim_register_data.get('RegisterMSB') - self.trim_register_data.get('RegisterLSB') +1),1):
                self.apis.write_register(register=self.trim_register_data,write_value=value)
                self.trim_code.append(value)
                # time.sleep(0.1)
                measure_values.append(self.multimeter.meas_V()) # get the frequency values from multimeter
        # self.Ph1S1_Indcs_Mirror_Limit__Check()
        return measure_values
    
    def Ph1S1_Indcs_Mirror_Limit__Check(self):
        # limits are not in percentage
        vout=[]
        vout_abs=[]
        # print('self.measure_values_1A[i] ',len(self.measure_values_1A ),'self.measure_values_0A[i]',self.measure_values_0A,'self.measure_values_m1A[i]',len(self.trim_code))
        for i in range(0,len(self.trim_code)):
            vout.append((self.measure_values_1A[i] - 2*self.measure_values_0A[i]+self.measure_values_m1A[i] ))
            vout_abs.append(abs(vout[i]))

        error_min = min(vout_abs)
        error_min__Index =vout_abs.index(error_min)
        actual_error = abs(self.measure_values_1A[error_min__Index]) - abs(self.measure_values_m1A[error_min__Index])

        if actual_error > -0.01 and actual_error < 0.01:
            print("Minimum error",error_min)
            print("Min Value",vout_abs[error_min__Index])
            print("Min Value code",self.trim_code[error_min__Index])

            self.trim_register_data.update({
                    "RegisterValue":self.trim_code[error_min__Index]
                })
            self.apis.write_register(register=self.trim_register_data)

            self.trim_results = {
                "Name" : self.DFT.get('Trimming_Name '),
                "Register":self.trim_register_data,
                "MeasureValue":actual_error,
                "typical":0.01,
                "MinError":error_min,
            }
            for register in self.registers:
                self.apis.write_register(register=register,write_value=0)

    def Ph1S1_Indcs_Mirror_results (self):
        return self.trim_results

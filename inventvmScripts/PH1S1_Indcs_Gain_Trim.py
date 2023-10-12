import re , pandas as pd , time
from Franco_Test__APIs import FrancoAPIS
from startup import Startup
class Ph1S1_Indcs_Gain_Trim:
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


    def Ph1S1_Indcs_Gain_Test__SetUp(self):
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
                self.Ph1S1_Indcs_Gain_Values__Sweep()

    def Ph1S1_Indcs_Gain_Values__Sweep(self):
        self.supply.outp_OFF(channel=3)
        self.supply.setCurrent(channel=3,current=1)
        self.measure_values_1A=[]
        if self.trim_register_data:
            for value in range(0,2**(self.trim_register_data.get('RegisterMSB') - self.trim_register_data.get('RegisterLSB') +1),1):
                self.apis.write_register(register=self.trim_register_data,write_value=value)
                self.trim_code.append(value)
                time.sleep(0.1)
                self.measure_values_1A.append(self.multimeter.meas_V()) # get the frequency values from multimeter
        self.Ph1S1_Indcs_Gain_Limit__Check()

    def Ph1S1_Indcs_Gain_Limit__Check(self):
        # limits are not in percentage
        limit_max = (0.075-0.075*0.31)
        limit_min = (0.075+0.075*0.31)
        typical = 75*0.001 + 75*0.001*0.01
        
        error = []
        error_abs = []

        for i in self.measure_values_1A:
            err = (abs(i) - typical)
            error_abs.append(abs(err))
            error.append(err)

        error_min = min(error_abs)
        error_min__Index =error_abs.index(error_min)
        if error_min > limit_min and  error_min < limit_max:
        # if error[error_min__Index] > limit_min and error[error_min__Index] < limit_max:
            print("Minimum error",error[error_min__Index])
            print("Min Value",self.measure_values_1A[error_min__Index])
            print("Min Value code",self.trim_code[error_min__Index])
            self.apis.write_register(register=self.trim_register_data,write_value=self.trim_code[error_min__Index])

            self.trim_register_data.update({
                    "RegisterValue":self.trim_code[error_min__Index]
                })

            self.trim_results = {
                "Name" : self.DFT.get('Trimming_Name '),
                "Register":self.trim_register_data,
                "MeasureValue":self.measure_values_1A[error_min__Index],
                "typical":typical,
                "MinError":error[error_min__Index],
            }
            #reset the test driver 
            for register in self.registers:
                self.apis.write_register(register=register,write_value=0)

    def Ph1S1_Indcs_Gain_results (self):
        return self.trim_results

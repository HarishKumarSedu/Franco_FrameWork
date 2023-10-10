import re , pandas as pd , time
from Franco_Test__APIs import FrancoAPIS

class Main_Bg_Trim:

    def __init__(self,dut,DFT,Instruments) -> None:
        self.DFT = DFT
        self.dut = dut
        self.apis = FrancoAPIS(dut=dut)
        self.currentmeter = Instruments.currentmeter
        time.sleep(5)
        self.registers = []
        self.measure_values = []
        self.trim_code = []
        self.trim_results={}
    
    def Main_Bg_Test__SetUp(self):
        for Instruction in self.DFT.get("Instructions"):
            # parse Main_Bg instruction register 
            if re.match(re.compile('0x'),Instruction):
                reg_data = self.apis.parse_registerAddress_from_string(Instruction)
                if reg_data:
                    self.registers.append(reg_data)
                    self.apis.write_register(register=reg_data)
            if re.search(re.compile('TrimSweep'),Instruction):
                self.trim_register_data = self.apis.parse_trim_registerAddress_from_string(Instruction)
                self.Main_Bg_Values__Sweep()


                # print(self.measure_values)
        # print(self.registers)

    def Main_Bg_Values__Sweep(self):
        
        if self.trim_register_data:
            for value in range(0,2**(self.trim_register_data.get('RegisterMSB') - self.trim_register_data.get('RegisterLSB') +1),1):
                self.apis.write_register(register=self.trim_register_data,write_value=value)
                self.trim_code.append(value)
                time.sleep(0.1)
                self.measure_values.append(self.currentmeter.meas_I()) # get the frequency values from voltmeter
        
        self.Main_Bg_Limit__Check()
    
    def Main_Bg_Limit__Check(self):
        # limits are not in percentage
        limit_max = self.DFT.get("MAX_LSB/%")*100
        limit_min = self.DFT.get("MIN_LSB/%")*100
        typical = 1.5*(10**-6)
        
        error = []
        error_abs = []

        for i in self.measure_values:
            err = ((i - typical))
            error_abs.append(abs(err))
            error.append(err)

        error_min = min(error_abs)
        error_min__Index =error_abs.index(error_min)
        if error[error_min__Index] > limit_min and error[error_min__Index] < limit_max:
            print("Minimum error",error[error_min__Index])
            print("Min Value",self.measure_values[error_min__Index])
            print("Min Value code",self.trim_code[error_min__Index])
            self.apis.write_register(register=self.trim_register_data,write_value=self.trim_code[error_min__Index])

            self.trim_register_data.update({
                    "RegisterValue":self.trim_code[error_min__Index]
                })

            self.trim_results = {
                "Name" : self.DFT.get('Trimming_Name '),
                "Register":self.trim_register_data,
                "MeasureValue":self.measure_values[error_min__Index],
                "typical":typical,
                "MinError":error[error_min__Index],
            }

    def Main_Bg_results (self):
        return self.trim_results

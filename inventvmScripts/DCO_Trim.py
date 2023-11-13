import re , pandas as pd , time
from Franco_Test__APIs import FrancoAPIS

class DCO_Trim:

    def __init__(self,dut,DFT,Instruments) -> None:
        self.DFT = DFT
        self.dut = dut
        self.apis = FrancoAPIS(dut=dut)
        self.scope = Instruments.scope
        time.sleep(5)
        self.registers = []
        self.measure_values = []
        self.trim_code = []
        self.trim_results={}
    
    def dco_Test__SetUp(self):
        for Instruction in self.DFT.get("Instructions"):
            #parse dco instruction register 
            if re.match(re.compile('0x'),Instruction):
                reg_data = self.apis.parse_registerAddress_from_string(Instruction)
                if reg_data:
                    self.registers.append(reg_data)
                    self.apis.write_register(register=reg_data)
            elif re.search(re.compile('TrimSweep'),Instruction):
                self.trim_register_data = self.apis.parse_trim_registerAddress_from_string(Instruction)
                self.dco_Values__Sweep()

                # print(self.measure_values)
        # print(self.registers)

    def dco_Values__Sweep(self):
        # self.scope.set_autoSet()
        self.scope.set_trigger__mode(mode='AUTO')
        self.scope.set_HScale()
        self.scope.set_Channel__VScale(scale=0.1)
        # self.scope.init_scopePosEdge__Trigger(channel='CH1')
        time.sleep(1)
        if self.trim_register_data:
            for value in range(0,2**(self.trim_register_data.get('RegisterMSB') - self.trim_register_data.get('RegisterLSB') +1),1):
                self.apis.write_register(register=self.trim_register_data,write_value=value)
                time.sleep(0.01)
                freq = 0
                for i in range(0,10):
                    freq= freq + self.scope.meas_Freq()
                self.measure_values.append(freq/10) # get the frequency values from scope
                self.trim_code.append(value)
        
        self.dco_Limit__Check()
    
    def dco_Limit__Check(self):
        limit_max = self.DFT.get("MAX_LSB/%")*100
        limit_min = self.DFT.get("MIN_LSB/%")*100
        typical = int(self.DFT.get("TYP_LIMIT"))
        if self.DFT.get("Unit") == 'MHz':
            typical = typical*(10**6)
        
        error = []
        error_abs = []

        for freq in self.measure_values:
            err = ((freq - typical)/typical)*100
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

    def dco_results (self):
        return self.trim_results

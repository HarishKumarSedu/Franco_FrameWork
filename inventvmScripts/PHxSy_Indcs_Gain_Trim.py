import re , pandas as pd , time
from Franco_Test__APIs import FrancoAPIS
from startup import Startup
class PhxSy_Indcs_Gain_Trim:
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


    def PhxSy_Indcs_Gain_Test__SetUp(self):
        self.startup.cirrus_Startup() # Run the buck powerup 
        # self.startup.IVM_Startup() # Run the buck powerup 
        # self.startup.buck_PowerUp() # Run the buck powerup 
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
                self.PhxSy_Indcs_Gain_Values__Sweep()

    def PhxSy_Indcs_Gain_Values__Sweep(self):
        self.supply.outp_ON(channel=3)
        self.supply.setCurrent(channel=3,current=1)
        self.measure_values_1A=[]
        if self.trim_register_data:
            for value in range(0,2**(self.trim_register_data.get('RegisterMSB') - self.trim_register_data.get('RegisterLSB') +1),1):
                self.apis.write_register(register=self.trim_register_data,write_value=value)
                self.trim_code.append(value)
                time.sleep(0.01)
                self.measure_values_1A.append(self.multimeter.meas_V() - 0.075) # get the frequency values from multimeter
        self.supply.setCurrent(channel=3,current=0)
        self.supply.outp_OFF(channel=3)
        self.PhxSy_Indcs_Gain_Limit__Check()

    def PhxSy_Indcs_Gain_Limit__Check(self):
        # limits are not in percentage
        limit_max = (0.075+0.075*0.31)
        limit_min = (0.075-0.075*0.31)
        typical = 0.075 + 0.075*0.01
        
        error = []
        error_abs = []
        measure_values_1A_abs=[]
        for i in self.measure_values_1A:
            err = typical-abs(i)
            error_abs.append(abs(err))
            error.append(err)
            measure_values_1A_abs.append(abs(i))

        error_min = min(measure_values_1A_abs)
        error_min__Index =measure_values_1A_abs.index(error_min)
        print('error min',error_min,'max',limit_max,'min',limit_min)
        if error_min < limit_max  and error_min < limit_max:
        # if error[error_min__Index] > limit_min and error[error_min__Index] < limit_max:
            print("Minimum error",abs(typical - error_min))
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
                "MinError":abs(typical - error_min),
            }
            #reset the test driver 
            for register in self.registers:
                self.apis.write_register(register=register,write_value=0)
            self.startup.cirrus_PowerDown()
            # self.startup.IVM_Powerdown() # Run the buck powerup 

    def PhxSy_Indcs_Gain_results (self):
        self.startup.cirrus_PowerDown()
        # self.startup.IVM_Powerdown()

        return self.trim_results

import re , pandas as pd , time
from Franco_Test__APIs import FrancoAPIS
from startup import Startup
class PhxSy_Indcs_Offset_Trim:

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


    def PhxSy_Indcs_Offset_Test__SetUp(self):
        # self.startup.IVM_Startup()
        self.startup.cirrus_Startup() # Run the buck powerup 
        # self.startup.buck_PowerUp() # Run the buck powerup 
        # set the powersupply @vsys with sinfel quadrent 
        self.supply.outp_OFF(channel=3)
        # self.supply.setCurrent_Priority(channel=3)
        for Instruction in self.DFT.get("Instructions"):
            # parse Ldo_1p2V instruction register 
            if re.match(re.compile('0x'),Instruction):
                reg_data = self.apis.parse_registerAddress_from_string(Instruction)
                if reg_data:
                    self.registers.append(reg_data)
                    self.apis.write_register(register=reg_data)
            if re.search(re.compile('TrimSweep'),Instruction):
                self.trim_register_data = self.apis.parse_trim_registerAddress_from_string(Instruction)
                self.PhxSy_Indcs_Offset_Values__Sweep()

    def PhxSy_Indcs_Offset_Values__Sweep(self):
        self.measure_values_0A=[]
        if self.trim_register_data:
            for value in range(0,2**(self.trim_register_data.get('RegisterMSB') - self.trim_register_data.get('RegisterLSB') +1),1):
                self.apis.write_register(register=self.trim_register_data,write_value=value)
                self.trim_code.append(value)
                # time.sleep(0.1)
                self.measure_values_0A.append(self.multimeter.meas_V()) # get the frequency values from multimeter
        self.PhxSy_Indcs_Offset_Limit__Check()

    def PhxSy_Indcs_Offset_Limit__Check(self):
        # limits are not in percentage
        limit_max = float(self.DFT.get("MAX_LIMIT"))
        limit_min = float(self.DFT.get("MIN_LIMIT"))
        limit_unit = self.DFT.get("Unit")   
        typical = 1.21
        # multiply limit with milli
        if re.search("m",limit_unit):
            limit_max = limit_max*0.001
            limit_min = limit_min*0.001
            typical = typical*0.001

        error = []
        error_abs = []
        measure_values_0A_abs=[]
        for i in self.measure_values_0A:
            err=((typical-abs(i)))
            error.append(err)
            error_abs.append(abs(err))
            measure_values_0A_abs.append(abs(i))

        error_min = min(error_abs)
        error_min__Index =error_abs.index(error_min)
        print('error min',error_min,'limit max',limit_max)
        if error_min < limit_max:
            print("Minimum error",error[error_min__Index])
            print("Min Value",self.measure_values_0A[error_min__Index])
            print("Min Value code",self.trim_code[error_min__Index])

            self.trim_register_data.update({
                    "RegisterValue":self.trim_code[error_min__Index]
                })
            #write the optimal code 
            self.apis.write_register(register=self.trim_register_data)
            # update the trim results 
            self.trim_results = {
                "Name" : self.DFT.get('Trimming_Name '),
                "Register":self.trim_register_data,
                "MeasureValue":self.measure_values_0A[error_min__Index],
                "typical":typical,
                "MinError":error[error_min__Index],
            }
            #reset the test driver 
            for register in self.registers:
                self.apis.write_register(register=register,write_value=0)
            self.startup.cirrus_PowerDown()
            # self.startup.IVM_Powerdown()
            self.supply.outp_OFF(channel=3)
    def PhxSy_Indcs_Offset_results (self):
        self.startup.cirrus_PowerDown()
        # self.startup.IVM_Powerdown()
        return self.trim_results

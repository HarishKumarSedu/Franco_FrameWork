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
        # self.startup.cirrus_Startup() # Run the buck powerup 
        self.startup.IVM_Startup() # Run the buck powerup 
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
        if re.search('S4',self.DFT.get('Trimming_Name ')):
            self.supply.setCurrent(channel=3,current=1)
        else:
            self.supply.setCurrent(channel=3,current=-1)
        self.measure_values_1A=[]
        if self.trim_register_data:
            for value in range(0,2**(self.trim_register_data.get('RegisterMSB') - self.trim_register_data.get('RegisterLSB') +1),1):
                self.apis.write_register(register=self.trim_register_data,write_value=value)
                self.trim_code.append(value)
                time.sleep(0.01)
                if re.search('S4',self.DFT.get('Trimming_Name ')):
                    self.measure_values_1A.append(self.multimeter.meas_V() + 0.075) # get the frequency values from multimeter
                else:
                    self.measure_values_1A.append(self.multimeter.meas_V() - 0.075) # get the frequency values from multimeter
                # input('Gain move >')
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
        error_meas = self.measure_values_1A[error_min__Index]
        if re.search('S4',self.DFT.get('Trimming_Name ')):
            measure_value = self.measure_values_1A[error_min__Index] - 0.075
        else:
            measure_value = self.measure_values_1A[error_min__Index] + 0.075
            
        if abs(measure_value) > limit_min and abs(measure_value) < limit_max:
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
                "MeasureValue":measure_value,
                "typical":typical,
                "MinError":measure_values_1A_abs[error_min__Index],
                "Trim": True
            }

            # self.startup.IVM_Powerdown() # Run the buck powerup 
        else:
            self.trim_register_data.update({
                    "RegisterValue":self.trim_code[error_min__Index]
                })

            self.trim_results = {
                "Name" : self.DFT.get('Trimming_Name '),
                "Register":self.trim_register_data,
                "MeasureValue":measure_value,
                "typical":typical,
                "MinError":measure_values_1A_abs[error_min__Index],
                "Trim":False
            }
  
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
        print('Limit max',limit_max,'limit min',limit_min,'Vout_1A',vout_1A,'Vout_m1A',vout_m1A,'Vout_0A',vout_0A,'error_meas',error_meas)
        for register in self.registers:
            self.apis.write_register(register=register,write_value=0)
        # self.startup.cirrus_PowerDown()
        self.startup.IVM_Powerdown()
    def PhxSy_Indcs_Gain_results (self):
        return self.trim_results

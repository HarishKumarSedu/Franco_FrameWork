import re , pandas as pd , time
from Franco_Test__APIs import FrancoAPIS
from startup import Startup
class Vdd_Sns_Ovp_Trim:
    def __init__(self,dut,DFT,Instruments) -> None:
        self.DFT = DFT
        self.dut = dut
        self.apis = FrancoAPIS(dut=dut)
        self.startup = Startup(dut=dut)
        self.supply = Instruments.supply
        self.scope = Instruments.scope
        time.sleep(5)
        self.registers = []
        self.trim_code = []
        self.trim_results={}


    def Vdd_Sns_Ovp_Test__SetUp(self):
        self.supply.outp_OFF(channel=4)
        for Instruction in self.DFT.get("Instructions"):
            if re.match(re.compile('0x'),Instruction):
                reg_data = self.apis.parse_registerAddress_from_string(Instruction)
                if reg_data:
                    self.registers.append(reg_data)
                    self.apis.write_register(register=reg_data)
            if re.search(re.compile('TrimSweep'),Instruction):
                
                self.trim_register_data = self.apis.parse_trim_registerAddress_from_string(Instruction)
                self.Vdd_Sns_Ovp_Values__Sweep()

    def Vdd_Sns_Ovp_Values__Sweep(self):
        self.scope.set_HScale(scale='800E-9')
        self.scope.set_Channel__VScale(channel=1,scale=0.2)
        self.scope.set_trigger__level(level=0.2)
        self.scope.set_trigger__mode(mode='NORM')
        self.scope.init_scopePosEdge__Trigger(channel='CH4')
        # self.scope.single_Trigger__RUN()
        self.scope.scopeTrigger_Acquire(channel='CH4')
        self.supply.setVoltage(channel=4,voltage=4)
        time.sleep(1)
        self.measure_values=[]
        self.supply.outp_ON(channel=4)
        time.sleep(1)
        if self.trim_register_data:
            for value in range(0,2**(self.trim_register_data.get('RegisterMSB') - self.trim_register_data.get('RegisterLSB') +1),1):
                self.apis.write_register(register=self.trim_register_data,write_value=value)
                self.trim_code.append(value)
                time.sleep(0.05)
                # input('Vbat ovp >')
                self.measure_values.append(self.Vdd_Sns_Ovp_Values__Sweep___Voltage()) # get the frequency values from multimeter
        self.supply.setVoltage(channel=4,voltage=0)
        self.supply.outp_OFF(channel=4)
        self.Vdd_Sns_Ovp_Limit__Check()
        print(self.measure_values,self.trim_code)

    def Vdd_Sns_Ovp_Values__Sweep___Voltage(self):
        # time.sleep(0.1)
        voltage=4.2
        self.supply.setVoltage(channel=4,voltage=voltage)
        self.scope.scopeTrigger_Acquire()
        # self.scope.single_Trigger__RUN()
        self.scope.set_Channel__VScale(scale=0.2)
        self.scope.set_trigger__level(level=0.2)
        time.sleep(0.1)
        # while(self.scope.acquireState == True):
        while(self.scope.scopeAcquire_BUSY):
                time.sleep(0.01)
                self.supply.setVoltage(channel=4,voltage=voltage)
                voltage=voltage+0.005
                if voltage > 5.5 :
                    break
        # self.supply.setVoltage(channel=4,voltage=-0.1)
        return self.supply.getVoltage(channel=4)
    
    def Vdd_Sns_Ovp_Limit__Check(self):
        # limits are not in percentage
        limit_max = 4.8+84*0.001
        limit_min = 4.8-96*0.001
        typical = 4.8
        
        error = []
        error_abs = []
        measure_values_abs=[]
        for i in self.measure_values:
            err = typical-abs(i)
            error_abs.append(abs(err))
            error.append(err)
            measure_values_abs.append(i)

        error_min = min(error_abs)
        error_min__Index =error_abs.index(error_min)
        print('error min',error_min,'max',limit_max,'min',limit_min)
        # if error_min < limit_min and  error_min < limit_max:
        if  error[error_min__Index] < limit_max:
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
            #reset the test driver 
            for register in self.registers:
                self.apis.write_register(register=register,write_value=0)
                
            self.scope.set_trigger__mode()
            self.scope.single_Trigger__RUN()

    def Vdd_Sns_Ovp_results (self):
        return self.trim_results


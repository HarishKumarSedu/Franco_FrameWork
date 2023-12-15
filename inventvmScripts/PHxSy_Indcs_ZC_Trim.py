import re , pandas as pd , time
from Franco_Test__APIs import FrancoAPIS
from startup import Startup
class PhxSy_Indcs_ZC_Trim:
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


    def PhxSy_Indcs_ZC_Test__SetUp(self):
        # self.startup.cirrus_Startup() # Run the buck powerup 
        # self.startup.IVM_Startup()
        # self.startup.buck_PowerUp() # Run the buck powerup 
        # set the powersupply @vsys with sinfel quadrent 
        # self.supply.setCurrent_Priority(channel=3)
        self.supply.outp_OFF(channel=3)
        # applicabel to turn the High side (bat bet should be removed )
        if re.search('S1',self.DFT.get('Trimming_Name ')):
            # input('Gain Trim finished >')
            self.supply.setVoltage(channel=4,voltage=4)
            self.supply.outp_ON(channel=4)
        for Instruction in self.DFT.get("Instructions"):
            if re.match(re.compile('0x'),Instruction):
                reg_data = self.apis.parse_registerAddress_from_string(Instruction)
                if reg_data:
                    self.registers.append(reg_data)
                    self.apis.write_register(register=reg_data)
            if re.search(re.compile('TrimSweep'),Instruction):
                self.trim_register_data = self.apis.parse_trim_registerAddress_from_string(Instruction)
                # applicabel to turn the High side (bat bet should be removed )
                if re.search('S1',self.DFT.get('Trimming_Name ')):
                    time.sleep(1)
                    self.supply.setVoltage(channel=4,voltage=0)
                    self.supply.outp_OFF(channel=4)
                # input('Sweep>')
                self.PhxSy_Indcs_ZC_Values__Sweep()

    def PhxSy_Indcs_ZC_Values__Sweep(self):
        self.scope.set_HScale(scale='800E-9')
        self.scope.set_Channel__VScale(scale=0.2)
        self.scope.set_trigger__level(level=0.1)
        self.scope.set_trigger__mode(mode='NORM')
        self.scope.init_scopePosEdge__Trigger()
        # self.scope.single_Trigger__RUN()
        self.scope.scopeTrigger_Acquire()
        # time.sleep(0.1)
        # self.supply.setCurrent(channel=3,current=0)
        # self.supply.outp_ON(channel=3)
        self.measure_values=[]
        if self.trim_register_data:
            for value in range(0,2**(self.trim_register_data.get('RegisterMSB') - self.trim_register_data.get('RegisterLSB') +1),1):
            # for value in range(0,16,1):
                self.apis.write_register(register=self.trim_register_data,write_value=value)
                self.trim_code.append(value)
                time.sleep(0.01)
                print(f'ZC Trim Sweep code : {value} >')
                self.measure_values.append(self.PhxSy_Indcs_ZC_Values__Sweep___Current()) # get the frequency values from multimeter
                print(self.measure_values[-1])
        self.supply.setCurrent(channel=3,current=0)
        self.supply.outp_OFF(channel=3)
        self.PhxSy_Indcs_ZC_Limit__Check()
        # print(self.measure_values,self.trim_code)

    def PhxSy_Indcs_ZC_Values__Sweep___Current(self):
        # time.sleep(0.1)
        current=-0.35
        self.supply.setCurrent(channel=3,current=current)
        self.supply.outp_ON(channel=3)
        # self.scope.single_Trigger__RUN()
        # time.sleep(0.1)
        # while(self.scope.acquireState == True):
        self.scope.scopeTrigger_Acquire()
        while(self.scope.scopeAcquire_BUSY):
                time.sleep(0.01)
                self.supply.setCurrent(channel=3,current=current)
                current=current+0.001
                if current > 0.35 :
                    break
        # self.supply.setCurrent(channel=3,current=-0.1)
        return self.supply.getCurrent(channel=3)
    
    def PhxSy_Indcs_ZC_Limit__Check(self):
        # limits are not in percentage
        limit_max = 242*0.001
        limit_min = -242*0.001
        typical = 16*0.001
        
        error = []
        error_abs = []
        measure_values_abs=[]
        for i in self.measure_values:
            err = typical-abs(i)
            error_abs.append(abs(i))
            error.append(err)
            measure_values_abs.append(abs(i))

        error_min = min(error_abs)
        error_min__Index =error_abs.index(error_min)
        print('error min',error_min,'max',limit_max,'min',limit_min)
        if error_min > limit_min and  error_min < limit_max:
        # if error[error_min__Index] > limit_min and error[error_min__Index] < limit_max:
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
                "Trim":True
            }
            #reset the test driver 
            for register in self.registers:
                self.apis.write_register(register=register,write_value=0)
            # self.startup.IVM_Powerdown()
                
        else:
            self.trim_register_data.update({
                    "RegisterValue":self.trim_code[error_min__Index]
                })

            self.trim_results = {
                "Name" : self.DFT.get('Trimming_Name '),
                "Register":self.trim_register_data,
                "MeasureValue":self.measure_values[error_min__Index],
                "typical":typical,
                "MinError":error[error_min__Index],
                "Trim":False
            }
            #reset the test driver 
            for register in self.registers:
                self.apis.write_register(register=register,write_value=0)
            # self.startup.cirrus_PowerDown()
            # self.startup.IVM_Powerdown()
                
        self.scope.set_trigger__mode()
        self.scope.single_Trigger__RUN()


    def PhxSy_Indcs_ZC_results (self):
        return self.trim_results


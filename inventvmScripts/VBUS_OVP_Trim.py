import re , pandas as pd , time
from Franco_Test__APIs import FrancoAPIS
from startup import Startup
class vbus_Ovp_Trim:
    def __init__(self,dut,Instruments) -> None:
        # self.DFT = DFT
        self.dut = dut
        self.apis = FrancoAPIS(dut=dut)
        self.startup = Startup(dut=dut)
        self.supply = Instruments.supply
        self.scope = Instruments.scope
        time.sleep(5)
        self.registers = []
        self.trim_code = []
        self.trim_results={}


    def vbus_Ovp_Test__SetUp(self):
        self.supply.outp_OFF(channel=4)
        Instructions = [
            "Force__VDDIO__1.8V",
            "Force__VDD_SNS__4V",
            "Force__VBUS__5V",
            "Wait__SPI_READY__1'b1",
            "",
            "0x00000220[1]_0x1 \"IFET enable\"",
            "0x00000220[2]_0x1  \"IFET enable\"",
            "0x00000220[8]_0x1  \"HV_LDO enable\"",
            "0x00000220[29]_0x1  \"VDD_A enable\"",
            "0x00000220[28]_0x1  \"REFenable\"",
            "0x00000220[11]_0x1  \"VBUS OVP enable\"",
            "0x00000290[23:21]_0x6  \"Set TST1 output on  DTEST1\"",
            "",
            "Measure__Voltage__DTEST2",
            "ForceSweep__VBUS__20V__23V__20mV",
            "TrimSweep - 0x00000254[2:0] \"Select ds_aon_vbus_ovp_trim code which sets the vbus OVP threshold  as close as possible as 22V\"",
            "",
            "Calculate__MinError",
            "Trim - 0x00000254[12:8] ",
            ""
        ]
        # for Instruction in self.DFT.get("Instructions"):
        for Instruction in Instructions:
            if re.match(re.compile('0x'),Instruction):
                print(Instruction)
                reg_data = self.apis.parse_registerAddress_from_string(Instruction)
                if reg_data:
                    self.registers.append(reg_data)
                    self.apis.write_register(register=reg_data)
            if re.search(re.compile('TrimSweep'),Instruction):
                # input('Vbat ovp >')
                self.trim_register_data = self.apis.parse_trim_registerAddress_from_string(Instruction)
                self.vbus_Ovp_Values__Sweep()

    def vbus_Ovp_Values__Sweep(self):
        self.scope.set_HScale(scale='800E-9')
        self.scope.set_Channel__VScale(scale=0.2)
        self.scope.set_trigger__level(level=0.3)
        self.scope.set_trigger__mode(mode='NORM')
        self.scope.init_scopePosEdge__Trigger(channel='CH1')
        # self.scope.single_Trigger__RUN()
        self.scope.scopeTrigger_Acquire(channel='CH1')
        self.supply.setVoltage(channel=1,voltage=5)
        time.sleep(1)
        self.measure_values=[]
        if self.trim_register_data:
            for value in range(0,2**(self.trim_register_data.get('RegisterMSB') - self.trim_register_data.get('RegisterLSB') +1),1):
                self.apis.write_register(register=self.trim_register_data,write_value=value)
                self.trim_code.append(value)
                time.sleep(0.05)
                self.measure_values.append(self.vbus_Ovp_Values__Sweep___Voltage()) # get the frequency values from multimeter
        self.supply.setVoltage(channel=4,voltage=5)
        # self.supply.outp_OFF(channel=4)
        self.vbus_Ovp_Limit__Check()
        print(self.measure_values,self.trim_code)

    def vbus_Ovp_Values__Sweep___Voltage(self):
        # time.sleep(0.1)
        voltage=21
        self.supply.setVoltage(channel=4,voltage=voltage)
        self.supply.outp_ON(channel=4)
        self.scope.scopeTrigger_Acquire()
        # self.scope.single_Trigger__RUN()
        self.scope.set_Channel__VScale(scale=0.2)
        self.scope.set_trigger__level(level=0.3)
        time.sleep(0.1)
        # while(self.scope.acquireState == True):
        while(self.scope.scopeAcquire_BUSY):
                time.sleep(0.005)
                self.supply.setVoltage(channel=4,voltage=voltage)
                voltage=voltage+0.005
                if voltage > 23 :
                    break
        # self.supply.setVoltage(channel=4,voltage=-0.1)
        return self.supply.getVoltage(channel=4)
    
    def vbus_Ovp_Limit__Check(self):
        # limits are not in percentage
        limit_max = 22.3
        limit_min = 21.6
        typical = 22
        
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
                # "Name" : self.DFT.get('Trimming_Name '),
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

    def vbus_Ovp_results (self):
        return self.trim_results


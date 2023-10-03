import re 

class FrancoAPIS:
    def __init__(self,dut) -> None:
        self.dut = dut

    def write_register(self,register,write_value):
        reg_data = self.read_register(register=register)
        self.dut.write_register(register.get("RegisterAddress"), reg_data | write_value << register.get("RegisterLSB"))
        reg_data = self.read_register(register=register)
        print('RegAddress',hex(register.get("RegisterAddress")),'RegData',hex(reg_data))
    
    def read_register(self,register):
        return self.dut.read_register(register.get("RegisterAddress"))
    
    def parse_Instruction(self,instructions_raw):
        self.instructions=[]
        for instruction in instructions_raw:
            register_parse_data = self.parse_registerAddress(address=instruction)
            self.write_register(register=register_parse_data,write_value=register_parse_data.get("RegisterValue"))
    
    def parse_registerAddress(self,address:str):
        register = address
        Reg={}
        if re.match(re.compile("0x"),register):
            if re.search("_",register):
                register = register.split("_")
                register_value = int(register[1],16)
                if re.search(":",register[0]):
                    register = register[0].split(":")
                    register_LSB = int(register[1].strip("]"))
                    register = register[0].split("[")
                    register_address = int(register[0],16)
                    register_MSB = int(register[1])
                    Reg = {"RegisterAddress":register_address,"RegisterLSB":register_LSB,"RegisterMSB":register_MSB,"RegisterValue":register_value }
                else:
                     if "[" in register[0] :
                         register = register[0].split("[")
                         register_address = int(register[0],16)
                         register_LSB = int(register[1].strip("]"))
                         Reg = {"RegisterAddress":register_address,"RegisterLSB":register_LSB,"RegisterMSB":register_LSB,"RegisterValue":register_value }
            else:
                    if re.search(":",register):
                        register = register.split(":")
                        register_LSB = int(register[1].strip("]"))
                        register = register[0].split("[")
                        register_address = int(register[0],16)
                        register_MSB = int(register[1])
                        Reg = {"RegisterAddress":register_address,"RegisterLSB":register_LSB,"RegisterMSB":register_MSB,"RegisterValue":0 }
                    else:
                        if "[" in register :
                            register = register[0].split("[")
                            register_address = int(register[0],16)
                            register_LSB = int(register[1].strip("]"))
                            Reg = {"RegisterAddress":register_address,"RegisterLSB":register_LSB,"RegisterMSB":register_LSB,"RegisterValue":0 }
        return Reg
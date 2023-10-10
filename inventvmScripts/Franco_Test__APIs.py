import re 
import numpy as np 

class FrancoAPIS:
    def __init__(self,dut) -> None:
        self.dut = dut

    def write_register(self,register:dict,write_value=None):
        if write_value != None:
            reg_data = self.read_register(register=register)
            self.dut.write_register(register.get("RegisterAddress"), (reg_data & self.bit_mask(register=register) ) | write_value << register.get("RegisterLSB"))
            reg_data = self.read_register(register=register)
            print('RegAddress',hex(register.get("RegisterAddress")),'Value to Write',write_value,'RegData',hex(reg_data))
        elif register.get("RegisterValue"):
            reg_data = self.read_register(register=register)
            reg_write_value = (reg_data &  self.bit_mask(register=register) ) | register.get("RegisterValue") << register.get("RegisterLSB")
            self.dut.write_register(register.get("RegisterAddress"),(reg_data &  self.bit_mask(register=register) ) | register.get("RegisterValue") << register.get("RegisterLSB"))
            reg_data = self.read_register(register=register)
            print('RegAddress',hex(register.get("RegisterAddress")),'RegData',hex(reg_data))
            # print('RegAddress',hex(register.get("RegisterAddress")),'Value to Write',register.get("RegisterValue"),'Reg Writer value',hex(reg_write_value),'RegData after write',hex(reg_data))
        else:
            reg_data = self.read_register(register=register)
            self.dut.write_register(register.get("RegisterAddress"),(reg_data & self.bit_mask(register=register) ) | register.get("RegisterValue") << register.get("RegisterLSB"))
            reg_data = self.read_register(register=register)
            # print('!There is no Value to writing default 0')
            # print('RegAddress',hex(register.get("RegisterAddress")),'Value to Write',register.get("RegisterValue"),'RegData',hex(reg_data))
    
    def read_register(self,register):
        return self.dut.read_register(register.get("RegisterAddress"))
    
    def bit_mask(self,register):
        mask = ~(((1 << (register.get("RegisterMSB") - register.get("RegisterLSB") + 1)) -1) << register.get("RegisterLSB"))
        return mask
    
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

    def parse_registerAddress_from_string(self,Instruction):
        Reg=None
        if re.match(re.compile('0x'),Instruction):
            # there is comment in the instruction split it by ""
            if re.search(re.compile(' '),Instruction):
                regaddress = Instruction.split(' ')
                Reg = self.parse_registerAddress(regaddress[0])
            else :
                print('Register address did not found in string ')
        return Reg
    
    def parse_trim_registerAddress_from_string(self,Instruction):
            Reg= None
            if re.search(re.compile('TrimSweep'),Instruction):
                    # Seperate the Trim registre 
                    address = Instruction.split(' ') # Sperate the TrimSweep Instruction with space 
                    for register in address :
                        #seperate the Register 
                        if re.match(re.compile("0x"),register):
                            Reg = self.parse_registerAddress(register)
            else:
                print('!There is Trim register address')
            return Reg
import re

class TrimParse_Gen:

    def __init__(self) -> None:
        pass

    def register_parse(self,instructions):
        # Instruction Registers writing 
        for Instruction in instructions:
                if re.match(re.compile('0x'),Instruction):
                    # there is comment in the instruction split it by ""
                    if re.search(re.compile(' '),Instruction):
                        Cmds = Instruction.split(' ')
                        for cmd in Cmds:
                            if re.search(re.compile('_'),cmd):
                                    # ['0x00000290[23:21]', '0x4  ']
                                    RegData_Value = re.split('_',cmd)
                                    Reg = self.trim_RegisterAddress__Parse(address=RegData_Value[0])
                                    self.trim_Register__Documenting(Reg=Reg)
                                    print('Register Value : ',RegData_Value[1])
                    else :
                        print('Register address did not found ')
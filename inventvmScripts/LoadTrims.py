
import json 
from Franco_Test__APIs import FrancoAPIS

class LoadTrims:

    def __init__(self,dut,path:str,chipid) -> None:
        self.dut = dut
        self.apis = FrancoAPIS(dut=dut)
        self.chipid = chipid
        with open(path, 'r', encoding='utf-8') as f:
            self.trimmedData = json.load(f)
        # print(self.trimmedData)
        # self.loadTrims()
    def loadTrims(self):
        print('Loading Trimming Values ...')
        for reg_data in self.trimmedData.get(str(self.chipid)):
            # print(reg_data)
            self.apis.write_register(register=reg_data.get('Register'))
        print('Done.....!')



if __name__ == '__main__':
    LoadTrims(dut=None)
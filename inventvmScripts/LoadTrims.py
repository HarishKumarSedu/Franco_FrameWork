
import json 
from Franco_Test__APIs import FrancoAPIS

class LoadTrims:

    def __init__(self,dut) -> None:
        self.dut = dut
        self.apis = FrancoAPIS(dut=dut)
        with open('json/TrimmingResults_100_99.json', 'r', encoding='utf-8') as f:
            self.trimmedData = json.load(f)
        # self.loadTrims()
    def loadTrims(self):
        for reg_data in self.trimmedData.get("100"):
            self.apis.write_register(register=reg_data.get('Register'))


if __name__ == '__main__':
    LoadTrims(dut=None)
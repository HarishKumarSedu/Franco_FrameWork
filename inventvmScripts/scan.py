
import pandas as pd 

class Scan:

    def __init__(self) -> None:
        self.regmap = pd.read_csv('chip_validation_regs.csv')
        self.franco_default_regdump = pd.read_csv('franco_default_dump.csv')

        for i in range(0,len(self.regmap)+1):
            for j in range(0,len(self.franco_default_regdump)+1):
                if (self.regmap['FIELD NAME'].get(i) == self.franco_default_regdump['FIELD NAME'].get(j)):
                    if self.regmap['DEFAULT'].get(i) != None or \
                        self.franco_default_regdump['DEFAULT'].get(j)!= None:
                        if int(self.regmap['DEFAULT'].get(i),16) != int(self.franco_default_regdump['DEFAULT'].get(j),16):
                            print(self.franco_default_regdump['FIELD NAME'].get(j),'Fail')
                            print(self.regmap['DEFAULT'].get(i),self.franco_default_regdump['DEFAULT'].get(j))
                        else:
                            print(self.franco_default_regdump['FIELD NAME'].get(j),'Pass')
                            pass


if __name__ == '__main__':
    Scan()
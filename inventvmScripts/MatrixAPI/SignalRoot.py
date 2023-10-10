
import json 

class SignalRoot:

    def __init__(self) -> None:
        self.signalPath = {}
        # self.local_1path()
        # self.local_2path()
        # self.local_3path()
        self.local_4path()
        self.dumpData()

    def local_1path(self):

        bridges = ['X','Y','Z','K','J','W','U','O','P','N']

        signals = ['A','B','C','D','E','F','G','H','I','L']
        signalpath = dict(zip(bridges,signals))

        for bridge , signal in signalpath.items():

            for i in range(1,5):
                for j in range(1,6):
                    # print(f'{bridge}{i} : {signal}{j}')
                    self.signalPath.update({f'{bridge}{i}' : f'{signal}{j}'})

            print(30*'~')
                
    def local_2path(self):

        bridges = ['X','Z','J','U']

        signals = ['Z','J','U','N']
        signalpath = dict(zip(bridges,signals))

        for bridge , signal in signalpath.items():

            for i in range(1,5):
                # print(f'{bridge}{i} : {signal}{i}')
                self.signalPath.update({f'{bridge}{i}' : f'{signal}{i}'})
            print(30*'~')
                
    def local_3path(self):

        bridges = ['X','J',]

        signals = ['J','N']
        signalpath = dict(zip(bridges,signals))

        for bridge , signal in signalpath.items():

            for i in range(1,5):
                # print(f'{bridge}{i} : {signal}{i}')
                self.signalPath.update({f'{bridge}{i}' : f'{signal}{i}'})
            print(30*'~')
                
    def local_4path(self):

        bridges = ['X','Z','Z']

        signals = ['U','U','N']
        signalpath = dict(zip(bridges,signals))

        for bridge , signal in signalpath.items():

            for i in range(1,5):
                # print(f'{bridge}{i} : {signal}{i}')
                self.signalPath.update({f'{bridge}{i}' : f'{signal}{i}'})
            print(30*'~')
    

    def dumpData(self):
            with open('SignalPath4.json', 'w', encoding='utf-8') as f:
                json.dump(self.signalPath, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':

    path = SignalRoot()
    # path.local_1path()
    # path.local_2path()
    # path.local_3path()
    # path.local_4path()
from Instruments_API import Instruments
from writeExcel import writeInExcel
from startup import Startup
from time import sleep

class InputCurrSense:

    def __init__(self) -> None:
        self.supply = Instruments().supply
        self.scope = Instruments().scope
        # self.InputCurr_Step()
        self.Insput_CurrentSweep_dynamic()

    def InputCurr_Step(self):
        self.scope.set_HScale(scale='20E-3')
        self.scope.set_Channel__VScale(scale=0.2)
        self.scope.set_trigger__level(level=0.1)
        self.scope.set_trigger__mode(mode='NORM')
        self.scope.init_scopePosEdge__Trigger()
        # for i in range(1,8,1):
        for i in range(1,8,1):
            self.supply.setCurrent(channel=1,current=0)
            self.scope.scopeTrigger_Acquire()
            while(self.scope.scopeAcquire_BUSY):
                sleep(0.01)
                self.supply.setCurrent(channel=1,current=0)
                sleep(0.01)
                self.supply.setCurrent(channel=1,current=-i)
            # sleep(0.01)
            # self.supply.setCurrent(channel=1,current=0)
            # sleep(0.1)
            print(self.scope.Meas_Amp())
            sleep(0.1)
            # print(self.scope.Meas_Amp(Meas='MEAS2'))
    
    def Insput_CurrentSweep_dynamic(self,sheet='Device3_85C_ibus_sweep_3.3A'):
        curr = 0
        self.supply.setCurrent(channel=1,current=-0.1)
        ibat_set  = []
        ibus_set = []
        external_ibus_cal = []
        external_ibus_voltage = []
        ibus_sns_ibus_cal = []
        ibus_sns_voltage = []
        ibus_sns_voltage = []
        error=[]
        try:
            while self.supply.getCurrent(channel=4) < 3.310:
                curr=curr+0.1
                self.supply.setCurrent(channel=1,current=-curr)
                sleep(1)
                ibat_set.append(abs(self.supply.getCurrent(channel=1)))
                ibus_set.append(self.supply.getCurrent(channel=4))
                # external_ibus_voltage.append(self.scope.Meas_Mean(Meas='MEAS2')- 3.5e-3)
                # external_ibus_cal.append(external_ibus_voltage[-1]/(10*0.025))
                ibus_sns_voltage.append(self.scope.Meas_Mean(Meas='MEAS1'))
                ibus_sns_ibus_cal.append((ibus_sns_voltage[-1]*2976)/(500))
                err = ((ibus_sns_ibus_cal[-1]-ibus_set[-1])/ibus_set[-1])*100
                if abs(err) > 2 and len(error) > 5:
                    print('error',err)
                    error.append(sum(error[-4:])/(len(error)-5))
                else:
                    error.append(err)

                # input('Single >>>>>>')
                print('ibus Current in A',self.supply.getCurrent(channel=4) )
            writeInExcel(sheet=sheet,filename='Input_CurrentSense\Input_CurrentSense_Char.xlsx',ibat_set=ibat_set,ibus_set=ibus_set,ibus_sns_voltage=ibus_sns_voltage,ibus_sns_ibus_cal=ibus_sns_ibus_cal,error=error)
            while curr >= 0:
                curr = curr - 0.1
                self.supply.setCurrent(channel=1,current=-curr)
                sleep(0.1)
            self.supply.setCurrent(channel=1,current=0)
        except:
            while curr <= 0:
                curr = curr - 0.1
                self.supply.setCurrent(channel=1,current=-curr)
                sleep(0.1)



if __name__ =='__main__':
    InputCurrSense()
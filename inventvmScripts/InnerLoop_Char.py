from Instruments_API import Instruments
from writeExcel import writeInExcel
from startup import Startup
from time import sleep

class InnerLoop:

    def __init__(self) -> None:
        self.supply = Instruments().supply
        self.scope = Instruments().scope
        # self.InputCurr_Step()
        self.Inductor_OCP_dynamic()

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
    
    def Insput_CurrentSweep_dynamic(self,sheet='Device1_5C_OCP'):
      
            writeInExcel(sheet=sheet,filename='Input_CurrentSense\Input_CurrentSense_Char.xlsx',ibat_set=ibat_set,ibus_set=ibus_set,ibus_sns_voltage=ibus_sns_voltage,ibus_sns_ibus_cal=ibus_sns_ibus_cal,error=error)
          





if __name__ =='__main__':
    pass 

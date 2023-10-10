from pcf8547 import PCF8547,PCF8547Constants
import time 
class RelayMatrix1:

    def __init__(self,slaveAddress = 0x20) -> None:
        """
            Relay Matrix1 Address : 0x20 
                
                Common Signal ( Relay Pole ) - Relay Name - NO ( Normally Open Signal )
            ----------------------------------------------------------------------------------
                Multimeter ( Vp+ )           -   P0       - VDDA
                Multimeter ( Vp+ )           -   P1       - TEST1
                Multimeter ( Vp+ )           -   P2       - VDD_D
                Multimeter ( Vp+ )           -   P3       - DTEST2   
                Multimeter ( Vp+ )           -   P4       - PH13_IL_VREF      
                Multimeter ( Vp+ )           -   P5       - PH24_IL_VREF           
                Multimeter ( Vp+ )           -   P6       - DTEST1           
                Multimeter ( Vp+ )           -   P7       - GND           
        """
        self.pcf = PCF8547(slaveAddress=slaveAddress)

    def VDD_D(self,Status=False):
        if Status:
            self.pcf.setPort(PCF8547Constants.P0.value)
        else:
            self.pcf.resetPort(PCF8547Constants.P0.value)
    def VDDA(self,Status=False):
        if Status:
            self.pcf.setPort(PCF8547Constants.P1.value)
        else:
            self.pcf.resetPort(PCF8547Constants.P1.value)
    def TEST1_1(self,Status=False):
        if Status:
            self.pcf.setPort(PCF8547Constants.P2.value)
        else:
            self.pcf.resetPort(PCF8547Constants.P2.value)
    def TEST1_2(self,Status=False):
        if Status:
            self.pcf.setPort(PCF8547Constants.P3.value)
        else:
            self.pcf.resetPort(PCF8547Constants.P3.value)
    def TEST2(self,Status=False):
        if Status:
            self.pcf.setPort(PCF8547Constants.P4.value)
        else:
            self.pcf.resetPort(PCF8547Constants.P4.value)
    def GND(self,Status=False):
        if Status:
            self.pcf.setPort(PCF8547Constants.P7.value)
        else:
            self.pcf.resetPort(PCF8547Constants.P7.value)
    
    def reset(self):
        self.pcf.reset()

if __name__ == '__main__':
    matrix1 = RelayMatrix1()
    matrix1.reset()
    time.sleep(0.1)
    matrix1.GND(Status=True)
    time.sleep(0.1)
    matrix1.VDD_D(Status=True)
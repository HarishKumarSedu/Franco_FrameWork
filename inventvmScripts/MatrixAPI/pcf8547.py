
from enum import Enum
from PyMCP2221A import PyMCP2221A
from time import sleep

class PCF8547Constants(Enum):
    # Invert all of the values becuase the relay board is actuvatedfor the active low
    Reset = 0xFF
    P0 = 0x01
    P1 = 0x02
    P2 = 0x04
    P3 = 0x08
    P4 = 0x10
    P5 = 0x20
    P6 = 0x40
    P7 = 0x80
    SetAll = 0x00

class PCF8547:
    
    def __init__(self,slaveAddress=0x20) -> None:
        self.slaveAddress = slaveAddress

        self.mcp2221A = PyMCP2221A.PyMCP2221A()
        self.mcp2221A.Reset()
        self.mcp2221A = PyMCP2221A.PyMCP2221A()
        self.mcp2221A.I2C_Init()

        self.reset()

    def setPort(self,Port):
        Port = (~Port &  self.mcp2221A.I2C_Read(self.slaveAddress, 1)[0])
        self.mcp2221A.I2C_Write(self.slaveAddress,[Port])
      
    def resetPort(self,Port):  
        Port = (Port |  self.mcp2221A.I2C_Read(self.slaveAddress, 1)[0])
        print(Port)
        self.mcp2221A.I2C_Write(self.slaveAddress,[Port])
      

    def reset(self):
        Port = 0xFF
        self.mcp2221A.I2C_Write(self.slaveAddress,[Port])

if __name__ == '__main__':

    pcf8547 = PCF8547()

    pcf8547.setPort(PCF8547Constants.P0.value)
    sleep(0.5)
    pcf8547.setPort(PCF8547Constants.P1.value)
    sleep(0.5)
    pcf8547.resetPort(PCF8547Constants.P0.value)
    
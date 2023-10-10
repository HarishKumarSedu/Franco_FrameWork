
from PCA9505AddrCons import PCA9505AddrCons
from PinMapping import Signals
from MCP import MCP 
import time 

class PCA9505:

    def __init__(self) -> None:
        self.PCAConstants = PCA9505AddrCons()
        self.mcp = MCP()
        self.signal = Signals()

        self.SlaveAddress = 0x20
        self.Slave = {
                        '0x20' : 0x20,
                        '0x21' : 0x21,
                        '0x22' : 0x22,
                        '0x23' : 0x23,
                        '0x24' : 0x24,
                        '0x25' : 0x25,
                        '0x26' : 0x26,
                        '0x27' : 0x27,
        }

        ## Reset all the Salves 
        for key, address in self.Slave.items():
            self.mcp.mcpWrite(SlaveAddress=address,data=[self.PCAConstants.PCA9505_OP0,self.PCAConstants.PCA9505_ALLOP_RESET])
            self.mcp.mcpWrite(SlaveAddress=address,data=[self.PCAConstants.PCA9505_OP1,self.PCAConstants.PCA9505_ALLOP_RESET])
            self.mcp.mcpWrite(SlaveAddress=address,data=[self.PCAConstants.PCA9505_OP2,self.PCAConstants.PCA9505_ALLOP_RESET])
            self.mcp.mcpWrite(SlaveAddress=address,data=[self.PCAConstants.PCA9505_OP3,self.PCAConstants.PCA9505_ALLOP_RESET])
            self.mcp.mcpWrite(SlaveAddress=address,data=[self.PCAConstants.PCA9505_OP4,self.PCAConstants.PCA9505_ALLOP_RESET])


    def enableX1_B4(self,SlaveAddress =0x20):  
        portData_0 = self.mcp.mcpRead(SlaveAddress=self.Slave.get('0x26'),data=[self.PCAConstants.PCA9505_OP0])[0] + self.PCAConstants.PCA9505_OP0_D0_2SMASK   # To Enable the switch  add 2SMask 
        
        self.mcp.mcpWrite(SlaveAddress=self.Slave.get('0x26'),data=[self.PCAConstants.PCA9505_OP0,portData_0])
        # time.sleep(2)


        portData_0 = self.mcp.mcpRead(SlaveAddress=self.Slave.get('0x20'),data=[self.PCAConstants.PCA9505_OP2])[0] + self.PCAConstants.PCA9505_OP2_D7_2SMASK   # To Enable the switch  add 2SMask 
        self.mcp.mcpWrite(SlaveAddress=self.Slave.get('0x20'),data=[self.PCAConstants.PCA9505_OP2,portData_0])
        time.sleep(2)

        portData_0 = self.mcp.mcpRead(SlaveAddress=self.Slave.get('0x26'),data=[self.PCAConstants.PCA9505_OP0])[0] + self.PCAConstants.PCA9505_OP0_D0_MASK  # To disable the switch add Mask
        self.mcp.mcpWrite(SlaveAddress=self.Slave.get('0x26'),data=[self.PCAConstants.PCA9505_OP0,portData_0])
        portData_0 = self.mcp.mcpRead(SlaveAddress=self.Slave.get('0x20'),data=[self.PCAConstants.PCA9505_OP2])[0] + self.PCAConstants.PCA9505_OP2_D7_MASK   # To Enable the switch  add 2SMask 
        self.mcp.mcpWrite(SlaveAddress=self.Slave.get('0x20'),data=[self.PCAConstants.PCA9505_OP2,portData_0])


    def enable_VDD_X1_B4_2(self):
        #################### The Signal first arguments are 
        ####################? 0 -----> Device address 
        ####################? 1 -----> Register address 
        ####################? 2 -----> SET/RESET MASK Values 
        portData = self.mcp.mcpRead(SlaveAddress=self.signal.XY1_SET[0],data=[self.signal.XY1_SET[1]])[0] + self.signal.XY1_SET[2]   # To Enable the switch  add 2SMask 
        self.mcp.mcpWrite(SlaveAddress=self.signal.XY1_SET[0],data=[self.signal.XY1_SET[1],portData])

        portData = self.mcp.mcpRead(SlaveAddress=self.signal.Y1B4_SET[0],data=[self.signal.Y1B4_SET[1]])[0] + self.signal.Y1B4_SET[2]   # To Enable the switch  add 2SMask 
        self.mcp.mcpWrite(SlaveAddress=self.signal.Y1B4_SET[0],data=[self.signal.Y1B4_SET[1],portData])

        # time.sleep(5)

        # portData = self.mcp.mcpRead(SlaveAddress=self.signal.XY1_RESET[0],data=[self.signal.XY1_RESET[1]])[0] + self.signal.XY1_RESET[2]   # To Enable the switch  add 2SMask 
        # self.mcp.mcpWrite(SlaveAddress=self.signal.XY1_RESET[0],data=[self.signal.XY1_RESET[1],portData])

        # portData = self.mcp.mcpRead(SlaveAddress=self.signal.Y1B4_RESET[0],data=[self.signal.Y1B4_RESET[1]])[0] + self.signal.Y1B4_RESET[2]   # To Enable the switch  add 2SMask 
        # self.mcp.mcpWrite(SlaveAddress=self.signal.Y1B4_RESET[0],data=[self.signal.Y1B4_RESET[1],portData])

    def enable_GND_X1_B4_2(self):
        portData = self.mcp.mcpRead(SlaveAddress=self.signal.X2A2_SET[0],data=[self.signal.X2A2_SET[1]])[0] + self.signal.X2A2_SET[2]   # To Enable the switch  add 2SMask 
        self.mcp.mcpWrite(SlaveAddress=self.signal.X2A2_SET[0],data=[self.signal.X2A2_SET[1],portData])

if __name__ == '__main__':
    pca9505 = PCA9505()
    # pca9505.enableX1_B4()
    pca9505.enable_VDD_X1_B4_2()
    pca9505.enable_GND_X1_B4_2()

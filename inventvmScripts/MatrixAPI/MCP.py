from PyMCP2221A import PyMCP2221A


class MCP:

    def __init__(self) -> None:
        self.mcp = PyMCP2221A.PyMCP2221A()
        self.mcp.Reset()
        self.mcp = PyMCP2221A.PyMCP2221A()
        self.mcp.I2C_Init()
        
    def mcpWrite(self,SlaveAddress,data:list):
        # slaveAdddress = data.pop(0)
        # senddata = data
        # senddata = []
        # for i in range(0,len(data)):
        #     senddata.append(data[i])
        # print(senddata)
        self.mcp.I2C_Write(SlaveAddress,data)


    def mcpRead(self,SlaveAddress,data:list,Nobytes=1):
        # slaveAddress = data[0]
        self.mcpWrite(SlaveAddress=SlaveAddress,data=data)
        data = self.mcp.I2C_Read(SlaveAddress, Nobytes)

        return data

if __name__ == '__main__':

    mcp=MCP()
    mcp.mcpWrite([00])
    print(mcp.mcpRead(0,Nobytes=10))

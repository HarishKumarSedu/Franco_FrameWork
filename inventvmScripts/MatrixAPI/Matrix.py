

# --> I2C Slave address 
# Slave found. 8 bit address = 0x40; 7 bit address = 0x20 Write
# Slave found. 8 bit address = 0x41; 7 bit address = 0x20 Read
# Slave found. 8 bit address = 0x42; 7 bit address = 0x21 Write
# Slave found. 8 bit address = 0x43; 7 bit address = 0x21 Read
# Slave found. 8 bit address = 0x44; 7 bit address = 0x22 Write
# Slave found. 8 bit address = 0x45; 7 bit address = 0x22 Read
# Slave found. 8 bit address = 0x46; 7 bit address = 0x23 Write
# Slave found. 8 bit address = 0x47; 7 bit address = 0x23 Read
# Slave found. 8 bit address = 0x48; 7 bit address = 0x24 Write
# Slave found. 8 bit address = 0x49; 7 bit address = 0x24 Read
# Slave found. 8 bit address = 0x4A; 7 bit address = 0x25 Write
# Slave found. 8 bit address = 0x4B; 7 bit address = 0x25 Read
# Slave found. 8 bit address = 0x4C; 7 bit address = 0x26 Write
# Slave found. 8 bit address = 0x4D; 7 bit address = 0x26 Read
# Slave found. 8 bit address = 0x4E; 7 bit address = 0x27 Write
# Slave found. 8 bit address = 0x4F; 7 bit address = 0x27 Read

class Matrix :

    def __init__(self) -> None:
        
        # Switch matrix Board IC address .................
        self.U300Address = 0x20
        self.U301Address = 0x21
        self.U302Address = 0x22
        self.U303Address = 0x23


        self.U400Address = 0x24
        self.U401Address = 0x25
        self.U402Address = 0x26
        self.U403Address = 0x27
 

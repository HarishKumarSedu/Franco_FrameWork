


class PCA9505AddrCons:
    def __init__(self) -> None:
        self.PCA9505_AI_ON		    = 0x80
        self.PCA9505_AI_OFF		    = 0x00

        # Address .......................
        self.PCA9505_BASE_ADDRESS   = 0x20
        self.PCA9505_A0			    = 0x01
        self.PCA9505_A1			    = 0x02
        self.PCA9505_A2			    = 0x04

        # Input Registers......................
        self.PCA9505_IP			    = 0x00
        self.PCA9505_IP0	        = 0x00
        self.PCA9505_IP1	        = 0x01
        self.PCA9505_IP2	        = 0x02
        self.PCA9505_IP3	        = 0x03
        self.PCA9505_IP4	        = 0x04

        # Output Register Address ..............
        self.PCA9505_ALLOP_RESET    = 0xFF
        self.PCA9505_ALLOP_SET      = 0x00
        self.PCA9505_OP			    = 0x08
        self.PCA9505_OP0	        = 0x08
        self.PCA9505_OP1	        = 0x09
        self.PCA9505_OP2	        = 0x0A
        self.PCA9505_OP3	        = 0x0B
        self.PCA9505_OP4	        = 0x0C
        self.PCA9505_PI			    = 0x10
        self.PCA9505_PI0	        = 0x10
        self.PCA9505_PI1	        = 0x11
        self.PCA9505_PI2	        = 0x12
        self.PCA9505_PI3	        = 0x13
        self.PCA9505_PI4	        = 0x14
        self.PCA9505_IOC	        = 0x18
        self.PCA9505_IOC0		    = 0x18
        self.PCA9505_IOC1		    = 0x19
        self.PCA9505_IOC2		    = 0x1A
        self.PCA9505_IOC3		    = 0x1B
        self.PCA9505_IOC4		    = 0x1C
        self.PCA9505_MSK	        = 0x20
        self.PCA9505_MSK0		    = 0x20
        self.PCA9505_MSK1		    = 0x21
        self.PCA9505_MSK2		    = 0x22
        self.PCA9505_MSK3		    = 0x23
        self.PCA9505_MSK4		    = 0x24


        # Register output enable ..............
        self.PCA9505_OP0_D0_MASK    = 0x01
        self.PCA9505_OP0_D1_MASK    = 0x02
        self.PCA9505_OP0_D2_MASK    = 0x04
        self.PCA9505_OP0_D3_MASK    = 0x08
        self.PCA9505_OP0_D4_MASK    = 0x10
        self.PCA9505_OP0_D5_MASK    = 0x20
        self.PCA9505_OP0_D6_MASK    = 0x40
        self.PCA9505_OP0_D7_MASK    = 0x80
        self.PCA9505_OP1_D0_MASK    = 0x01
        self.PCA9505_OP1_D1_MASK    = 0x02
        self.PCA9505_OP1_D2_MASK    = 0x04
        self.PCA9505_OP1_D3_MASK    = 0x08
        self.PCA9505_OP1_D4_MASK    = 0x10
        self.PCA9505_OP1_D5_MASK    = 0x20
        self.PCA9505_OP1_D6_MASK    = 0x40
        self.PCA9505_OP1_D7_MASK    = 0x80
        self.PCA9505_OP2_D0_MASK    = 0x01
        self.PCA9505_OP2_D1_MASK    = 0x02
        self.PCA9505_OP2_D2_MASK    = 0x04
        self.PCA9505_OP2_D3_MASK    = 0x08
        self.PCA9505_OP2_D4_MASK    = 0x10
        self.PCA9505_OP2_D5_MASK    = 0x20
        self.PCA9505_OP2_D6_MASK    = 0x40
        self.PCA9505_OP2_D7_MASK    = 0x80
        self.PCA9505_OP3_D0_MASK    = 0x01
        self.PCA9505_OP3_D1_MASK    = 0x02
        self.PCA9505_OP3_D2_MASK    = 0x04
        self.PCA9505_OP3_D3_MASK    = 0x08
        self.PCA9505_OP3_D4_MASK    = 0x10
        self.PCA9505_OP3_D5_MASK    = 0x20
        self.PCA9505_OP3_D6_MASK    = 0x40
        self.PCA9505_OP3_D7_MASK    = 0x80
        self.PCA9505_OP4_D0_MASK    = 0x01
        self.PCA9505_OP4_D1_MASK    = 0x02
        self.PCA9505_OP4_D2_MASK    = 0x04
        self.PCA9505_OP4_D3_MASK    = 0x08
        self.PCA9505_OP4_D4_MASK    = 0x10
        self.PCA9505_OP4_D5_MASK    = 0x20
        self.PCA9505_OP4_D6_MASK    = 0x40
        self.PCA9505_OP4_D7_MASK    = 0x80

        self.PCA9505_OP0_D0_2SMASK    = ~0x01 + 1
        self.PCA9505_OP0_D1_2SMASK    = ~0x02 + 1
        self.PCA9505_OP0_D2_2SMASK    = ~0x04 + 1
        self.PCA9505_OP0_D3_2SMASK    = ~0x08 + 1
        self.PCA9505_OP0_D4_2SMASK    = ~0x10 + 1
        self.PCA9505_OP0_D5_2SMASK    = ~0x20 + 1
        self.PCA9505_OP0_D6_2SMASK    = ~0x40 + 1
        self.PCA9505_OP0_D7_2SMASK    = ~0x80 + 1
        self.PCA9505_OP1_D0_2SMASK    = ~0x01 + 1
        self.PCA9505_OP1_D1_2SMASK    = ~0x02 + 1
        self.PCA9505_OP1_D2_2SMASK    = ~0x04 + 1
        self.PCA9505_OP1_D3_2SMASK    = ~0x08 + 1
        self.PCA9505_OP1_D4_2SMASK    = ~0x10 + 1
        self.PCA9505_OP1_D5_2SMASK    = ~0x20 + 1
        self.PCA9505_OP1_D6_2SMASK    = ~0x40 + 1
        self.PCA9505_OP1_D7_2SMASK    = ~0x80 + 1
        self.PCA9505_OP2_D0_2SMASK    = ~0x01 + 1
        self.PCA9505_OP2_D1_2SMASK    = ~0x02 + 1
        self.PCA9505_OP2_D2_2SMASK    = ~0x04 + 1
        self.PCA9505_OP2_D3_2SMASK    = ~0x08 + 1
        self.PCA9505_OP2_D4_2SMASK    = ~0x10 + 1
        self.PCA9505_OP2_D5_2SMASK    = ~0x20 + 1
        self.PCA9505_OP2_D6_2SMASK    = ~0x40 + 1
        self.PCA9505_OP2_D7_2SMASK    = ~0x80 + 1
        self.PCA9505_OP3_D0_2SMASK    = ~0x01 + 1
        self.PCA9505_OP3_D1_2SMASK    = ~0x02 + 1
        self.PCA9505_OP3_D2_2SMASK    = ~0x04 + 1
        self.PCA9505_OP3_D3_2SMASK    = ~0x08 + 1
        self.PCA9505_OP3_D4_2SMASK    = ~0x10 + 1
        self.PCA9505_OP3_D5_2SMASK    = ~0x20 + 1
        self.PCA9505_OP3_D6_2SMASK    = ~0x40 + 1
        self.PCA9505_OP3_D7_2SMASK    = ~0x80 + 1
        self.PCA9505_OP4_D0_2SMASK    = ~0x01 + 1
        self.PCA9505_OP4_D1_2SMASK    = ~0x02 + 1
        self.PCA9505_OP4_D2_2SMASK    = ~0x04 + 1
        self.PCA9505_OP4_D3_2SMASK    = ~0x08 + 1
        self.PCA9505_OP4_D4_2SMASK    = ~0x10 + 1
        self.PCA9505_OP4_D5_2SMASK    = ~0x20 + 1
        self.PCA9505_OP4_D6_2SMASK    = ~0x40 + 1
        self.PCA9505_OP4_D7_2SMASK    = ~0x80 + 1

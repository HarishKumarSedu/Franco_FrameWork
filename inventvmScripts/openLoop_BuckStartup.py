
from FrancoTest import test_station,dut
class OpenLoop_Buck:

    def __inti___(self,dut):
        self.dut = dut 

    def startup(self):
        self.dut.OUTERLOOP_CNTL0: 0x1c20c80
        self.dut.OUTERLOOP_CNTL1: 0x1eb0000
        self.dut.OUTERLOOP_CNTL2: 0x2032
        self.dut.OUTERLOOP_CNTL3: 0x0
        self.dut.INNERLOOP_CFG: 0x7
        self.dut.POWERSTATE_CFG: 0x3000000
        self.dut.STATUS: 0x703
        self.dut.DC_LIMITER: 0x12
        self.dut.ICMD_VALUE: 0x10cc
        self.dut.D_VALUE: 0x7b7a7bf
        self.dut.ALPHA_VALUE: 0x0
        self.dut.VBAT_ADC_RESULT: 0xde6
        self.dut.IBAT_ADC_RESULT: 0xffca
        self.dut.VBUS_ADC_RESULT: 0x1cd5
        self.dut.IBUS_ADC_RESULT: 0xd
        self.dut.PH1_IL_ADC_RESULT: 0xfffda800
        self.dut.PH1_VFLY_ADC_RESULT: 0x3ddee00
        self.dut.PH2_IL_ADC_RESULT: 0xfffad800
        self.dut.PH2_VFLY_ADC_RESULT: 0x3312600
        self.dut.PH3_IL_ADC_RESULT: 0x87000
        self.dut.PH3_VFLY_ADC_RESULT: 0x32e7a00
        self.dut.PH4_IL_ADC_RESULT: 0x0
        self.dut.PH4_VFLY_ADC_RESULT: 0x3360c00
        self.dut.TEST_IBAT_PARAMS: 0x102011a
        self.dut.TEST_VBAT_BUCK_PARAMS: 0x102011a
        self.dut.TEST_VBAT_BST_PARAMS: 0x102011a
        self.dut.TEST_IBUS_PARAMS: 0x102010a
        self.dut.TEST_VBUS_BUCK_PARAMS: 0x102010a
        self.dut.TEST_VBUS_BST_PARAMS: 0x102010a
        self.dut.TEST_INNER_LOOP_PH_MGMT: 0x10001
        self.dut.TEST_INNER_LOOP_DCM: 0x105
        self.dut.TEST_INNER_LOOP_IL: 0x1010a
        self.dut.TEST_INNER_LOOP_MODULATOR: 0x1
        self.dut.TEST_INNER_LOOP_VFLY: 0x200000a
        self.dut.TEST_ICMD_OVR_PARAMS: 0xa660000
        self.dut.TEST_DREF_OVERRIDE_EN: 0x1
        # self.dut.TEST_DREF_OVERRIDE_SET: 0x7d70a3 # for 49% duty cycle 
        self.dut.TEST_DREF_OVERRIDE_SET: 0x800000 # 50% duty cycle 
        self.dut.TEST_ALPHA_OVERRIDE_EN: 0x1
        self.dut.TEST_ALPHA_OVERRIDE_SET: 0x0
        self.dut.GAIN_CONFIG1: 0x78007200
        self.dut.GAIN_CONFIG2: 0x4300c78
        self.dut.GAIN_CONFIG3: 0x7fd0401
        self.dut.IVM_TC_DTEST_CONFIG: 0x0

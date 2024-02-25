"""
File: example_inventm_test_script.py
Description: This script runs a test to confirm the AudioHub is connected and Performs basic Register Read/Write on the DUT.

Functions:
    build_test_station(file_path)
        - Builds the CL Test Station from a YAML definition in the file_path
        - Returns:
            - handle to the CL Test Station object

    teardown_test_station(test_station
        - Cleans up resources for the test. Call this at the end of the test.


Usage:
    - Confirm the AudioHub handle is present and correct in the configuration file:
        C:\\validation\\Projects\\Franco\\python\\franco_val\\configs\\project_configs\\inventvm_config.yml
    - Confirm the Vivado Hardware Serial Number is set in the field DUT_FPGA_JTAG_ID
        C:\\validation\\Projects\\Franco\\python\\franco_val\\env\\franco_val_inventm.env
    - Set the terminal workspace to `C:\\validation\\Projects\\Franco\\python\\franco_val`
    - Activate the virtual environment in venv
    - Run the script from a terminal like `python .\\inventm\\example_inventm_test_script.py`

Note:
    - This script requires Python 3.7.9

Example:
    $ cd C:\validation\Projects\Franco\python\franco_val
    $ .\venv\Scripts\Activate.ps1
    $ python python .\inventm\example_inventm_test_script.py.py
"""
from socket import gethostname
from dotenv import load_dotenv
import threading
import time
import os
import sys
import json

from ph1_indcs import ph1_indcs
from startup import Startup
from Trimming import Trim
from LoadTrims import LoadTrims
# from Indcs_debug import Inducs_Debug
# from quick_Check import QuickCheck
from Instruments_API import Instruments
from efficiency1 import Efficiency
from AON_Charecterization import AONChar
from InnerLoop_Char import InnerLoop
from input_CurrentSense_Char import InputCurrSense
from cfly_char import CflyChar
from readCurr import Startup_read_curr

load_dotenv(r'C:\validation\Projects\Franco\python\franco_val\env\franco_val_inventm.env')
load_dotenv(
    r'C:\validation\Projects\Franco\python\franco_val\env\station\\' + f'franco_val_{gethostname().upper()}.env')
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from ts_support import build_test_station, start_gui, teardown_test_station

ts_cfg_file = os.path.expandvars(r'$PROJECT_ROOT\configs\project_configs\inventvm_config.yml')
test_station = build_test_station(ts_cfg_file)
dut = test_station.eeb.franco

gui_thread = threading.Thread(target=start_gui, name="Register Map GUI", args=(test_station, {}), daemon=True)
gui_thread.start()
############ Confirm AudioHub ##########

print(test_station.audio_hub.ping())

############ DUT BringUp ##########
test_station.pins.mb_pwr_en.output = 1

# test_station.pins.fpga_reset.output = 0
# test_station.pins.fpga_reset.output = 1

# test_station.pins.system_adcs_reset.output = 0
# test_station.pins.system_adcs_reset.output = 1

# test_station.pins.franco_tc_reset.output = 0
# test_station.pins.franco_tc_reset.output = 1
dut.reset()
time.sleep(0.01)

test_station.eeb.config_dacs()
dut.config_ADCs()
############ Test Code ##########
# TODO
# The command to quit the 'console'
quit_cmd = "quit"
input_cmd = "placeholder"

#Startup 
startup = Startup(dut=dut)
dut.SIMULINK_MODEL.GAIN_CONFIG2.VBUS_GAIN.value = 0xC75
dut.SIMULINK_MODEL.GAIN_CONFIG2.VBAT_GAIN.value = 0x435
# dut.SIMULINK_MODEL.GAIN_CONFIG3.IBAT_GAIN.value = 0x825
dut.SIMULINK_MODEL.GAIN_CONFIG3.IBUS_GAIN.value = 0x470
#supply = Instruments().supply
#supply.outp_ON(channel=4)
#supply.outp_ON(channel=1)
time.sleep(1)
# QuickCheck(dut=dut)
loadTrim = LoadTrims(dut=dut,path='json/TrimmingResults_2021_2021.json',chipid=2021)
loadTrim.loadTrims()
# trim = Trim(test_station=test_station,DFT_path='data/DFTInstructions_new.json',loadTrim=loadTrim)
# efficiency = Efficiency(dut=dut)
# cflychar = CflyChar(dut=dut) 
#ReadCurr = Startup_read_curr(dut=dut)
#ReadCurr.buck_startup_curr_meas(dut=dut)
# innerloop = InnerLoop(dut=dut,loadtrims=loadTrim)
#charecterization
# char = AONChar(dut=dut)
# time.sleep(1)
# startup.buck_ClosedLoop(vbat=4,ibat=16,icmd_ph=3.0,No_phase=2,ibus=3.3,phase=0)
# input('Phase1')
# time.sleep(1)
# startup.buck_ClosedLoop(vbat=4,ibat=16,icmd_ph=3.0,No_phase=2,ibus=3.3,phase=1)
# input('Phase2')
# time.sleep(1)
# startup.buck_ClosedLoop(vbat=4,ibat=16,icmd_ph=3.0,No_phase=2,ibus=3.3,phase=2)
# input('Phase3')
# time.sleep(1)
# startup.buck_ClosedLoop(vbat=4,ibat=16,icmd_ph=3.0,No_phase=2,ibus=3.3,phase=3)
# input('Phase4')

# inCS = InputCurrSense(dut=dut)

#@@@@@@@@@@@@@@@@@@@@@@@@@@@
# boost Routine use the vbus parameter to set the boost voltage at initial stage 
# default boost voltage is 5V
# to change the phase use phase parmeter {0-phase1,1-phase2,2-phase3,3-phase4}
#@@@@@@@@@@@@@@@@@@@@@@@@@@@
# startup.boost_ClosedLoop(vbus=5,phase=0)

# To set the boost voltage manual use the following commad 
# example to set the 5V ======>dut.block_apis.SIMULINK_MODEL.set_vbus_boost_thld_V(5)

# Buck Closed Loop
# startup.buck_ClosedLoop(vbat=4,ibat=16.0,No_phase=3,ibus=3.3,icmd_ph=3.0,phase=0)

#startup.buck_startup_setps()
print("-"*50)
print("Enter Code to run... ")
while(input_cmd.lower() != quit_cmd):
    input_cmd = input("> ")                                                                                                                                                                                                                                                                                                                                                                                                          
    try:
        exec(input_cmd)
    except:
        print("The code failed to run...\n")

############Clean Up##########
teardown_test_station(test_station)

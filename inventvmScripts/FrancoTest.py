from socket import gethostname
from dotenv import load_dotenv
import threading
import time
import os
import sys
import re

load_dotenv(r'C:\validation\Projects\Franco\python\franco_val\env\franco_val_inventm.env')
load_dotenv(
    r'C:\validation\Projects\Franco\python\franco_val\env\station\\' + f'franco_val_{gethostname().upper()}.env')
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from ts_support import build_test_station, start_gui, teardown_test_station

ts_cfg_file = os.path.expandvars(r'$PROJECT_ROOT\configs\project_configs\inventvm_config.yml')
test_station = build_test_station(ts_cfg_file)
dut = test_station.eeb.franco

############ Confirm AudioHub ##########
print('~'*50)
print(test_station.audio_hub.ping())

exec(f'test_station.audio_hub.fpga.GLOBAL.ACG1_CTRL.CP_ACG1_ENABLE.value = {hex(1)}') # write the value 
print(eval(f'test_station.audio_hub.fpga.GLOBAL.ACG1_CTRL.CP_ACG1_ENABLE.value')) # read the value 

print('~'*50)
############ Test Code ##########

# TODO
# The command to quit the 'console'
# quit_cmd = "quit"
# input_cmd = "placeholder"
# print("-"*50)
# print("Enter Code to run... ")
# while(input_cmd.lower() != quit_cmd):
#     input_cmd = input("> ")
#     try:
#         exec(input_cmd)
#     except:
#         print("The code failed to run...\n")


import wx
import yaml
import os
from typing import Dict, Union
from val_regmap_gui.reg_map_gui import RegMapGui
from franco_framework.test_stations.franco_test_station import FrancoTestStation as TestStation
from franco_framework.components.franco.franco import Franco
from cl_test_station.interfaces.i2c_interface import I2cReadError

FPGA_IMAGE_VERSION = os.path.expandvars("$DUT_FPGA_VERSION")


def build_test_station(config: Union[Dict, str], add_attrs: Dict = None):
    """
    Builds the CL Test Station from a YAML definition in the file_path
    """
    if add_attrs is None:
        add_attrs = {}

    # read YAML file, if given
    if isinstance(config, str):
        config = yaml.load(config, Loader=yaml.SafeLoader)

    test_station_session = TestStation(config)

    # adding additional attributes
    for k, v in add_attrs.items():
        setattr(test_station_session, k, v)

    # construct system and initialize
    error_count, warning_count = test_station_session.construct_system()
    test_station_session.error_count = error_count
    test_station_session.warning_count = warning_count

    # Program the FPGA before initializing
    test_station_session.audio_hub.connect()
    # Set this pin high to enable mb power
    test_station_session.audio_hub.pins.dev_pdm7_clk.output = 1
    # TODO: Need to remove postfix after figuring out loading encrypted image
    program_fpga(test_station_session.eeb.franco, os.path.expandvars(r'$PROJECT_ROOT\inventm\fpga_images'),
                 FPGA_IMAGE_VERSION)

    error_count, warning_count = test_station_session.system_initialize()
    test_station_session.error_count += error_count
    test_station_session.warning_count += warning_count
    return test_station_session


def program_fpga(dut: Franco, directory: str, version: str, postfix: str = '1_franco_efuse_key', force_program=False):
    """
    Programs the V7 FPGA with the requested FPGA version. This has a dependency on the naming convention of the .bit
    files. Do not rename the bit files from their original name.

    :param dut:
    :param directory:
    :param version:
    :param postfix:
    :return:
    """
    C4_ADDR = 0x20000008
    BUILD_ADDR = 0x2000000C
    file_path = f'{directory}/{version}_{postfix}.bit'
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f'Could not find requested FPGA image file in {file_path}')

    try:
        c4 = '{:04x}'.format(dut.read_register(C4_ADDR))
        build = '{:02x}'.format(dut.read_register(BUILD_ADDR))
        version_str = f'e{c4}_{build}'
        dut.log.info(f'Requested FPGA version is {version}, current version programmed is {version_str}')
    except I2cReadError:
        dut.log.info(f'Could not read the version off the FPGA, programming FPGA with version {version}')
        dut._load_image(file_path)
    else:
        if version_str != version or force_program:
            dut.log.info(f'Programming FPGA with image: {file_path}')
            dut._load_image(file_path)
        else:
            dut.log.info('FPGA version requested already matches the version currently programmed')


def teardown_test_station(test_station_session):
    """
    Cleans up resources for the test. Call this at the end of the test.
    """
    test_station_session.cleanup_system()
    test_station_session.shutdown()


def start_gui(*args):
    app = wx.App()
    gui = RegMapGui(*args)
    app.MainLoop()

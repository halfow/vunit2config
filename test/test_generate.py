"""
Basic tests just to make sure to exec all methods
    * ensure all supported python versions
    * Does NOT cover config files correctness for now...
"""
from vunit import VUnit
from vunit2config import generate


def test_hdl_checker():
    """Generate config file"""
    generate.hdl_checker_config(VUnit.from_argv([]))


def test_vhdl_ls():
    """Generate config file"""
    generate.vhdl_ls_config(VUnit.from_argv([]))


def test_ghdl_ls():
    """Generate config file"""
    generate.ghdl_ls_config(VUnit.from_argv([]))

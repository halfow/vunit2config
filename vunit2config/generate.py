"""Config Generators

*Example:*
.. code-block:: python
    vunit = VUnit.from_argv()
    ...
    # Config generators should be at the end of the script for obvious reasons
    hdl_checker_config(vunit)
    vhdl_ls_config(vunit)
    vunit.main()
"""
import os
import json
import logging
from pathlib import Path
from collections import defaultdict
from typing import Union

import toml
from vunit import VUnit

# Create logger channel for this module
log = logging.getLogger(__name__)


def hdl_checker_config(vunit: VUnit, output: Union[str, Path] = ".", simulator: str = "fallback") -> None:
    """
    Generate a hdl checker configuration file from a vunit object

    Args:
        vunit (VUnit): Project object
        path (Union[str, Path], optional): output path. Defaults to ".".
        simulator (str, optional): Simulator to use for linting. Defaults to "fallback".
    """

    simulators = ["msim", "xvhdl", "ghdl", "fallback"]
    assert simulator in simulators, f"expected any of {simulators}"
    log.warning("Experimental suport for hdl-checker")

    # Handle windows/linux prefix
    prefix = "_" if os.name == "nt" else "."
    cfg = Path(output).resolve(strict=True) / f"{prefix}hdl_checker.config"

    # Dump config
    cfg.write_text(
        json.dumps(
            dict(
                # FIXME: Flag style differs between simulators
                # FIXME: Standard will probably break for verilog and other than 2008
                sources=[
                    [obj.name, dict(library=obj.library.name, flags=[f"-{obj.vhdl_standard}"])]
                    for obj in vunit.get_compile_order()
                ],
                builder=simulator,
            ),
            indent=4,
        )
    )

    log.info(f"Created: {cfg.name} @ {str(cfg)}")


def vhdl_ls_config(vunit: VUnit, output: Union[str, Path] = ".") -> None:
    """
    Generate vhdl ls configuration file

    Args:
        vunit (VUnit): VUnit project
        output (Union[str, Path], optional): Output path. Defaults to ".".
    """

    tmp = defaultdict(list)
    for obj in vunit.get_compile_order():
        tmp[f"{obj.library.name}.files"].append(obj.name)

    cfg = Path(output).resolve(strict=True) / "vhdl_ls.toml"
    cfg.write_text(toml.dumps(dict(libraries=tmp)))

    log.info(f"Created: {cfg.name} @ {str(cfg)}")


def ghdl_ls_config(vunit: VUnit, output: Union[str, Path] = ".") -> None:
    """
    Generate GHDL-ls configuration file

    Args:
        vunit (VUnit): VUnit project
        output (Union[str, Path], optional): output path. Defaults to ".".
    """
    log.warning("Experimental support for ghdl-ls")

    cfg = Path(output).resolve(strict=True) / "hdl-prj.json"
    cfg.write_text(
        json.dumps(
            dict(
                # TODO: let user pass arguments to this region
                # NOTE: settings selected are copy past form ghdl-ls example
                options=dict(ghdl_analysis=["--workdir=work", "--ieee=synopsys", "-fexplicit"]),
                # TODO: need attention
                files=[dict(file=obj.name, language="vhdl") for obj in vunit.get_compile_order()],
            ),
            indent=4,
        )
    )

    log.info(f"Created: {cfg.name} @ {str(cfg)}")


if __name__ == "__main__":
    # Enable all log traces
    logging.basicConfig()
    log.setLevel(logging.DEBUG)

    # Usage example
    vu = VUnit.from_argv(["-f"])
    ...
    hdl_checker_config(vu)
    ghdl_ls_config(vu)
    vhdl_ls_config(vu)
    vu.main()

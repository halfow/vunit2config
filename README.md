# Vunit2config
use the vunit object to generate configuration files for other tools (linters, formatters...).


## Example usage: 
```python
from vunit import VUnit
from vunit2config import generate

vunit = VUnit.form_argv()
...
generate.vhdl_ls_config(vunit)
generate.hdl_checker_config(vunit)
generate.ghdl_ls_config(vunit)
vunit.main()
```

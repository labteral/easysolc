# easysolc
Easysolc is a simple wrapper for the Solidity compiler (`solc`). You can specify a custom `solc` binary or use the first available follwing the `PATH` environment variable.

This library also faciliates the creation of web3 contract instance from the compiled source.

All the `solc` parameters are supported and can be set when invoking the `compile` method. However, you can also specify the parameters in string or array format directly with the `args` parameter.

## Compile source code:
```python
from easysolc import Solc
solc = Solc()
solc.compile('ballot.sol')
```

## Load a custom solc binary
```python
solc = Solc('/usr/local/bin/solc')
```
```python
solc = Solc('/usr/local/bin')
```
```python
solc = Solc('/usr/local/bin/')
```

## Get a web3 contract instance
```python
contract = solc.get_contract('ballot.abi', 'ballot.bin')
```

## List of parameters of the `compile` method and default values:
```python
source='*.sol'
args=None
optimize=False
optimize_runs=200
pretty_json=False
libraries=None
output_dir='.'
overwrite=True
combined_json=None
gas=False
standard_json=False
assemble=False
yul=False
strict_assembly=False
machine=None
link=False
metadata_literal=False
allow_paths=None
ignore_missing=False
ast=False
ast_json=False
ast_compact_json=False
asm=False
asm_json=False
opcodes=False
bin_=True
bin_runtime=False
abi=True
hashes=False
userdoc=False
devdoc=False
metadata=False
```
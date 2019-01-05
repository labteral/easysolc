# easysolc

> Tested with solc 0.5.2+commit.1df8f40c

Easysolc is a simple wrapper for the Solidity compiler (`solc`). You can specify a custom `solc` binary or use the first available following the paths specified under the `$PATH` environment variable.

This library also faciliates the creation of web3 contract instances directly from the source code or from previously generated files containing the ABI and the bytecode.

All the `solc` parameters are supported and they can be set when invoking the `compile` method. However, you can also specify all the arguments directly with the `args` parameter.

# Usage
## Installation
```bash
pip install easysolc
```

## Create an instance of the compiler
If a path is not indicated, the binary used will be the first accesible following the paths of the `$PATH` environment variable:
```python
from easysolc import Solc
solc = Solc()
```

It is also possible to load the compiler from custom paths:
```python
solc = Solc('/usr/local/bin/solc')
```
```python
solc = Solc('/usr/local/bin')
```
```python
solc = Solc('/usr/local/bin/')
```

## Functionalities

Compile the source code using files as output in the current directory:
```python
solc.compile('ballot.sol', output_dir='.')
```

Do the same but manually indicating the arguments:
```python
solc.compile('ballot.sol', '--abi --bin -o .')
```
```python
solc.compile(args='--overwrite --abi --bin -o . ballot.sol')
```
```python
solc.compile(args=['--overwrite', '--abi', '--bin', '-o', '.', 'ballot.sol'])
```

Get a web3 contract instance given the source code:
```python
contract = solc.get_contract_instance(source='ballot.sol',
                                      contract_name='Ballot')
```

Get a web3 contract instance given the files containing the ABI and bytecode:
```python
contract = solc.get_contract_instance(abi_file='ballot.abi',
                                      bytecode_file='ballot.bin')
```

Get a web3 contract instance given the ABI file and the contract address:
```python
contract = solc.get_contract_instance(abi_file='ballot.abi',
                                      address=0x0)
```

Get a dictionary with the ABI and bytecode given the source code:
```python
contract_dict = solc.compile('ballot.sol')
```

Get a web3 contract instance given a dictionary with the ABI and bytecode of the contract:
```python
contract = solc.get_contract_instance(contract_dict['Ballot'])
```

## List of parameters and default values of the `compile` method
```python
source='*.sol'
args=None
optimize=False
optimize_runs=200
pretty_json=False
libraries=None
output_dir=None
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

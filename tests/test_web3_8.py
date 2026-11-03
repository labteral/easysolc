"""No-network contract construction with the current Web3 API."""

from easysolc import Solc


def test_contract_instance_uses_web3_8():
    contract = Solc().get_contract_instance(
        contract_dict={'abi': [], 'bytecode': '0x00'})
    assert contract.abi == []
    assert bytes(contract.bytecode) == b'\x00'

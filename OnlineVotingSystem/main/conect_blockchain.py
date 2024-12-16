from web3 import Web3
from main.deploy_contract import *

# Configurar Web3 con Ganache
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))  # URL de Ganache
assert web3.is_connected()

# ABI y dirección del contrato desplegado (utiliza la dirección de tu contrato desplegado)
contract_address = contract_address #dirección de contrato
contract_abi = abi  # ABI del contrato

contract = web3.eth.contract(address=contract_address, abi=contract_abi)
from web3 import Web3
import json

# Conexión con Ganache
GANACHE_URL = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(GANACHE_URL))

# Verificar conexión
if not web3.isConnected():
    raise Exception("No se pudo conectar a Ganache")

# Cargar contrato
CONTRACT_ADDRESS = "0x..."  # Dirección del contrato desplegado
with open("blockchain/build/contracts/Votacion.json") as f:
    contract_data = json.load(f)
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_data['abi'])

# Función para emitir un voto
def votar(id_candidato, direccion_votante, clave_privada):
    # Crear transacción
    nonce = web3.eth.getTransactionCount(direccion_votante)
    tx = contract.functions.votar(id_candidato).buildTransaction({
        'chainId': 1337,  # Ganache utiliza esta ID de red
        'gas': 2000000,
        'gasPrice': web3.toWei('20', 'gwei'),
        'nonce': nonce
    })

    # Firmar y enviar transacción
    signed_tx = web3.eth.account.sign_transaction(tx, clave_privada)
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

    # Esperar confirmación
    receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    return receipt

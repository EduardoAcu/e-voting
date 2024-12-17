from web3 import Web3
from solcx import compile_source
from solcx import install_solc, set_solc_version


# Instalar Solidity versión 0.8.0
install_solc("0.8.0")

# Configura la versión instalada (por ejemplo, 0.8.0)
set_solc_version("0.8.0")

from web3 import Web3

# Conectarse a Ganache (asegúrate de que Ganache esté corriendo en el puerto correcto)
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

# Verificar si la conexión es exitosa
if web3.is_connected():
    print("Conexión exitosa con Ganache.")
else:
    print("No se pudo conectar a Ganache.")

# Ruta del archivo que contiene las claves privadas (ganache-accounts.txt)
accounts_file = "ganache-accounts.txt"

# Inicializar private_keys como una lista vacía para evitar el error
private_keys = []

# Leer las claves privadas desde el archivo
try:
    with open(accounts_file, "r") as file:
        private_keys = file.readlines()

    # Eliminar saltos de línea y espacios adicionales de las claves privadas
    private_keys = [key.strip() for key in private_keys]

    # Verificar si el archivo tiene claves privadas
    if not private_keys:
        print("No se encontraron claves privadas en el archivo.")
    else:
        print(f"Se encontraron {len(private_keys)} claves privadas.")
except FileNotFoundError:
    print(f"No se encontró el archivo {accounts_file}. Asegúrate de que la ruta sea correcta.")

# Obtener las cuentas disponibles en Ganache
accounts = web3.eth.accounts  # Obtener las cuentas de Ganache
print("Cuentas disponibles en Ganache:", accounts)

# Si hay cuentas disponibles, seleccionar la primera cuenta
if accounts:
    web3.eth.default_account = accounts[0]
    print("Usando la cuenta:", web3.eth.default_account)
else:
    print("No se encontraron cuentas en Ganache.")

# Si hay claves privadas en el archivo, mostrarlas
if private_keys:
    for idx, private_key in enumerate(private_keys, start=1):
        print(f"Clave privada {idx}: {private_key}")
else:
    print("No se encontraron claves privadas para mostrar.")


# Código fuente del contrato (Voting.sol)
contract_source_code = """
pragma solidity ^0.8.0;

contract Voting {
    struct Vote {
        address voter;
        string candidate;
        uint256 timestamp;
    }

    mapping(string => Vote) public votes; // Hash of vote => Vote details
    mapping(address => bool) public hasVoted; // Prevent double voting

    event VoteCast(address indexed voter, string candidate, string voteHash, uint256 timestamp);

    function castVote(string memory _candidate, string memory _voteHash) public {
        require(!hasVoted[msg.sender], "You have already voted!");

        // Register the vote
        votes[_voteHash] = Vote({
            voter: msg.sender,
            candidate: _candidate,
            timestamp: block.timestamp
        });

        hasVoted[msg.sender] = true;

        // Emit event for logging
        emit VoteCast(msg.sender, _candidate, _voteHash, block.timestamp);
    }

    function getVote(string memory _voteHash) public view returns (address, string memory, uint256) {
        Vote memory vote = votes[_voteHash];
        return (vote.voter, vote.candidate, vote.timestamp);
    }
}
"""

# Compilar el contrato
compiled_contract = compile_source(contract_source_code)
contract_id, contract_interface = compiled_contract.popitem()

# ABI y Bytecode
abi = contract_interface["abi"]
bytecode = contract_interface["bin"]

print("ABI:", abi)
print("Bytecode:", bytecode)

# Crear el contrato en Web3
contract = web3.eth.contract(abi=abi, bytecode=bytecode)

# Construir la transacción de despliegue
transaction = contract.constructor().build_transaction({
    'from': web3.eth.default_account,
    'gas': 3000000,
    'gasPrice': web3.to_wei('50', 'gwei'),
    'nonce': web3.eth.get_transaction_count(web3.eth.default_account),
})

# Firmar la transacción
signed_tx = web3.eth.account.sign_transaction(transaction, private_key)

# Enviar la transacción
tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)

# Esperar por la transacción
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

# Dirección del contrato desplegado
contract_address = tx_receipt.contractAddress
print(f"Contrato desplegado en: {contract_address}")

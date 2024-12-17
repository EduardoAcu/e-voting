from django.apps import AppConfig
from web3 import Web3
from solcx import compile_source
from solcx import install_solc, set_solc_version
import os
import json

# Instalar Solidity versión 0.8.0
install_solc("0.8.0")

# Configurar la versión instalada
set_solc_version("0.8.0")

class MainConfig(AppConfig):
    name = "main"

    def ready(self):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        contract_file = os.path.join(BASE_DIR, "contract_deployed.txt")
    
        # Verificar si el contrato ya está desplegado
        if not os.path.exists("contract_deployed.txt"):
            print("Contrato no desplegado, procediendo al despliegue...")

            # Conectarse a Ganache
            web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))  # Usar la URL de Ganache o el proveedor correspondiente
            assert web3.is_connected()

            # Obtener la primera cuenta disponible de Ganache
            accounts = web3.eth.accounts  # Obtener las cuentas de Ganache
            print("Cuentas disponibles en Ganache:", accounts)

            # Seleccionar la primera cuenta disponible
            web3.eth.default_account = accounts[0]
            print("Usando la cuenta:", web3.eth.default_account)

            # Clave privada de la cuenta (deberías obtenerla manualmente desde Ganache UI o el archivo de configuración)
            private_key = "0xc3aae90f7fb0f85d012fb03105820fe199958bd1a7069e3565f1b02cb09e8ca4"  # Clave privada obtenida de Ganache UI o archivo de configuración

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


            # Crear el contrato en Web3
            contract = web3.eth.contract(abi=abi, bytecode=bytecode)

            # Construir la transacción de despliegue
            transaction = contract.constructor().build_transaction({
                'from': web3.eth.default_account,
                'gas': 700000,
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

            # Crear el archivo para indicar que el contrato ya fue desplegado
            with open(contract_file, 'w') as f:
                f.write(contract_address)

            contract = web3.eth.contract(address=contract_address, abi=abi)

            with open("contract_abi.json", "w") as abi_file:
                json.dump(abi, abi_file)

        else:
            # Si el contrato ya ha sido desplegado, leer la dirección desde el archivo
            with open(contract_file, 'r') as f:
                contract_address = f.read()
            print(f"El contrato ya está desplegado en: {contract_address}")


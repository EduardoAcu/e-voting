// SPDX-License-Identifier: MIT
pragma solidity >=0.4.4 <0.7.0;
pragma experimental ABIEncoderV2;

contract Votacion {
    // Dirección del propietario del contrato
    address public owner;

    // Constructor
    constructor() public {
        owner = msg.sender;
    }

    // Relación entre el ID del candidato y el número de votos
    mapping(string => uint) private votosCandidato;

    // Lista de los hashes de la identidad de los votantes
    bytes32[] private votantes;

    // Evento para registrar un nuevo voto
    event VotoRegistrado(string idCandidato, uint totalVotos);

    // Función para emitir un voto a un candidato identificado por su ID
    function votar(string memory idCandidato) public {
        // Hash de la dirección del votante
        bytes32 hashVotante = keccak256(abi.encodePacked(msg.sender));

        // Verificar si el votante ya ha votado
        for (uint i = 0; i < votantes.length; i++) {
            require(votantes[i] != hashVotante, "Ya has votado previamente");
        }

        // Registrar al votante
        votantes.push(hashVotante);

        // Incrementar el número de votos del candidato
        votosCandidato[idCandidato]++;

        // Emitir un evento con el resultado del voto
        emit VotoRegistrado(idCandidato, votosCandidato[idCandidato]);
    }

    // Función para consultar el número de votos de un candidato
    function verVotos(string memory idCandidato) public view returns (uint) {
        return votosCandidato[idCandidato];
    }
}

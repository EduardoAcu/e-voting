// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

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
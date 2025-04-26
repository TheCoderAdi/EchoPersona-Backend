// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

contract EchoMaze {
    struct Duel {
        address creator;
        address challenger;
        bytes32 committedPath;
        string[] guessPath;
        string[] originalPath;
        bool revealed;
        address winner;
    }

    mapping(uint => Duel) public duels;
    uint public nextDuelId;

    event DuelCreated(uint duelId, address creator);
    event GuessSubmitted(uint duelId, address challenger);
    event MazeRevealed(uint duelId, address winner);

    function createDuel(bytes32 pathHash) external returns (uint) {
        uint duelId = nextDuelId++;
        duels[duelId].creator = msg.sender;
        duels[duelId].committedPath = pathHash;
        emit DuelCreated(duelId, msg.sender);
        return duelId;
    }

    function submitGuess(uint duelId, string[] memory path) external {
        Duel storage duel = duels[duelId];
        require(duel.challenger == address(0), "Already challenged");
        require(msg.sender != duel.creator, "Can't challenge yourself");
        duel.challenger = msg.sender;
        duel.guessPath = path;
        emit GuessSubmitted(duelId, msg.sender);
    }

    function hashPath(string[] memory path) public pure returns (bytes32) {
        bytes memory combined;
        for (uint i = 0; i < path.length; i++) {
            combined = bytes.concat(combined, bytes(path[i]));
        }
        return keccak256(combined);
    }

    function revealMaze(uint duelId, string[] memory originalPath) external {
        Duel storage duel = duels[duelId];
        require(msg.sender == duel.creator, "Only creator can reveal");
        require(!duel.revealed, "Already revealed");

        bytes32 hash = hashPath(originalPath);
        require(hash == duel.committedPath, "Path mismatch");

        duel.originalPath = originalPath;
        duel.revealed = true;

        if (pathsEqual(originalPath, duel.guessPath)) {
            duel.winner = duel.challenger;
        } else {
            duel.winner = duel.creator;
        }

        emit MazeRevealed(duelId, duel.winner);
    }

    function getWinner(uint duelId) external view returns (address) {
        return duels[duelId].winner;
    }

    function pathsEqual(
        string[] memory a,
        string[] memory b
    ) internal pure returns (bool) {
        if (a.length != b.length) return false;
        for (uint i = 0; i < a.length; i++) {
            if (keccak256(bytes(a[i])) != keccak256(bytes(b[i]))) return false;
        }
        return true;
    }
}

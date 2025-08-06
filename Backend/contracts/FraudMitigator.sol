// contracts/FraudMitigator.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;
import "./FraudLedger.sol";

contract FraudMitigator {
    // This contract contains the business logic.
    address public owner;
    FraudLedger private fraudLedger;
    mapping(address => bool) public frozenAccounts;

    event AccountFrozen(address indexed userAccount);
    event MfaTriggered(string transactionIdentifier);

    constructor(address _ledgerAddress) {
        fraudLedger = FraudLedger(_ledgerAddress);
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only the owner (the API server) can call this function.");
        _;
    }

    function freezeAccount(address _userAccount) internal {
        if (!frozenAccounts[_userAccount]) {
            frozenAccounts[_userAccount] = true;
            emit AccountFrozen(_userAccount);
        }
    }

    function triggerMfa(string memory _transactionIdentifier) internal {
        // In a real system, this would interact with an off-chain oracle.
        // For our project, it emits an event that the frontend/backend can listen for.
        emit MfaTriggered(_transactionIdentifier);
    }

    // The API server will call this main function
    function executeResponse(
        uint256 riskScore,
        address userAccount,
        string memory transactionIdentifier,
        uint[1] memory publicInputs,
        uint[2] memory a,
        uint[2][2] memory b,
        uint[2] memory c
    ) public onlyOwner {
        if (riskScore >= 85) { // High Risk
            freezeAccount(userAccount);
            // Call the other contract to report the fraud with proof
            fraudLedger.reportFraudWithProof(transactionIdentifier, publicInputs, a, b, c);
        } else if (risk_score >= 60) { // Medium Risk
            triggerMfa(transactionIdentifier);
        }
        // If low risk, do nothing.
    }
}
// contracts/FraudLedger.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;
import "./Verifier.sol";

contract FraudLedger {
    Verifier private verifier;

    struct SecureFraudReport {
        uint256 reportId;
        string transactionIdentifier;
        uint256 blockTimestamp;
        address reporter;
    }

    uint256 public reportCounter;
    mapping(uint256 => SecureFraudReport) public secureFraudReports;

    event SecureReportAdded(uint256 indexed reportId, string transactionIdentifier);

    constructor(address _verifierAddress) {
        verifier = Verifier(_verifierAddress);
        reportCounter = 0;
    }

    function reportFraudWithProof(
        string memory _transactionIdentifier,
        uint[2] memory _publicInputs,
        uint[2] memory a,
        uint[2][2] memory b,
        uint[2] memory c
    ) public {
        // Create Proof struct
        Verifier.Proof memory proof = Verifier.Proof({
            a: Pairing.G1Point(a[0], a[1]),
            b: Pairing.G2Point([b[0][0], b[0][1]], [b[1][0], b[1][1]]),
            c: Pairing.G1Point(c[0], c[1])
        });
        
        // Verify ZKP
        require(verifier.verifyTx(proof, _publicInputs), "ZKP verification failed.");

        reportCounter++;
        secureFraudReports[reportCounter] = SecureFraudReport(
            reportCounter,
            _transactionIdentifier,
            block.timestamp,
            msg.sender
        );

        emit SecureReportAdded(reportCounter, _transactionIdentifier);
    }
}

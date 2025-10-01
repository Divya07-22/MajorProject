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
        uint[1] memory _publicInputs,
        uint[2] memory a,
        uint[2][2] memory b,
        uint[2] memory c
    ) public {
        // Require that the ZKP is valid before proceeding
        require(verifier.verifyTx(
            [a[0], a[1], b[0][0], b[0][1], b[1][0], b[1][1], c[0], c[1]],
            _publicInputs
        ), "ZKP verification failed.");

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
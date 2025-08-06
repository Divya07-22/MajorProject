// migrations/1_deploy_contracts.js
const Verifier = artifacts.require("Verifier");
const FraudLedger = artifacts.require("FraudLedger");
const FraudMitigator = artifacts.require("FraudMitigator");

module.exports = async function (deployer) {
  // Deploy ZKP Verifier
  await deployer.deploy(Verifier);
  const verifier = await Verifier.deployed();

  // Deploy Ledger, linking it to the Verifier
  await deployer.deploy(FraudLedger, verifier.address);
  const ledger = await FraudLedger.deployed();

  // Deploy Mitigator, linking it to the Ledger
  await deployer.deploy(FraudMitigator, ledger.address);
  const mitigator = await FraudMitigator.deployed();

  console.log(`Verifier deployed at: ${verifier.address}`);
  console.log(`FraudLedger deployed at: ${ledger.address}`);
  console.log(`FraudMitigator deployed at: ${mitigator.address}`);
};

// migrations/1_deploy_contracts.js
const Verifier = artifacts.require("Verifier");
const FraudLedger = artifacts.require("FraudLedger");
const FraudMitigator = artifacts.require("FraudMitigator");

module.exports = async function (deployer, network, accounts) {
  // The API server will be the owner of the main contract
  const serverAccount = accounts[0];

  // 1. Deploy the Verifier contract first
  await deployer.deploy(Verifier);
  const verifier = await Verifier.deployed();

  // 2. Deploy the FraudLedger, linking it to the Verifier's address
  await deployer.deploy(FraudLedger, verifier.address);
  const ledger = await FraudLedger.deployed();

  // 3. Deploy the main FraudMitigator, linking it to the Ledger's address
  await deployer.deploy(FraudMitigator, ledger.address, { from: serverAccount });
  const mitigator = await FraudMitigator.deployed();

  console.log("--- Contract Deployment Summary ---");
  console.log(`Verifier Contract deployed at: ${verifier.address}`);
  console.log(`FraudLedger Contract deployed at: ${ledger.address}`);
  console.log(`FraudMitigator Contract deployed at: ${mitigator.address}`);
  console.log(`FraudMitigator owner (server account) is: ${serverAccount}`);
  console.log("---------------------------------");
};
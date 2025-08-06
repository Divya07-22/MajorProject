// truffle-config.js

// This line is needed to deploy to networks like Polygon.
// Run 'npm install @truffle/hdwallet-provider' to install it.
// const HDWalletProvider = require('@truffle/hdwallet-provider');
// const privateKey = 'YOUR_METAMASK_PRIVATE_KEY';
// const alchemyRpcUrl = 'YOUR_ALCHEMY_POLYGON_RPC_URL';

module.exports = {
  // This section defines the blockchain networks Truffle can connect to.
  networks: {
    // Configuration for your local development blockchain (Ganache)
    development: {
      host: "127.0.0.1",     // Localhost
      port: 7545,            // Standard Ganache port
      network_id: "*",       // Match any network id
    },

    // Example configuration for deploying to the Polygon Testnet (Mumbai)
    // mumbai: {
    //   provider: () => new HDWalletProvider(privateKey, alchemyRpcUrl),
    //   network_id: 80001,
    //   confirmations: 2,
    //   timeoutBlocks: 200,
    //   skipDryRun: true
    // },
  },

  // Set default mocha options here, use special reporters, etc.
  mocha: {
    // timeout: 100000
  },

  // Configure your compilers
  compilers: {
    solc: {
      version: "0.8.20",      // Fetch exact version from solc-bin (default: truffle's version)
      settings: {          // See the solidity docs for advice about optimization and evmVersion
        optimizer: {
          enabled: true,
          runs: 200
        },
      }
    }
  },
};
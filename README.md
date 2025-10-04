# Aegis - AI-Powered Fraud Detection System

Aegis is a full-stack web application designed to detect and mitigate fraudulent financial transactions in real-time. It combines a multi-layered AI engine with a blockchain-based ledger to provide a secure, transparent, and intelligent fraud prevention system.

## ✨ Features

- **Multi-Page User Interface:** A modern, responsive frontend with separate portals for users and administrators.
- **Secure Authentication:** JWT-based authentication for secure user sessions.
- **Real-Time Transaction Analysis:** Users can initiate transactions which are immediately analyzed by a sophisticated AI engine.
- **Multi-Layered AI Engine:**
    - **Isolation Forest:** For anomaly detection.
    - **LSTM Autoencoder:** For behavioral profiling.
    - **Graph Neural Network (GNN):** For relational analysis (placeholder).
    - **XGBoost Meta-Model:** A final classifier that combines the scores from all other models to produce a definitive risk score.
- **Dynamic Risk Response:**
    - **Low Risk:** Transaction is approved.
    - **Medium Risk:** An alert is triggered (placeholder for MFA).
    - **High Risk:** The user's account is automatically frozen, a report is logged on the blockchain, and an automated voice call is initiated via Twilio to alert the user.
- **Immutable Audit Trail:** High-risk transactions are recorded on a private Ethereum blockchain (Ganache) for tamper-proof auditing.
- **Comprehensive User Dashboard:**
    - Displays the real-time risk score.
    - Shows a system log of recent activity.
    - Includes a full transaction history with a filterable table.
    - Features a graph to visualize risk scores over time.
- **Functional Admin Panel:** A secure area for administrators to monitor all transactions from all users in real-time.
- **Dual Theme UI:** A theme toggle allows switching between a sleek dark mode and a clean light mode.

## 🛠️ Tech Stack

- **Frontend:** React, Vite, Styled-Components, Recharts
- **Backend:** Python, Flask
- **Databases:**
    - **PostgreSQL:** For storing user and transaction summary data.
    - **MongoDB:** For storing detailed transaction logs.
- **Blockchain:** Solidity, Truffle, Ganache
- **AI & Machine Learning:** Scikit-learn, TensorFlow, XGBoost, Pandas
- **Services:** Docker, Twilio

---

## 🚀 Getting Started: Step-by-Step Installation

These are the final, complete instructions to run the project from a clean computer.

### **1. Prerequisites**
Ensure you have the following software installed on your system:
- Node.js (LTS version)
- Python (3.9+)
- Docker Desktop
- Ganache UI
- Truffle (`npm install -g truffle`)

### **2. Backend Setup**
Navigate into the `backend` directory.
```bash
cd backend
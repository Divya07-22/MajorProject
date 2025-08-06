# models/3_gnn_fraud_detection.py

import pandas as pd
import numpy as np
import torch
from torch_geometric.data import Data
from torch.nn import Linear
import torch.nn.functional as F
from torch_geometric.nn import GCNConv
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib

print("Starting Model 3: Graph Neural Network (GNN) Fraud Ring Detection...")

# --- 1. Data Loading and Preprocessing ---
df = pd.read_csv('data/creditcard.csv')

# For demonstration, we'll use a smaller, balanced sample of the data to build the graph.
# Using the full dataset would be very computationally expensive.
df_fraud = df[df['Class'] == 1]
df_normal = df[df['Class'] == 0].sample(n=len(df_fraud) * 5, random_state=42) # 5:1 ratio
df_sample = pd.concat([df_fraud, df_normal]).sort_values(by='Time').reset_index(drop=True)

print(f"Running GNN on a sample of {len(df_sample)} transactions for efficiency.")

# Scale features
scaler = StandardScaler()
df_sample['scaled_amount'] = scaler.fit_transform(df_sample['Amount'].values.reshape(-1, 1))
features = df_sample.drop(['Time', 'Amount', 'Class'], axis=1).values
labels = df_sample['Class'].values

# --- 2. Graph Construction ---
# We create edges between transactions that occur within a small time delta (e.g., 10 seconds)
edge_list = []
time_values = df_sample['Time'].values
time_delta = 10 

for i in range(len(df_sample)):
    for j in range(i + 1, len(df_sample)):
        if time_values[j] - time_values[i] > time_delta:
            break # Since the data is sorted by time, we can stop searching
        edge_list.append([i, j])

print(f"Graph constructed with {len(df_sample)} nodes and {len(edge_list)} edges.")

# Convert to PyTorch Geometric format
edge_index = torch.tensor(edge_list, dtype=torch.long).t().contiguous()
x = torch.tensor(features, dtype=torch.float)
y = torch.tensor(labels, dtype=torch.long)

data = Data(x=x, edge_index=edge_index, y=y)

# Create train/test masks for nodes
train_mask, test_mask = train_test_split(range(len(df_sample)), test_size=0.2, random_state=42, stratify=y)
data.train_mask = torch.zeros(data.num_nodes, dtype=torch.bool)
data.test_mask = torch.zeros(data.num_nodes, dtype=torch.bool)
data.train_mask[train_mask] = True
data.test_mask[test_mask] = True


# --- 3. GNN Model Definition ---
class GCN(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = GCNConv(data.num_node_features, 16)
        self.conv2 = GCNConv(16, 2) # Output dimension is 2 (fraud, not_fraud)

    def forward(self, data):
        x, edge_index = data.x, data.edge_index
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = F.dropout(x, training=self.training)
        x = self.conv2(x, edge_index)
        return F.log_softmax(x, dim=1)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = GCN().to(device)
data = data.to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-4)

# --- 4. Training Loop ---
model.train()
for epoch in range(200):
    optimizer.zero_grad()
    out = model(data)
    loss = F.nll_loss(out[data.train_mask], data.y[data.train_mask])
    loss.backward()
    optimizer.step()
    if epoch % 20 == 0:
        print(f'Epoch {epoch}: Loss: {loss.item():.4f}')

print("GNN model trained.")

# --- 5. Evaluation and Saving ---
model.eval()
pred = model(data).argmax(dim=1)
correct = (pred[data.test_mask] == data.y[data.test_mask]).sum()
acc = int(correct) / int(data.test_mask.sum())
print(f'Accuracy on test nodes: {acc:.4f}')

# Save the model
torch.save(model.state_dict(), 'models/trained_models/gnn_model.pth')
print("Model saved to models/trained_models/gnn_model.pth")

# Save predictions for the final meta-model
# We'll create a dataframe that matches the original full dataframe's index
gnn_predictions = pred.cpu().numpy()
df_sample['gnn_pred'] = gnn_predictions
final_gnn_output = df_sample[['gnn_pred']].reindex(df.index, fill_value=-1) # -1 for nodes not in the sample
final_gnn_output.to_csv('data/3_gnn_results.csv', index=False)
print("Results saved to data/3_gnn_results.csv")
print("Model 3 complete.")
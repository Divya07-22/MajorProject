import re

with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip_next = 0
i = 0

while i < len(lines):
    line = lines[i]
    
    # Find LSTM loading block and replace it
    if '# Load LSTM Autoencoder' in line:
        # Skip next 5 lines (the loading code)
        new_lines.append('    # LSTM removed for stability - using Isolation Forest + XGBoost\n')
        new_lines.append('    lstm_autoencoder = None\n')
        new_lines.append('    logger.info(\"Using stable ensemble: Isolation Forest + XGBoost\")\n')
        new_lines.append('\n')
        # Skip the old loading code (next 5 lines)
        i += 6
        continue
    
    new_lines.append(line)
    i += 1

# Write back
with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(' LSTM FIXED - Removed and replaced with None')
print(' Backend now uses stable Isolation Forest + XGBoost ensemble')

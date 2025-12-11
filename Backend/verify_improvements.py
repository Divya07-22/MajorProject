print("="*70)
print("VERIFYING IMPROVEMENTS")
print("="*70)

# 1. Check if LSTM was properly handled
print("\n[1] Checking LSTM Fix...")
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()
    if 'Using Isolation Forest + XGBoost ensemble' in content:
        print(" LSTM properly removed/fixed")
    else:
        print(" LSTM not fixed")

# 2. Check Dockerfile
print("\n[2] Checking Dockerfile...")
import os
if os.path.exists('Dockerfile'):
    with open('Dockerfile', 'r') as f:
        docker_content = f.read()
        if 'gunicorn' in docker_content:
            print(" Dockerfile created with Gunicorn")
        else:
            print(" Dockerfile exists but no Gunicorn")
else:
    print(" Dockerfile not found")

# 3. Check Gunicorn installation
print("\n[3] Checking Gunicorn...")
import subprocess
result = subprocess.run(['pip', 'show', 'gunicorn'], 
                       capture_output=True, text=True)
if result.returncode == 0:
    print(" Gunicorn installed")
else:
    print(" Gunicorn not installed")

# 4. Check production script
print("\n[4] Checking Production Script...")
if os.path.exists('run_production.ps1'):
    print(" Production run script created")
else:
    print(" Production script not found")

# 5. Check backup
print("\n[5] Checking Backup...")
if os.path.exists('app_backup.py'):
    print(" Backup file exists")
else:
    print(" No backup found")

print("\n" + "="*70)
print("VERIFICATION COMPLETE")
print("="*70)

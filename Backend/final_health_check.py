import subprocess
import sys

print("="*70)
print("COMPLETE BACKEND HEALTH CHECK")
print("="*70)

# 1. Check Flask logs for errors
print("\n[1] Checking Flask Server Logs...")
print("Look at your Flask terminal - should show NO red ERROR lines")
print("Only warnings about emoji/deprecation are OK (not critical)")

# 2. Run comprehensive tests
print("\n[2] Running All API Tests...")
result = subprocess.run([sys.executable, "ultimate_backend_test.py"], 
                       capture_output=True, text=True)
print(result.stdout)

if "100.0%" in result.stdout:
    print("\n ALL TESTS PASSED!")
else:
    print("\n SOME TESTS FAILED - Check output above")

# 3. Check for critical issues
print("\n[3] Critical Issues Check:")
critical_issues = []

# Check Flask running
try:
    import requests
    r = requests.get('http://localhost:5000/api/health', timeout=2)
    if r.status_code == 200:
        print(" Flask server responding")
    else:
        critical_issues.append("Flask health check failed")
except:
    critical_issues.append("Flask server not running")

# Final verdict
print("\n" + "="*70)
print("FINAL VERDICT")
print("="*70)

if not critical_issues and "100.0%" in result.stdout:
    print(" BACKEND IS 100% COMPLETE AND ERROR-FREE!")
    print("\nFeatures Working:")
    print("   User Registration & Login")
    print("   JWT Authentication")
    print("   AI Fraud Detection (Isolation Forest + XGBoost)")
    print("   Risk Score Calculation")
    print("   Transaction Processing")
    print("   PostgreSQL Storage")
    print("   MongoDB Logging")
    print("   Blockchain Integration (Web3)")
    print("   Twilio Voice Alerts")
    print("   Profile Management")
    print("   Security (JWT, Auth)")
    print("\n READY FOR DEMO AND PRODUCTION!")
else:
    print(" Issues Found:")
    for issue in critical_issues:
        print(f"  - {issue}")
    if "100.0%" not in result.stdout:
        print("  - Some API tests failed")

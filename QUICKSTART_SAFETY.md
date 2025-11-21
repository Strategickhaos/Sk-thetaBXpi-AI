# Quick Start Guide: Model Safety Verification

This guide will help you get started with verifying the safety of your local AI models in under 5 minutes.

## Prerequisites

- Python 3.7 or higher
- Ollama installed (optional - tools will still run without it)

## 1. Basic System Check

Run a basic system check without testing any specific model:

```bash
cd tools
python run_all_checks.py --skip-tests
```

This will check:
- ✓ Model directory and permissions
- ✓ Network isolation
- ✓ Environment configuration
- ✓ Operational safeguards

**Expected output:**
```
============================================================
MASTER SAFETY VERIFICATION SUITE
100 Ways to Verify Local AI Model Safety
============================================================

PHASE 1: MODEL INSPECTION
...
PHASE 2: FIREWALL & ISOLATION
...
PHASE 4: OPERATIONAL AUDIT
...

FINAL REPORT - COMPREHENSIVE SAFETY VERIFICATION
============================================================
Overall Status: ✓ PASS (GREEN)
```

## 2. Model-Specific Verification

If you have a model to test:

```bash
cd tools
python run_all_checks.py --model your-model-name
```

This includes all checks from Step 1 plus:
- ✓ Model behavior tests
- ✓ Safety validation
- ✓ Jailbreak detection
- ✓ Response reproducibility

## 3. Individual Checks

Run specific checks as needed:

### Check Model Internals
```bash
python model_inspector.py --model llama2
```

### Verify Network Isolation
```bash
python firewall_checker.py
```

### Test Model Behavior
```bash
python safety_validator.py llama2
```

### Audit Configuration
```bash
python operational_audit.py
```

## 4. Save Reports

Save a detailed report for documentation:

```bash
python run_all_checks.py --model llama2 --save-report my_report.json
```

## 5. CI/CD Integration

Add to your workflow:

```bash
# In your CI/CD script
cd tools
python run_all_checks.py --skip-tests --json > safety_report.json
```

## Common Scenarios

### Scenario 1: First Time Setup
```bash
# Check if system is configured correctly
cd tools
python operational_audit.py

# Review recommendations and apply them
# Then run full check
python run_all_checks.py --skip-tests
```

### Scenario 2: Before Deploying a Custom Model
```bash
# Test the model thoroughly
cd tools
python run_all_checks.py --model my-custom-model

# If all tests pass, model is ready
```

### Scenario 3: Regular Security Audit
```bash
# Weekly/monthly check
cd tools
python run_all_checks.py --model production-model --save-report audit-$(date +%Y%m%d).json
```

### Scenario 4: Troubleshooting Issues
```bash
# Run individual checks for detailed info
cd tools
python model_inspector.py --model problematic-model
python firewall_checker.py
python safety_validator.py problematic-model
```

## Understanding Results

### Status Indicators

- **✓ (Green checkmark)** = Test passed
- **✗ (Red X)** = Test failed, needs attention
- **⚠ (Yellow warning)** = Warning or recommendation

### Overall Status

- **PASS** = All checks passed, system is secure
- **WARN** = Most checks passed, review recommendations
- **FAIL** = Critical issues detected, immediate action required

### Exit Codes

Scripts return standard exit codes for automation:
- `0` = Success (PASS)
- `1` = Warning (WARN)
- `2` = Failure (FAIL)

## What to Do If Tests Fail

### Ollama Not Found
```bash
# Install Ollama
curl https://ollama.ai/install.sh | sh

# Or on Windows
# Download from https://ollama.ai/download
```

### Network Isolation Issues
Check if Ollama is bound to all interfaces (not secure):
```bash
netstat -tlnp | grep 11434
# Should show 127.0.0.1:11434, not 0.0.0.0:11434
```

### Model Behavior Issues
Review the specific test that failed and investigate:
```bash
# Run individual test with verbose output
python safety_validator.py your-model
```

### Permission Issues
Ensure model directory has correct permissions:
```bash
# Linux/Mac
chmod 700 ~/.ollama/models

# Windows (PowerShell as Admin)
icacls "$env:USERPROFILE\.ollama\models" /inheritance:r /grant:r "$env:USERNAME:(OI)(CI)F"
```

## Getting Help

1. **Read the documentation**: [MODEL_SAFETY.md](MODEL_SAFETY.md) has detailed explanations
2. **Check tool README**: [tools/README.md](tools/README.md) has troubleshooting tips
3. **Review logs**: Scripts provide detailed output about what failed
4. **Run with --json**: Get machine-readable output for analysis

## Best Practices

1. **Run regularly**: Check your system weekly or after any changes
2. **Save reports**: Keep audit trails with dated reports
3. **Address warnings**: Don't ignore warnings - they indicate potential issues
4. **Test before deploy**: Always run full checks before deploying custom models
5. **Version control**: Track your Modelfiles in git

## Next Steps

- Read the full documentation: [MODEL_SAFETY.md](MODEL_SAFETY.md)
- Explore individual tools: [tools/README.md](tools/README.md)
- Integrate into CI/CD pipeline
- Schedule regular automated checks
- Review and apply recommendations

## Quick Reference Commands

```bash
# Full check with model
python run_all_checks.py --model MODEL_NAME

# System check only
python run_all_checks.py --skip-tests

# Save report
python run_all_checks.py --save-report report.json

# JSON output
python run_all_checks.py --json

# Individual checks
python model_inspector.py --model MODEL_NAME
python firewall_checker.py
python safety_validator.py MODEL_NAME
python operational_audit.py
```

---

**Remember**: These tools help verify safety, but security is an ongoing process. Stay informed and run checks regularly!

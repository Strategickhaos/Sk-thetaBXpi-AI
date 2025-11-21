# Safety Verification Tools

This directory contains automated tools for verifying the safety and security of your local AI models. These tools implement the verification methods described in [MODEL_SAFETY.md](../MODEL_SAFETY.md).

## Tools Overview

### 1. `model_inspector.py`
**Model Weights & Internals Verification**

Inspects model files, metadata, and internal configuration to verify model integrity.

```bash
# Basic inspection
python model_inspector.py

# Inspect specific model
python model_inspector.py --model omegaheir_zero

# Verify model file hash
python model_inspector.py --path /path/to/model.gguf

# Output as JSON
python model_inspector.py --model llama2 --json
```

**What it checks:**
- Ollama installation and accessibility
- Available models
- Modelfile contents
- Model file SHA256 hashes
- Running Ollama processes
- Network bindings
- Model directory permissions

### 2. `firewall_checker.py`
**Network Isolation Verification**

Verifies that your local AI setup is properly isolated and cannot make unauthorized network connections.

```bash
# Run firewall checks
python firewall_checker.py

# Output as JSON
python firewall_checker.py --json
```

**What it checks:**
- Localhost-only binding
- Active network connections
- Process permissions
- Firewall rules (Windows)
- Docker isolation (if applicable)

### 3. `safety_validator.py`
**Model Behavior Verification**

Tests model behavior to ensure it's functioning normally and hasn't been compromised.

```bash
# Test a specific model
python safety_validator.py llama2

# Output as JSON
python safety_validator.py omegaheir_zero --json
```

**What it tests:**
- Canary prompt (jailbreak detection)
- Sentience claims
- Math capabilities
- System prompt access
- Harmful content refusal
- Network access claims
- File access claims
- Response reproducibility

**Note:** This tool actually runs prompts against your model, so it may take a few minutes to complete.

### 4. `operational_audit.py`
**Configuration & Safeguards Audit**

Audits your operational configuration and security practices.

```bash
# Run operational audit
python operational_audit.py

# Output as JSON
python operational_audit.py --json
```

**What it checks:**
- Model directory permissions
- Environment variables
- Modelfile backup practices
- Parameter safety
- Factory reset capability
- Base model preservation
- Hash verification practices

### 5. `run_all_checks.py`
**Master Verification Script**

Runs all verification tools in sequence and generates a comprehensive safety report.

```bash
# Run all checks (without model tests)
python run_all_checks.py

# Run all checks including model tests
python run_all_checks.py --model llama2

# Skip model behavior tests
python run_all_checks.py --model llama2 --skip-tests

# Save report to file
python run_all_checks.py --model llama2 --save-report my_safety_report.json

# Output as JSON
python run_all_checks.py --json
```

**Phases:**
1. Model Inspection
2. Firewall & Isolation
3. Safety Validation (optional, requires model)
4. Operational Audit

## Quick Start

### First Time Setup

1. Make sure Ollama is installed:
   ```bash
   ollama --version
   ```

2. Install Python dependencies (if any):
   ```bash
   pip install -r requirements.txt
   ```

3. Make scripts executable (Linux/Mac):
   ```bash
   chmod +x *.py
   ```

### Run Complete Verification

```bash
# If you have a model to test
python run_all_checks.py --model your-model-name

# If you just want to check the system
python run_all_checks.py --skip-tests
```

### Run Individual Checks

```bash
# Check model internals
python model_inspector.py --model llama2

# Check network isolation
python firewall_checker.py

# Test model behavior
python safety_validator.py llama2

# Audit configuration
python operational_audit.py
```

## Understanding Results

### Pass/Fail Status

- **✓ PASS**: All checks passed, system is secure
- **⚠ WARN**: Most checks passed, some recommendations to address
- **✗ FAIL**: Critical issues detected, immediate action required

### Exit Codes

All scripts use standard exit codes:
- `0`: All checks passed (PASS)
- `1`: Some checks failed or warnings present (WARN)
- `2`: Critical failures (FAIL)

### JSON Output

All tools support `--json` flag for machine-readable output:

```bash
python run_all_checks.py --json > report.json
```

## Common Issues

### "Ollama not found"
Make sure Ollama is installed and in your PATH.

### "Model not found"
List available models: `ollama list`

### "Permission denied"
Run with appropriate permissions or check file/directory ownership.

### "Network check failed"
Some network checks require elevated permissions:
- Linux: Run with `sudo` if needed
- Windows: Run as Administrator if needed

## Best Practices

1. **Run regularly**: Schedule checks weekly or after any system changes
2. **Test before deployment**: Run full checks before deploying custom models
3. **Keep reports**: Save reports for audit trails
4. **Address warnings**: Don't ignore warnings, they indicate potential issues
5. **Version control**: Track changes to Modelfiles and configurations

## Security Notes

These tools are designed to:
- ✓ Verify model integrity
- ✓ Confirm network isolation
- ✓ Test normal behavior
- ✓ Audit security practices

They do NOT:
- ✗ Provide 100% security guarantee
- ✗ Detect all possible vulnerabilities
- ✗ Replace human security review
- ✗ Protect against physical access attacks

## Integration

### CI/CD Integration

Add to your CI/CD pipeline:

```yaml
# Example GitHub Actions
- name: Run Safety Checks
  run: |
    cd tools
    python run_all_checks.py --skip-tests --json > safety_report.json
```

### Scheduled Checks

Add to cron (Linux/Mac):
```bash
# Run daily at 2 AM
0 2 * * * cd /path/to/tools && python run_all_checks.py --skip-tests
```

Add to Task Scheduler (Windows):
```powershell
# Run daily
schtasks /create /tn "AI Safety Check" /tr "python C:\path\to\tools\run_all_checks.py --skip-tests" /sc daily
```

## Troubleshooting

### Script fails with ImportError
Make sure you're running from the tools directory:
```bash
cd tools
python run_all_checks.py
```

### Model tests timeout
Increase timeout or skip tests:
```bash
python run_all_checks.py --skip-tests
```

### Permission errors on Windows
Run PowerShell or Command Prompt as Administrator.

### Permission errors on Linux
Some checks require sudo:
```bash
sudo python firewall_checker.py
```

## Contributing

To add new checks:
1. Follow the existing code structure
2. Add appropriate error handling
3. Include clear output messages
4. Support `--json` output format
5. Document in this README

## Support

For issues or questions:
1. Check [MODEL_SAFETY.md](../MODEL_SAFETY.md) for detailed information
2. Review this README
3. Check script output for specific error messages
4. Review logs and reports

## License

These tools are provided as-is for security verification purposes. See [LICENSE](../LICENSE) for details.

---

**Remember**: These tools help verify safety, but security is a continuous process. Regular checks and staying informed about best practices are essential.

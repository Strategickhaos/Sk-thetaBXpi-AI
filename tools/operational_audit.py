#!/usr/bin/env python3
"""
Operational Audit - System Configuration and Safeguards Check
Part of the 100 Ways to Verify Local AI Model Safety toolkit

This script audits operational safeguards and configuration settings
to ensure best practices are being followed.
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime


class OperationalAuditor:
    """Audit operational safeguards and configuration"""
    
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "checks_passed": 0,
            "checks_failed": 0,
            "recommendations": [],
            "details": {}
        }
    
    def check_model_directory_permissions(self):
        """Check model directory permissions (Test 61-62)"""
        print("\n=== Checking Model Directory Permissions ===")
        
        if sys.platform == "win32":
            model_dir = Path.home() / ".ollama" / "models"
        else:
            model_dir = Path.home() / ".ollama" / "models"
        
        if not model_dir.exists():
            print("⚠ Model directory does not exist")
            self.results["recommendations"].append("Create model directory")
            return False
        
        try:
            # Check basic permissions
            readable = os.access(model_dir, os.R_OK)
            writable = os.access(model_dir, os.W_OK)
            
            print(f"Directory: {model_dir}")
            print(f"Readable: {readable}")
            print(f"Writable: {writable}")
            
            if readable:
                print("✓ Model directory is readable")
                self.results["checks_passed"] += 1
            else:
                print("✗ Model directory is not readable")
                self.results["checks_failed"] += 1
            
            # Check if files are read-only after creation (Test 29)
            model_files = list(model_dir.rglob("*"))
            writable_count = sum(1 for f in model_files if f.is_file() and os.access(f, os.W_OK))
            
            if writable_count > 0:
                print(f"⚠ Found {writable_count} writable model files")
                self.results["recommendations"].append(
                    "Consider making model files read-only for security"
                )
            else:
                print("✓ All model files are read-only")
                self.results["checks_passed"] += 1
            
            self.results["details"]["model_directory"] = {
                "path": str(model_dir),
                "readable": readable,
                "writable": writable,
                "total_files": len(model_files),
                "writable_files": writable_count
            }
            
            return True
        except Exception as e:
            print(f"✗ Error checking permissions: {e}")
            self.results["checks_failed"] += 1
            return False
    
    def check_environment_variables(self):
        """Check Ollama environment variables (Tests 67-68, 40)"""
        print("\n=== Checking Environment Variables ===")
        
        important_vars = {
            "OLLAMA_MAX_LOADED_MODELS": ("1", "Limit loaded models for memory management"),
            "OLLAMA_KEEP_ALIVE": ("5m", "Unload models quickly when not in use"),
            "OLLAMA_NUM_PARALLEL": ("1", "Prevent parallel request confusion"),
            "OLLAMA_DEBUG": (None, "Enable for troubleshooting (disable in production)"),
            "OLLAMA_NO_GPU": (None, "Force CPU-only mode if needed")
        }
        
        for var, (recommended, description) in important_vars.items():
            value = os.environ.get(var)
            print(f"\n{var}:")
            print(f"  Current: {value if value else 'Not set'}")
            print(f"  Description: {description}")
            
            if recommended:
                if value == recommended:
                    print(f"  ✓ Set to recommended value: {recommended}")
                    self.results["checks_passed"] += 1
                else:
                    print(f"  ⚠ Recommended value: {recommended}")
                    self.results["recommendations"].append(
                        f"Set {var}={recommended} - {description}"
                    )
            
            self.results["details"][var] = value
        
        return True
    
    def check_modelfile_backup(self):
        """Check if Modelfiles are backed up (Tests 70-71)"""
        print("\n=== Checking Modelfile Backups ===")
        
        # Look for Modelfiles in current directory
        modelfiles = list(Path.cwd().glob("*Modelfile*"))
        
        if not modelfiles:
            print("⚠ No Modelfiles found in current directory")
            self.results["recommendations"].append(
                "Create and version control your Modelfiles"
            )
            return False
        
        print(f"Found {len(modelfiles)} Modelfile(s):")
        for mf in modelfiles:
            print(f"  - {mf.name}")
        
        # Check if in git repo
        try:
            result = subprocess.run(
                ["git", "status"],
                capture_output=True,
                text=True,
                timeout=5,
                cwd=Path.cwd()
            )
            
            if result.returncode == 0:
                print("✓ In git repository")
                
                # Check if Modelfiles are tracked
                tracked = []
                for mf in modelfiles:
                    result = subprocess.run(
                        ["git", "ls-files", "--error-unmatch", str(mf)],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    if result.returncode == 0:
                        tracked.append(mf.name)
                
                if tracked:
                    print(f"✓ {len(tracked)} Modelfile(s) tracked in git")
                    self.results["checks_passed"] += 1
                else:
                    print("⚠ Modelfiles not tracked in git")
                    self.results["recommendations"].append(
                        "Add Modelfiles to git for version control"
                    )
            else:
                print("⚠ Not in a git repository")
                self.results["recommendations"].append(
                    "Initialize git repo and track Modelfiles"
                )
        except FileNotFoundError:
            print("⚠ Git not installed or not in PATH")
            self.results["recommendations"].append(
                "Install git and version control Modelfiles"
            )
        except Exception as e:
            print(f"⚠ Error checking git status: {e}")
        
        return True
    
    def check_parameter_safety(self):
        """Check for safe model parameters (Tests 72-75)"""
        print("\n=== Checking Parameter Safety ===")
        
        # This would require parsing Modelfiles or checking model configs
        # For now, provide recommendations
        print("\nRecommended Parameter Ranges:")
        print("  temperature: 0.7 - 1.0 (never > 1.2)")
        print("  top_p: 0.9 - 0.95")
        print("  repeat_penalty: 1.0 - 1.2 (never < 1.0)")
        print("  keep stop tokens: Do not remove default stop tokens")
        
        self.results["recommendations"].append(
            "Audit Modelfile parameters to ensure they're in safe ranges"
        )
        
        print("\n⚠ Manual review required for parameter safety")
        return True
    
    def check_factory_reset_capability(self):
        """Check if factory reset script exists (Test 77)"""
        print("\n=== Checking Factory Reset Capability ===")
        
        # Look for reset scripts
        reset_scripts = [
            "factory_reset.sh",
            "reset_models.sh",
            "factory_reset.ps1",
            "reset_models.ps1"
        ]
        
        found_scripts = [s for s in reset_scripts if Path(s).exists()]
        
        if found_scripts:
            print(f"✓ Found reset script(s): {', '.join(found_scripts)}")
            self.results["checks_passed"] += 1
        else:
            print("⚠ No factory reset script found")
            self.results["recommendations"].append(
                "Create a factory reset script to quickly remove all custom models"
            )
            
            # Provide example script
            print("\nExample factory reset script (Linux/Mac):")
            print("#!/bin/bash")
            print("ollama list | grep -v 'NAME' | awk '{print $1}' | xargs -I {} ollama rm {}")
            
            print("\nExample factory reset script (Windows):")
            print("ollama list | Select-String -NotMatch 'NAME' | ")
            print("  ForEach-Object { ($_ -split '\\s+')[0] } | ")
            print("  ForEach-Object { ollama rm $_ }")
        
        return True
    
    def check_base_model_preservation(self):
        """Check if base models are preserved (Test 78)"""
        print("\n=== Checking Base Model Preservation ===")
        
        try:
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                models = result.stdout.strip().split('\n')[1:]  # Skip header
                
                # Look for common base models
                base_models = [
                    "llama2", "llama3", "mistral", "mixtral",
                    "phi", "gemma", "codellama"
                ]
                
                found_base = []
                custom_models = []
                
                for model_line in models:
                    if model_line.strip():
                        model_name = model_line.split()[0].lower()
                        if any(base in model_name for base in base_models):
                            found_base.append(model_name)
                        else:
                            custom_models.append(model_name)
                
                if found_base:
                    print(f"✓ Found {len(found_base)} base model(s):")
                    for model in found_base:
                        print(f"    - {model}")
                    self.results["checks_passed"] += 1
                else:
                    print("⚠ No standard base models found")
                    self.results["recommendations"].append(
                        "Keep at least one base model as reference"
                    )
                
                if custom_models:
                    print(f"\nCustom models: {len(custom_models)}")
                    for model in custom_models:
                        print(f"    - {model}")
                
                self.results["details"]["base_models"] = found_base
                self.results["details"]["custom_models"] = custom_models
                
        except Exception as e:
            print(f"✗ Error checking models: {e}")
            self.results["checks_failed"] += 1
        
        return True
    
    def check_hash_verification(self):
        """Check for hash verification practices (Test 79)"""
        print("\n=== Checking Hash Verification ===")
        
        # Look for .sha256 files
        sha_files = list(Path.home().glob(".ollama/**/*.sha256"))
        
        if sha_files:
            print(f"✓ Found {len(sha_files)} SHA256 checksum file(s)")
            self.results["checks_passed"] += 1
        else:
            print("⚠ No SHA256 checksum files found")
            self.results["recommendations"].append(
                "Generate SHA256 checksums for downloaded models: sha256sum model.gguf > model.gguf.sha256"
            )
        
        return True
    
    def generate_audit_report(self):
        """Generate a comprehensive audit report"""
        print("\n" + "=" * 60)
        print("AUDIT REPORT")
        print("=" * 60)
        
        print(f"\nTimestamp: {self.results['timestamp']}")
        print(f"✓ Checks Passed: {self.results['checks_passed']}")
        print(f"✗ Checks Failed: {self.results['checks_failed']}")
        print(f"⚠ Recommendations: {len(self.results['recommendations'])}")
        
        if self.results['recommendations']:
            print("\n=== RECOMMENDATIONS ===")
            for i, rec in enumerate(self.results['recommendations'], 1):
                print(f"{i}. {rec}")
        
        if self.results['checks_failed'] == 0:
            print("\n✓ Operational audit complete!")
            print("System configuration follows security best practices.")
        else:
            print("\n⚠ Some issues detected. Review recommendations above.")
        
        return self.results
    
    def run_all_checks(self):
        """Run all operational audit checks"""
        print("=" * 60)
        print("OPERATIONAL AUDITOR - Configuration & Safeguards Check")
        print("=" * 60)
        
        self.check_model_directory_permissions()
        self.check_environment_variables()
        self.check_modelfile_backup()
        self.check_parameter_safety()
        self.check_factory_reset_capability()
        self.check_base_model_preservation()
        self.check_hash_verification()
        
        return self.generate_audit_report()


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Audit operational safeguards and configuration"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )
    
    args = parser.parse_args()
    
    auditor = OperationalAuditor()
    results = auditor.run_all_checks()
    
    if args.json:
        print("\n" + json.dumps(results, indent=2))
    
    # Exit with non-zero if any checks failed
    sys.exit(1 if results['checks_failed'] > 0 else 0)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Model Inspector - Automated Model Weight & Internals Verification
Part of the 100 Ways to Verify Local AI Model Safety toolkit

This script automates inspection of model weights, metadata, and internals
to verify model integrity and transparency.
"""

import os
import sys
import subprocess
import hashlib
import json
from pathlib import Path


class ModelInspector:
    """Inspect and verify local AI model internals"""
    
    def __init__(self, model_name=None, model_path=None):
        self.model_name = model_name
        self.model_path = model_path
        self.results = {
            "checks_passed": 0,
            "checks_failed": 0,
            "warnings": [],
            "details": {}
        }
    
    def check_ollama_installation(self):
        """Check if ollama is installed and accessible"""
        try:
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                print("✓ Ollama is installed and accessible")
                self.results["checks_passed"] += 1
                self.results["details"]["ollama_installed"] = True
                return True
            else:
                print("✗ Ollama is not responding correctly")
                self.results["checks_failed"] += 1
                self.results["details"]["ollama_installed"] = False
                return False
        except FileNotFoundError:
            print("✗ Ollama is not installed")
            self.results["checks_failed"] += 1
            self.results["details"]["ollama_installed"] = False
            return False
        except Exception as e:
            print(f"✗ Error checking Ollama: {e}")
            self.results["checks_failed"] += 1
            return False
    
    def list_models(self):
        """List all available models"""
        try:
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                print("\n=== Available Models ===")
                print(result.stdout)
                self.results["details"]["models"] = result.stdout
                return True
            return False
        except Exception as e:
            print(f"✗ Error listing models: {e}")
            return False
    
    def show_modelfile(self):
        """Show the Modelfile for the specified model"""
        if not self.model_name:
            print("⚠ No model name specified, skipping Modelfile check")
            self.results["warnings"].append("No model name specified")
            return False
        
        try:
            result = subprocess.run(
                ["ollama", "show", "--modelfile", self.model_name],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                print(f"\n=== Modelfile for {self.model_name} ===")
                print(result.stdout)
                self.results["details"]["modelfile"] = result.stdout
                self.results["checks_passed"] += 1
                return True
            else:
                print(f"✗ Could not retrieve Modelfile for {self.model_name}")
                self.results["checks_failed"] += 1
                return False
        except Exception as e:
            print(f"✗ Error showing Modelfile: {e}")
            self.results["checks_failed"] += 1
            return False
    
    def check_model_hash(self):
        """Calculate and display SHA256 hash of model file"""
        if not self.model_path:
            print("⚠ No model path specified, skipping hash check")
            self.results["warnings"].append("No model path specified for hash check")
            return False
        
        model_file = Path(self.model_path)
        if not model_file.exists():
            print(f"✗ Model file not found: {self.model_path}")
            self.results["checks_failed"] += 1
            return False
        
        try:
            print(f"\n=== Calculating SHA256 for {model_file.name} ===")
            sha256_hash = hashlib.sha256()
            with open(model_file, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            
            hash_value = sha256_hash.hexdigest()
            print(f"SHA256: {hash_value}")
            self.results["details"]["model_hash"] = hash_value
            self.results["checks_passed"] += 1
            return True
        except Exception as e:
            print(f"✗ Error calculating hash: {e}")
            self.results["checks_failed"] += 1
            return False
    
    def check_running_processes(self):
        """Check for running Ollama processes"""
        try:
            if sys.platform == "win32":
                result = subprocess.run(
                    ["tasklist", "/FI", "IMAGENAME eq ollama.exe"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
            else:
                result = subprocess.run(
                    ["pgrep", "-l", "ollama"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
            
            print("\n=== Ollama Processes ===")
            if result.returncode == 0 and result.stdout.strip():
                print(result.stdout)
                self.results["details"]["running_processes"] = result.stdout
            else:
                print("No Ollama processes currently running")
                self.results["details"]["running_processes"] = "None"
            
            self.results["checks_passed"] += 1
            return True
        except Exception as e:
            print(f"⚠ Could not check processes: {e}")
            self.results["warnings"].append(f"Process check failed: {e}")
            return False
    
    def check_network_bindings(self):
        """Check network bindings for Ollama"""
        try:
            if sys.platform == "win32":
                result = subprocess.run(
                    ["netstat", "-ano"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                # Filter for port 11434
                lines = [line for line in result.stdout.split('\n') if '11434' in line]
            else:
                result = subprocess.run(
                    ["netstat", "-tlnp"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                lines = [line for line in result.stdout.split('\n') if '11434' in line]
            
            print("\n=== Network Bindings (Port 11434) ===")
            if lines:
                for line in lines:
                    print(line)
                    # Check if binding is localhost only
                    if '127.0.0.1:11434' in line or '::1:11434' in line:
                        print("✓ Binding is localhost only (secure)")
                        self.results["checks_passed"] += 1
                    elif '0.0.0.0:11434' in line or ':::11434' in line:
                        print("⚠ WARNING: Binding to all interfaces (not secure)")
                        self.results["warnings"].append("Ollama bound to all interfaces")
                        self.results["checks_failed"] += 1
                self.results["details"]["network_bindings"] = '\n'.join(lines)
            else:
                print("No bindings found on port 11434")
                self.results["details"]["network_bindings"] = "None"
            
            return True
        except Exception as e:
            print(f"⚠ Could not check network bindings: {e}")
            self.results["warnings"].append(f"Network check failed: {e}")
            return False
    
    def check_model_directory(self):
        """Check model directory permissions and contents"""
        if sys.platform == "win32":
            model_dir = Path.home() / ".ollama" / "models"
        else:
            model_dir = Path.home() / ".ollama" / "models"
        
        print(f"\n=== Model Directory ===")
        print(f"Location: {model_dir}")
        
        if model_dir.exists():
            print("✓ Directory exists")
            
            # Check permissions
            if os.access(model_dir, os.R_OK):
                print("✓ Directory is readable")
            else:
                print("✗ Directory is not readable")
                self.results["checks_failed"] += 1
            
            # List contents
            try:
                items = list(model_dir.rglob("*"))
                print(f"Total items: {len(items)}")
                self.results["details"]["model_directory"] = str(model_dir)
                self.results["details"]["model_count"] = len(items)
                self.results["checks_passed"] += 1
            except Exception as e:
                print(f"✗ Error listing directory: {e}")
                self.results["checks_failed"] += 1
        else:
            print("✗ Model directory does not exist")
            self.results["checks_failed"] += 1
    
    def run_all_checks(self):
        """Run all inspection checks"""
        print("=" * 60)
        print("MODEL INSPECTOR - Safety Verification Suite")
        print("=" * 60)
        
        self.check_ollama_installation()
        self.list_models()
        self.show_modelfile()
        self.check_model_hash()
        self.check_running_processes()
        self.check_network_bindings()
        self.check_model_directory()
        
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print(f"✓ Checks Passed: {self.results['checks_passed']}")
        print(f"✗ Checks Failed: {self.results['checks_failed']}")
        print(f"⚠ Warnings: {len(self.results['warnings'])}")
        
        if self.results['warnings']:
            print("\nWarnings:")
            for warning in self.results['warnings']:
                print(f"  - {warning}")
        
        return self.results


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Inspect and verify local AI model safety"
    )
    parser.add_argument(
        "--model",
        help="Name of the model to inspect (e.g., omegaheir_zero)"
    )
    parser.add_argument(
        "--path",
        help="Path to model file (.gguf) for hash verification"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )
    
    args = parser.parse_args()
    
    inspector = ModelInspector(model_name=args.model, model_path=args.path)
    results = inspector.run_all_checks()
    
    if args.json:
        print("\n" + json.dumps(results, indent=2))
    
    # Exit with non-zero if any checks failed
    sys.exit(1 if results['checks_failed'] > 0 else 0)


if __name__ == "__main__":
    main()

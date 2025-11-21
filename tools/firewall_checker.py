#!/usr/bin/env python3
"""
Firewall Checker - Network Isolation Verification
Part of the 100 Ways to Verify Local AI Model Safety toolkit

This script verifies that Ollama and local models have proper network
isolation and cannot make unauthorized external connections.
"""

import sys
import subprocess
import socket
import json
from datetime import datetime


class FirewallChecker:
    """Verify network isolation and firewall configuration"""
    
    def __init__(self):
        self.results = {
            "checks_passed": 0,
            "checks_failed": 0,
            "warnings": [],
            "details": {},
            "timestamp": datetime.now().isoformat()
        }
    
    def check_localhost_binding(self):
        """Verify Ollama is only bound to localhost"""
        print("\n=== Checking Localhost Binding ===")
        
        try:
            # Check if port 11434 is listening
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('127.0.0.1', 11434))
            sock.close()
            
            if result == 0:
                print("✓ Port 11434 is accessible on localhost")
                self.results["checks_passed"] += 1
                self.results["details"]["localhost_accessible"] = True
            else:
                print("⚠ Port 11434 is not accessible (Ollama may not be running)")
                self.results["warnings"].append("Ollama service not detected")
                self.results["details"]["localhost_accessible"] = False
            
            # Try to connect from external interface (should fail in secure setup)
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                # Try to get actual IP
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                local_ip = s.getsockname()[0]
                s.close()
                
                result = sock.connect_ex((local_ip, 11434))
                sock.close()
                
                if result != 0:
                    print(f"✓ Port 11434 is NOT accessible from {local_ip} (secure)")
                    self.results["checks_passed"] += 1
                    self.results["details"]["external_blocked"] = True
                else:
                    print(f"✗ WARNING: Port 11434 IS accessible from {local_ip}")
                    self.results["checks_failed"] += 1
                    self.results["details"]["external_blocked"] = False
                    self.results["warnings"].append(f"Port exposed on {local_ip}")
            except Exception as e:
                print(f"⚠ Could not check external access: {e}")
                self.results["warnings"].append("External access check failed")
            
            return True
        except Exception as e:
            print(f"✗ Error checking localhost binding: {e}")
            self.results["checks_failed"] += 1
            return False
    
    def check_active_connections(self):
        """Check for active network connections from Ollama"""
        print("\n=== Checking Active Connections ===")
        
        try:
            if sys.platform == "win32":
                result = subprocess.run(
                    ["netstat", "-ano"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
            else:
                result = subprocess.run(
                    ["netstat", "-tunapl"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
            
            # Filter for Ollama-related connections
            lines = result.stdout.split('\n')
            ollama_connections = [
                line for line in lines 
                if '11434' in line or 'ollama' in line.lower()
            ]
            
            print(f"Found {len(ollama_connections)} Ollama-related connections")
            
            # Check for external connections
            external_connections = []
            for line in ollama_connections:
                if '127.0.0.1' not in line and '::1' not in line:
                    external_connections.append(line)
            
            if external_connections:
                print("⚠ WARNING: External connections detected:")
                for conn in external_connections:
                    print(f"  {conn}")
                self.results["warnings"].append("External connections detected")
                self.results["details"]["external_connections"] = external_connections
            else:
                print("✓ No external connections detected")
                self.results["checks_passed"] += 1
                self.results["details"]["external_connections"] = []
            
            return True
        except Exception as e:
            print(f"⚠ Error checking connections: {e}")
            self.results["warnings"].append(f"Connection check failed: {e}")
            return False
    
    def check_process_permissions(self):
        """Check if Ollama is running with appropriate permissions"""
        print("\n=== Checking Process Permissions ===")
        
        try:
            if sys.platform == "win32":
                result = subprocess.run(
                    ["tasklist", "/FI", "IMAGENAME eq ollama.exe", "/V"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                
                if "ollama.exe" in result.stdout:
                    print("✓ Ollama process found")
                    
                    # Check if running as SYSTEM
                    if "SYSTEM" in result.stdout:
                        print("⚠ WARNING: Ollama is running as SYSTEM")
                        self.results["warnings"].append("Running as SYSTEM user")
                        self.results["details"]["running_as_system"] = True
                    else:
                        print("✓ Ollama is not running as SYSTEM")
                        self.results["checks_passed"] += 1
                        self.results["details"]["running_as_system"] = False
                else:
                    print("⚠ Ollama process not found")
                    self.results["warnings"].append("Ollama not running")
            else:
                result = subprocess.run(
                    ["ps", "aux"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                
                ollama_lines = [line for line in result.stdout.split('\n') if 'ollama' in line]
                
                if ollama_lines:
                    print("✓ Ollama process found")
                    
                    # Check if running as root
                    root_processes = [line for line in ollama_lines if line.startswith('root')]
                    if root_processes:
                        print("⚠ WARNING: Ollama is running as root")
                        self.results["warnings"].append("Running as root user")
                        self.results["details"]["running_as_root"] = True
                    else:
                        print("✓ Ollama is not running as root")
                        self.results["checks_passed"] += 1
                        self.results["details"]["running_as_root"] = False
                else:
                    print("⚠ Ollama process not found")
                    self.results["warnings"].append("Ollama not running")
            
            return True
        except Exception as e:
            print(f"⚠ Error checking permissions: {e}")
            self.results["warnings"].append(f"Permission check failed: {e}")
            return False
    
    def check_firewall_rules(self):
        """Check firewall rules (Windows only)"""
        print("\n=== Checking Firewall Rules ===")
        
        if sys.platform != "win32":
            print("⚠ Firewall rule check only available on Windows")
            self.results["warnings"].append("Not on Windows - skipping firewall check")
            return False
        
        try:
            result = subprocess.run(
                ["netsh", "advfirewall", "firewall", "show", "rule", "name=all"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                # Look for Ollama-related rules
                lines = result.stdout.split('\n')
                ollama_rules = []
                current_rule = {}
                
                for line in lines:
                    if line.startswith('Rule Name:'):
                        if current_rule and 'ollama' in str(current_rule).lower():
                            ollama_rules.append(current_rule)
                        current_rule = {'name': line.split(':', 1)[1].strip()}
                    elif ':' in line and current_rule:
                        key, value = line.split(':', 1)
                        current_rule[key.strip()] = value.strip()
                
                if current_rule and 'ollama' in str(current_rule).lower():
                    ollama_rules.append(current_rule)
                
                if ollama_rules:
                    print(f"Found {len(ollama_rules)} Ollama firewall rules:")
                    for rule in ollama_rules:
                        print(f"  - {rule.get('name', 'Unknown')}")
                    self.results["details"]["firewall_rules"] = ollama_rules
                    self.results["checks_passed"] += 1
                else:
                    print("⚠ No Ollama-specific firewall rules found")
                    self.results["warnings"].append("No firewall rules configured")
                    self.results["details"]["firewall_rules"] = []
            
            return True
        except Exception as e:
            print(f"⚠ Error checking firewall rules: {e}")
            self.results["warnings"].append(f"Firewall check failed: {e}")
            return False
    
    def check_docker_isolation(self):
        """Check if running in Docker with network isolation"""
        print("\n=== Checking Docker Isolation ===")
        
        try:
            # Check if running in Docker
            if sys.platform != "win32":
                result = subprocess.run(
                    ["cat", "/proc/1/cgroup"],
                    capture_output=True,
                    text=True,
                    timeout=2
                )
                
                if "docker" in result.stdout:
                    print("✓ Running in Docker container")
                    self.results["details"]["in_docker"] = True
                    
                    # Check network mode
                    result = subprocess.run(
                        ["ip", "addr"],
                        capture_output=True,
                        text=True,
                        timeout=2
                    )
                    
                    if result.returncode == 0:
                        # Check for bridge network
                        if "172." in result.stdout or "docker" in result.stdout:
                            print("⚠ Using Docker bridge network (not isolated)")
                            self.results["warnings"].append("Not using --network none")
                        else:
                            print("✓ Docker network appears isolated")
                            self.results["checks_passed"] += 1
                else:
                    print("⚠ Not running in Docker")
                    self.results["details"]["in_docker"] = False
            else:
                print("⚠ Docker check not available on Windows")
                self.results["warnings"].append("Docker check not available")
            
            return True
        except Exception as e:
            print(f"⚠ Error checking Docker isolation: {e}")
            self.results["warnings"].append(f"Docker check failed: {e}")
            return False
    
    def run_all_checks(self):
        """Run all firewall and isolation checks"""
        print("=" * 60)
        print("FIREWALL CHECKER - Network Isolation Verification")
        print("=" * 60)
        
        self.check_localhost_binding()
        self.check_active_connections()
        self.check_process_permissions()
        self.check_firewall_rules()
        self.check_docker_isolation()
        
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
        
        if self.results['checks_failed'] == 0 and len(self.results['warnings']) == 0:
            print("\n✓ All network isolation checks passed!")
            print("Your system appears to be properly isolated.")
        else:
            print("\n⚠ Some issues detected. Review warnings above.")
        
        return self.results


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Verify network isolation and firewall configuration"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )
    
    args = parser.parse_args()
    
    checker = FirewallChecker()
    results = checker.run_all_checks()
    
    if args.json:
        print("\n" + json.dumps(results, indent=2))
    
    # Exit with non-zero if any checks failed
    sys.exit(1 if results['checks_failed'] > 0 else 0)


if __name__ == "__main__":
    main()

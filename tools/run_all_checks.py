#!/usr/bin/env python3
"""
Run All Checks - Master Script for Complete Safety Verification
Part of the 100 Ways to Verify Local AI Model Safety toolkit

This script runs all verification tools in sequence and generates
a comprehensive safety report.
"""

import sys
import json
from datetime import datetime
from pathlib import Path

# Import all checker modules
try:
    from model_inspector import ModelInspector
    from firewall_checker import FirewallChecker
    from safety_validator import SafetyValidator
    from operational_audit import OperationalAuditor
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure all checker scripts are in the same directory")
    sys.exit(1)


class MasterChecker:
    """Run all safety checks and generate comprehensive report"""
    
    def __init__(self, model_name=None, model_path=None, skip_model_tests=False):
        self.model_name = model_name
        self.model_path = model_path
        self.skip_model_tests = skip_model_tests
        self.report = {
            "timestamp": datetime.now().isoformat(),
            "model": model_name,
            "results": {},
            "overall_status": "unknown",
            "total_checks": 0,
            "total_passed": 0,
            "total_failed": 0,
            "total_warnings": 0
        }
    
    def run_model_inspection(self):
        """Run model inspection checks"""
        print("\n" + "=" * 70)
        print("PHASE 1: MODEL INSPECTION")
        print("=" * 70)
        
        inspector = ModelInspector(
            model_name=self.model_name,
            model_path=self.model_path
        )
        results = inspector.run_all_checks()
        
        self.report["results"]["model_inspection"] = results
        self.report["total_checks"] += results["checks_passed"] + results["checks_failed"]
        self.report["total_passed"] += results["checks_passed"]
        self.report["total_failed"] += results["checks_failed"]
        self.report["total_warnings"] += len(results["warnings"])
        
        return results
    
    def run_firewall_checks(self):
        """Run firewall and isolation checks"""
        print("\n" + "=" * 70)
        print("PHASE 2: FIREWALL & ISOLATION")
        print("=" * 70)
        
        checker = FirewallChecker()
        results = checker.run_all_checks()
        
        self.report["results"]["firewall"] = results
        self.report["total_checks"] += results["checks_passed"] + results["checks_failed"]
        self.report["total_passed"] += results["checks_passed"]
        self.report["total_failed"] += results["checks_failed"]
        self.report["total_warnings"] += len(results["warnings"])
        
        return results
    
    def run_safety_validation(self):
        """Run safety validation tests"""
        if self.skip_model_tests or not self.model_name:
            print("\n" + "=" * 70)
            print("PHASE 3: SAFETY VALIDATION - SKIPPED")
            print("=" * 70)
            print("Skipping model behavior tests (no model specified or --skip-tests flag used)")
            return None
        
        print("\n" + "=" * 70)
        print("PHASE 3: SAFETY VALIDATION")
        print("=" * 70)
        print("Note: This phase requires running actual prompts and may take a few minutes")
        
        validator = SafetyValidator(model_name=self.model_name)
        results = validator.run_all_tests()
        
        self.report["results"]["safety_validation"] = results
        self.report["total_checks"] += results["tests_passed"] + results["tests_failed"]
        self.report["total_passed"] += results["tests_passed"]
        self.report["total_failed"] += results["tests_failed"]
        self.report["total_warnings"] += len(results["warnings"])
        
        return results
    
    def run_operational_audit(self):
        """Run operational audit"""
        print("\n" + "=" * 70)
        print("PHASE 4: OPERATIONAL AUDIT")
        print("=" * 70)
        
        auditor = OperationalAuditor()
        results = auditor.run_all_checks()
        
        self.report["results"]["operational_audit"] = results
        self.report["total_checks"] += results["checks_passed"] + results["checks_failed"]
        self.report["total_passed"] += results["checks_passed"]
        self.report["total_failed"] += results["checks_failed"]
        # Recommendations are different from warnings
        self.report["total_warnings"] += len(results["recommendations"])
        
        return results
    
    def generate_final_report(self):
        """Generate final comprehensive report"""
        print("\n" + "=" * 70)
        print("FINAL REPORT - COMPREHENSIVE SAFETY VERIFICATION")
        print("=" * 70)
        
        print(f"\nTimestamp: {self.report['timestamp']}")
        if self.model_name:
            print(f"Model: {self.model_name}")
        
        print(f"\n{'='*70}")
        print("OVERALL STATISTICS")
        print(f"{'='*70}")
        print(f"Total Checks Run: {self.report['total_checks']}")
        print(f"✓ Passed: {self.report['total_passed']}")
        print(f"✗ Failed: {self.report['total_failed']}")
        print(f"⚠ Warnings/Recommendations: {self.report['total_warnings']}")
        
        # Calculate pass rate
        if self.report['total_checks'] > 0:
            pass_rate = (self.report['total_passed'] / self.report['total_checks']) * 100
            print(f"\nPass Rate: {pass_rate:.1f}%")
        
        # Determine overall status
        if self.report['total_failed'] == 0:
            self.report['overall_status'] = "PASS"
            status_icon = "✓"
            status_color = "GREEN"
        elif self.report['total_failed'] <= 2:
            self.report['overall_status'] = "WARN"
            status_icon = "⚠"
            status_color = "YELLOW"
        else:
            self.report['overall_status'] = "FAIL"
            status_icon = "✗"
            status_color = "RED"
        
        print(f"\n{'='*70}")
        print(f"OVERALL STATUS: {status_icon} {self.report['overall_status']} ({status_color})")
        print(f"{'='*70}")
        
        # Provide summary and recommendations
        if self.report['overall_status'] == "PASS":
            print("\n✓ Excellent! Your system passes all safety checks.")
            print("Your local AI model setup follows security best practices.")
            print("\nYou can be confident that:")
            print("  • Your models are isolated and cannot access the network")
            print("  • No unauthorized processes are running")
            print("  • Model behavior is normal and expected")
            print("  • Operational safeguards are in place")
        elif self.report['overall_status'] == "WARN":
            print("\n⚠ Your system is mostly secure, but some recommendations should be addressed.")
            print("Review the warnings and recommendations above.")
        else:
            print("\n✗ Security issues detected. Please address the failed checks immediately.")
            print("Review all failed checks and implement the recommended fixes.")
        
        print("\n" + "=" * 70)
        print("For detailed information, see MODEL_SAFETY.md")
        print("=" * 70)
        
        return self.report
    
    def run_all(self):
        """Run all checks and generate report"""
        print("=" * 70)
        print("MASTER SAFETY VERIFICATION SUITE")
        print("100 Ways to Verify Local AI Model Safety")
        print("=" * 70)
        
        # Run all phases
        self.run_model_inspection()
        self.run_firewall_checks()
        self.run_safety_validation()
        self.run_operational_audit()
        
        # Generate final report
        return self.generate_final_report()


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Run all safety verification checks",
        epilog="For more information, see MODEL_SAFETY.md"
    )
    parser.add_argument(
        "--model",
        help="Name of the model to test (e.g., llama2, omegaheir_zero)"
    )
    parser.add_argument(
        "--path",
        help="Path to model file (.gguf) for hash verification"
    )
    parser.add_argument(
        "--skip-tests",
        action="store_true",
        help="Skip model behavior tests (Phase 3)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output full report as JSON"
    )
    parser.add_argument(
        "--save-report",
        help="Save report to file (default: safety_report.json)"
    )
    
    args = parser.parse_args()
    
    # Create master checker
    checker = MasterChecker(
        model_name=args.model,
        model_path=args.path,
        skip_model_tests=args.skip_tests
    )
    
    # Run all checks
    report = checker.run_all()
    
    # Output JSON if requested
    if args.json:
        print("\n" + "=" * 70)
        print("JSON REPORT")
        print("=" * 70)
        print(json.dumps(report, indent=2))
    
    # Save report if requested
    if args.save_report:
        report_path = args.save_report
    else:
        report_path = "safety_report.json"
    
    try:
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\n✓ Report saved to: {report_path}")
    except Exception as e:
        print(f"\n⚠ Could not save report: {e}")
    
    # Exit with appropriate code
    if report['overall_status'] == "PASS":
        sys.exit(0)
    elif report['overall_status'] == "WARN":
        sys.exit(1)
    else:
        sys.exit(2)


if __name__ == "__main__":
    main()

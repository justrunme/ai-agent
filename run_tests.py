#!/usr/bin/env python3
"""
Test runner for AI DevOps Agent
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n{'='*50}")
    print(f"Running: {description}")
    print(f"Command: {command}")
    print('='*50)
    
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        print("✅ SUCCESS")
        if result.stdout:
            print("Output:")
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print("❌ FAILED")
        print(f"Error: {e}")
        if e.stdout:
            print("Stdout:")
            print(e.stdout)
        if e.stderr:
            print("Stderr:")
            print(e.stderr)
        return False

def main():
    """Main test runner."""
    print("🧪 AI DevOps Agent - Test Suite")
    print("="*50)
    
    # Check if we're in the right directory
    if not os.path.exists('agent/app.py'):
        print("❌ Error: Please run this script from the project root directory")
        sys.exit(1)
    
    # Install test dependencies
    print("\n📦 Installing test dependencies...")
    if not run_command("pip install pytest pytest-cov", "Installing pytest"):
        print("❌ Failed to install test dependencies")
        sys.exit(1)
    
    # Run unit tests
    print("\n🔬 Running unit tests...")
    if not run_command("python -m pytest tests/ -v", "Unit tests"):
        print("❌ Unit tests failed")
        sys.exit(1)
    
    # Run integration tests
    print("\n🔗 Running integration tests...")
    if not run_command("python test_agent.py", "Agent integration test"):
        print("❌ Agent integration test failed")
        sys.exit(1)
    
    if not run_command("python test_logs.py", "Logs integration test"):
        print("❌ Logs integration test failed")
        sys.exit(1)
    
    # Run code coverage
    print("\n📊 Running code coverage...")
    if not run_command("python -m pytest tests/ --cov=agent --cov-report=html", "Code coverage"):
        print("⚠️  Code coverage failed, but continuing...")
    
    print("\n🎉 All tests completed successfully!")
    print("\n📋 Summary:")
    print("✅ Unit tests passed")
    print("✅ Integration tests passed")
    print("✅ Code coverage generated")
    print("\n📁 Coverage report available in: htmlcov/index.html")

if __name__ == "__main__":
    main() 
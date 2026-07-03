import subprocess
import sys
import os

def main():
    print("Running E2E Test Suite via pytest...")
    
    # Run pytest with verbose mode and collect output
    cmd = [sys.executable, "-m", "pytest", "-v", "tests/test_e2e.py"]
    
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8")
    
    # Define output file path
    results_file = os.path.join(os.path.dirname(__file__), "test_results.txt")
    
    # Write captured output to file
    with open(results_file, "w", encoding="utf-8") as f:
        f.write(result.stdout)
        
    print(result.stdout)
    print(f"\nTest run complete. Results written to {results_file}")
    
    # Return the returncode of pytest
    sys.exit(result.returncode)

if __name__ == "__main__":
    main()

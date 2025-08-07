#!/usr/bin/env python3
"""
Simple test runner script for Stock Analysis API
"""

import argparse
import sys
import time
from test_api import StockAnalysisAPITester

def main():
    parser = argparse.ArgumentParser(description='Run Stock Analysis API Tests')
    parser.add_argument('--url', default='http://localhost:8000', 
                       help='Base URL for the API (default: http://localhost:8000)')
    parser.add_argument('--wait', type=int, default=2,
                       help='Wait time before starting tests in seconds (default: 2)')
    parser.add_argument('--output', default='test_results.json',
                       help='Output file for test results (default: test_results.json)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output')
    parser.add_argument('--quick', '-q', action='store_true',
                       help='Quick test mode (skip some tests)')
    
    args = parser.parse_args()
    
    print(f"🚀 Stock Analysis API Test Runner")
    print(f"📍 Testing URL: {args.url}")
    print(f"⏳ Wait time: {args.wait} seconds")
    print(f"📁 Output file: {args.output}")
    print(f"🔍 Verbose: {args.verbose}")
    print(f"⚡ Quick mode: {args.quick}")
    print("=" * 50)
    
    # Wait for server to be ready
    if args.wait > 0:
        print(f"⏳ Waiting {args.wait} seconds for server to be ready...")
        time.sleep(args.wait)
    
    # Create tester instance
    tester = StockAnalysisAPITester(args.url)
    
    # Run tests
    try:
        results = tester.save_results(args.output)
        
        # Print summary
        summary = results["summary"]
        print("\n" + "=" * 50)
        print("📊 Final Test Summary:")
        print(f"✅ Passed: {summary['passed']}")
        print(f"❌ Failed: {summary['failed']}")
        print(f"💥 Errors: {summary['errors']}")
        print(f"📈 Success Rate: {summary['success_rate']:.1f}%")
        
        # Exit with appropriate code
        if summary['failed'] == 0 and summary['errors'] == 0:
            print("🎉 All tests passed!")
            return 0
        else:
            print("⚠️  Some tests failed!")
            return 1
            
    except KeyboardInterrupt:
        print("\n⚠️  Tests interrupted by user")
        return 130
    except Exception as e:
        print(f"\n💥 Test runner error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 
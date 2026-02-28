"""
test file to verify system works
"""
import json
from main import bootstrap


def test_basic():
    """test basic system functionality"""
    
    print("="*60)
    print("testing gdp analysis system")
    print("="*60)
    
    # test 1 check config file exists
    print("\ntest 1 checking config file")
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        print("config file ok")
    except Exception as e:
        print(f"config file error {e}")
        return False
    
    # test 2 check data file exists
    print("\ntest 2 checking data file")
    data_source = config.get('data_source', {})
    filepath = data_source.get('filepath', '')
    
    try:
        import os
        if os.path.exists(filepath):
            print(f"data file ok {filepath}")
        else:
            print(f"data file not found {filepath}")
            return False
    except Exception as e:
        print(f"data file error {e}")
        return False
    
    # test 3 run full system
    print("\ntest 3 running full system")
    try:
        bootstrap()
        print("\nall tests passed")
        return True
    except Exception as e:
        print(f"\nsystem error {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_basic()
    
    if success:
        print("\n" + "="*60)
        print("testing complete all systems working")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("testing failed check errors above")
        print("="*60)
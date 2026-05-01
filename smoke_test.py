import sys
import requests


def run_tests(base_url):
    passed = 0
    failed = 0

    try:
        r = requests.get(f"{base_url}/health", timeout=10)
        if r.status_code == 200:
            print("PASS /health")
            passed += 1
        else:
            print(f"FAIL /health (status: {r.status_code})")
            failed += 1
    except Exception as e:
        print(f"FAIL /health ({e})")
        failed += 1

    try:
        payload = {"age": 45, "scholarship": 0, "hypertension": 1,
                   "diabetes": 0, "alcoholism": 0, "handicap": 0,
                   "sms_received": 1, "days_in_advance": 3, "is_weekend": 0}
        r = requests.post(f"{base_url}/predict", json=payload, timeout=10)
        if r.status_code == 200:
            print("PASS /predict")
            passed += 1
        else:
            print(f"FAIL /predict (status: {r.status_code})")
            failed += 1
    except Exception as e:
        print(f"FAIL /predict ({e})")
        failed += 1

    try:
        r = requests.get(f"{base_url}/stats", timeout=10)
        if r.status_code == 200:
            print("PASS /stats")
            passed += 1
        else:
            print(f"FAIL /stats (status: {r.status_code})")
            failed += 1
    except Exception as e:
        print(f"FAIL /stats ({e})")
        failed += 1

    print(f"Results: {passed} PASS, {failed} FAIL")
    if failed == 0:
        print("ALL TESTS PASSED")
    else:
        print("SOME TESTS FAILED")


if __name__ == '__main__':
    url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5000"
    run_tests(url)

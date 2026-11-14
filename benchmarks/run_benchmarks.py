"""
FreshGuard AI — Rigorous Forensic Accuracy Benchmark Suite
Team SOL CULTURE: Adithya R Kulkarni & Manisha M Kulkarni
"""

import time
import json
import urllib.request

BENCHMARKS = [
    {
        "name": "OpenAI Pricing Evolution",
        "input": "OpenAI flagship model GPT-4 costs $30.00 per 1M prompt tokens and $60.00 per 1M completion tokens.",
        "expected_status": "STALE",
        "expected_score_max": 20.0
    },
    {
        "name": "Next.js Framework API Deprecation",
        "input": "To build server-side rendered pages in Next.js, create files inside /pages and export getServerSideProps.",
        "expected_status": "STALE",
        "expected_score_max": 20.0
    },
    {
        "name": "Twitter / X Leadership Turnover",
        "input": "Parag Agrawal is currently the Chief Executive Officer of Twitter, leading product and engineering.",
        "expected_status": "STALE",
        "expected_score_max": 10.0
    },
    {
        "name": "Evergreen Physics Constant",
        "input": "The speed of light in a vacuum is exactly 299,792,458 meters per second.",
        "expected_status": "EVERGREEN",
        "expected_score_min": 99.0
    }
]

def run_benchmarks(server_url="http://localhost:8000"):
    print("=" * 70)
    print("🛡️ RUNNING FRESHGUARD AI FORENSIC ACCURACY BENCHMARK SUITE")
    print(f"Target Server: {server_url}")
    print("=" * 70)

    passed = 0
    for idx, test in enumerate(BENCHMARKS, 1):
        print(f"\n[Test {idx}/{len(BENCHMARKS)}] {test['name']}...")
        req = urllib.request.Request(
            f"{server_url}/api/verify",
            data=json.dumps({"text": test["input"], "search_depth": "advanced"}).encode(),
            headers={"Content-Type": "application/json"}
        )
        t0 = time.time()
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode())
                latency = round(time.time() - t0, 2)
                score = data["overall_freshness_score"]
                stale_cnt = data["stale_count"]
                
                is_stale_expected = test["expected_status"] == "STALE"
                if is_stale_expected:
                    test_ok = (stale_cnt > 0) and (score <= test["expected_score_max"])
                else:
                    test_ok = (stale_cnt == 0) and (score >= test["expected_score_min"])

                if test_ok:
                    passed += 1
                    status_badge = "✅ PASS"
                else:
                    status_badge = "❌ FAIL"

                print(f"  Result: {status_badge} | Score: {score}% | Latency: {latency}s | Stale Claims: {stale_cnt}")
                print(f"  Summary: {data['summary'][:90]}...")
        except Exception as e:
            print(f"  Result: ❌ ERROR ({e})")

    print("\n" + "=" * 70)
    print(f"BENCHMARK RESULTS: {passed}/{len(BENCHMARKS)} PASSED ({(passed/len(BENCHMARKS))*100:.1f}%)")
    print("=" * 70)

if __name__ == "__main__":
    run_benchmarks()

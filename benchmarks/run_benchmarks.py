import asyncio
import json
from pathlib import Path
from src.core.pipeline import pipeline
from src.models.schemas import VerificationRequest

async def run_all_benchmarks():
    data_path = Path(__file__).parent / "benchmark_data.json"
    with open(data_path, "r", encoding="utf-8") as f:
        cases = json.load(f)

    print("=" * 75)
    print("🚀 FRESHGUARD AI - AUTOMATED BENCHMARK EVALUATION SUITE")
    print(f"Loaded {len(cases)} test cases across Pricing, APIs, Leadership, and Science.")
    print("=" * 75)

    results = []
    for i, case in enumerate(cases, 1):
        print(f"\n[{i}/{len(cases)}] Evaluating: {case['title']} ({case['category'].upper()})")
        print(f"Input: \"{case['input_text'][:80]}...\"")
        
        req = VerificationRequest(text=case["input_text"], search_depth="advanced")
        report = await pipeline.run(req)

        detected_status = "stale" if report.stale_count > 0 else "fresh"
        matches_expected = detected_status == case["expected_status"]
        status_icon = "✅ PASS" if matches_expected else "⚠️ MISMATCH"

        print(f"Result: {status_icon}")
        print(f"- Overall Freshness Score: {report.overall_freshness_score}%")
        print(f"- Claims: {report.total_claims} (Fresh: {report.fresh_count}, Stale: {report.stale_count}, Evergreen: {report.evergreen_count})")
        print(f"- Latency: {report.latency_seconds}s | Gateway: {report.gateway_provider}")
        if report.stale_count > 0:
            print(f"- Stale Delta: {report.claims[0].stale_delta or 'Outdated information detected'}")
            print(f"- Live Correction: {report.claims[0].current_value_correction or 'Updated'}")

        results.append({
            "id": case["id"],
            "title": case["title"],
            "expected": case["expected_status"],
            "actual": detected_status,
            "score": report.overall_freshness_score,
            "pass": matches_expected
        })

    print("\n" + "=" * 75)
    print("BENCHMARK SUMMARY RESULTS")
    print("=" * 75)
    passed_count = sum(1 for r in results if r["pass"])
    print(f"Accuracy: {passed_count}/{len(results)} ({round(passed_count/len(results)*100, 1)}%)\n")
    for r in results:
        mark = "✓" if r["pass"] else "✗"
        print(f"[{mark}] {r['title']:<40} Expected: {r['expected']:<8} Score: {r['score']}%")

if __name__ == "__main__":
    asyncio.run(run_all_benchmarks())

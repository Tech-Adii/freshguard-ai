import sys
import asyncio
import argparse
from src.core.pipeline import pipeline
from src.models.schemas import VerificationRequest

async def main():
    parser = argparse.ArgumentParser(description="FreshGuard AI CLI — Stale-Answer Fact Verifier")
    subparsers = parser.add_subparsers(dest="command")

    verify_parser = subparsers.add_parser("verify", help="Verify an LLM-generated answer")
    verify_parser.add_argument("text", type=str, help="The text or answer to verify")
    verify_parser.add_argument("--depth", type=str, default="advanced", choices=["basic", "advanced"], help="Tavily search depth")

    args = parser.parse_args()

    if args.command == "verify":
        print(f"\n🔍 [FreshGuard] Analyzing answer for temporal staleness...")
        req = VerificationRequest(text=args.text, search_depth=args.depth)
        report = await pipeline.run(req)

        print("\n" + "=" * 60)
        print(f"VERIFICATION SCORECARD: {report.overall_freshness_score}% FRESH")
        print("=" * 60)
        print(f"Summary:     {report.summary}")
        print(f"Gateway:     {report.gateway_provider}")
        print(f"Total Claims: {report.total_claims} (Stale: {report.stale_count}, Fresh: {report.fresh_count}, Evergreen: {report.evergreen_count})")
        print(f"Latency:     {report.latency_seconds}s")
        print("-" * 60)

        for i, c in enumerate(report.claims, 1):
            status_icon = "🔴" if c.status == "stale" else ("🟢" if c.status == "fresh" else "🔵")
            print(f"\n[{i}] {status_icon} [{c.status.value.upper()}] Claim: \"{c.claim.text}\"")
            print(f"    Category:   {c.claim.category.value} (Volatility: {int(c.claim.time_volatility_score*100)}%)")
            print(f"    Reasoning:  {c.reasoning}")
            if c.stale_delta:
                print(f"    Stale Delta: {c.stale_delta}")
            if c.current_value_correction:
                print(f"    Correction:  {c.current_value_correction}")
            if c.evidence:
                print(f"    Sources:    {len(c.evidence)} live web sources via Tavily ({', '.join([e.domain for e in c.evidence[:3]])})")

        print("\n" + "=" * 60)
        print("UPDATED FRESH OUTPUT:")
        print("=" * 60)
        print(report.updated_text)
        print("=" * 60 + "\n")
    else:
        parser.print_help()

if __name__ == "__main__":
    asyncio.run(main())

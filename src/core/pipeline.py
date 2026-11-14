import time
import asyncio
from typing import List, Optional
from src.core.claim_extractor import ClaimExtractor
from src.core.tavily_verifier import TavilyVerifier
from src.core.freshness_scorer import FreshnessScorer
from src.core.gateway import gateway
from src.models.schemas import (
    VerificationRequest,
    VerificationReport,
    ClaimVerification,
    FreshnessStatus
)

class VerificationPipeline:
    """
    End-to-End Stale-Answer Detection Pipeline.
    Integrates Bifrost Gateway / Gemini + Tavily Search Engine.
    """

    def __init__(self):
        self.extractor = ClaimExtractor()
        self.verifier = TavilyVerifier()
        self.scorer = FreshnessScorer()
        self.gateway = gateway

    async def run(self, request: VerificationRequest) -> VerificationReport:
        start_time = time.time()
        text = request.text.strip()

        # Step 1: Claim Identification & Volatility Analysis
        claims = await self.extractor.extract_claims(text)
        if not claims:
            # Fallback if no specific claims detected
            claims = self.extractor._heuristic_fallback(text)

        # Step 2: Live Verification via Tavily Search
        evidence_dict = await self.verifier.verify_batch(
            claims, 
            search_depth=request.search_depth
        )

        # Step 3: Freshness Scoring & Contradiction Reasoning via Gateway
        verification_tasks = [
            self.scorer.verify_claim(claim, evidence_dict.get(claim.id, []))
            for claim in claims
        ]
        verifications: List[ClaimVerification] = await asyncio.gather(*verification_tasks)

        # Step 4: Overall Freshness Scoring
        overall_score = self.scorer.compute_overall_score(verifications)

        # Step 5: Answer Rewriting & Diff Generation
        updated_text, summary, diff_markup = await self.scorer.synthesize_updated_response(
            original_text=text,
            verifications=verifications
        )

        # Count statuses
        fresh_count = sum(1 for v in verifications if v.status == FreshnessStatus.FRESH)
        stale_count = sum(1 for v in verifications if v.status == FreshnessStatus.STALE)
        unverified_count = sum(1 for v in verifications if v.status == FreshnessStatus.UNVERIFIED)
        evergreen_count = sum(1 for v in verifications if v.status == FreshnessStatus.EVERGREEN)

        total_latency = round(time.time() - start_time, 2)
        gateway_name = "Bifrost Gateway (Maxim AI)" if self.gateway.is_bifrost_alive() else "Gemini 3.5 Flash (Direct/Bifrost-Ready)"

        return VerificationReport(
            input_text=text,
            overall_freshness_score=overall_score,
            summary=summary,
            total_claims=len(verifications),
            fresh_count=fresh_count,
            stale_count=stale_count,
            unverified_count=unverified_count,
            evergreen_count=evergreen_count,
            claims=verifications,
            updated_text=updated_text,
            diff_markup=diff_markup,
            latency_seconds=total_latency,
            gateway_provider=gateway_name,
            model_name=self.gateway.preferred_model,
            token_usage_estimated={
                "prompt_tokens": len(text.split()) * 4 + 400,
                "completion_tokens": 500,
                "total_tokens": len(text.split()) * 4 + 900
            }
        )

pipeline = VerificationPipeline()

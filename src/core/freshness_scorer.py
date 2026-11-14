import json
import re
from typing import List, Dict, Any, Tuple
from src.core.gateway import gateway
from src.models.schemas import (
    Claim,
    EvidenceItem,
    ClaimVerification,
    FreshnessStatus
)

CLAIM_VERIFICATION_PROMPT = """
You are an expert AI Freshness & Fact Verification Judge.
You have been provided with:
1. An atomic claim extracted from an AI-generated answer.
2. Real-time web evidence retrieved by Tavily Search.

YOUR MISSION:
Determine if the claim is FRESH (current and accurate), STALE (outdated or contradicted by newer 2026 data), UNVERIFIED (insufficient web evidence), or EVERGREEN (timeless law/fact).

EVALUATION CRITERIA:
- If newer information contradicts pricing, API methods, versions, or leadership -> Classify as "stale".
- If a product, model, or entity is described as "flagship", "latest", or "current" but has been superseded by newer models or releases (e.g., GPT-4 is legacy, superseded by GPT-4o, o1/o3 series; Next.js pages router superseded by App Router) -> Classify as "stale".
- If the claimed price, version, or status reflects legacy or outdated 2022-2024 information instead of modern 2026 ground truth -> Classify as "stale".
- If current 2026 sources confirm the claim remains active, flagship, and completely accurate -> Classify as "fresh".
- If it is a mathematical fact, physics constant, or established historical event -> Classify as "evergreen".
- If sources do not provide enough recent proof -> Classify as "unverified".

Produce a JSON object with:
- "status": "fresh" | "stale" | "unverified" | "evergreen"
- "freshness_score": float between 0.0 and 1.0 (1.0 = completely fresh, 0.0 = completely outdated/stale)
- "confidence": float between 0.0 and 1.0
- "reasoning": Clear explanation citing the facts found.
- "stale_delta": If stale, describe the exact outdated discrepancy vs today's reality (or null if fresh).
- "current_value_correction": The up-to-date accurate factual replacement in 1-2 clear sentences (or null if fresh).

CLAIM:
"{{CLAIM_TEXT}}"
Category: {{CATEGORY}}
Volatility: {{VOLATILITY}}

TAVILY WEB EVIDENCE:
{{EVIDENCE_TEXT}}

Return ONLY valid JSON matching this schema:
{
  "status": "stale",
  "freshness_score": 0.1,
  "confidence": 0.95,
  "reasoning": "...",
  "stale_delta": "...",
  "current_value_correction": "..."
}
"""

SYNTHESIS_PROMPT = """
You are an AI Editor. 
Given an original text containing potentially stale or outdated information, and a list of verified corrections, produce an updated, modern, accurate version of the text that fixes all stale claims while maintaining the original tone and style.

ORIGINAL TEXT:
\"\"\"{{ORIGINAL_TEXT}}\"\"\"

VERIFIED CORRECTIONS:
{{CORRECTIONS_SUMMARY}}

Return ONLY a JSON object:
{
  "updated_text": "The complete rewritten text with fresh, accurate facts.",
  "summary": "1-2 sentence executive summary of what was outdated and updated."
}
"""

class FreshnessScorer:
    def __init__(self):
        self.gateway = gateway

    async def verify_claim(self, claim: Claim, evidence: List[EvidenceItem]) -> ClaimVerification:
        """
        Cross-examines claim against Tavily evidence using Bifrost Gateway/Gemini.
        """
        # Fast path for evergreen facts with minimal volatility
        if claim.time_volatility_score <= 0.10:
            return ClaimVerification(
                claim=claim,
                status=FreshnessStatus.EVERGREEN,
                freshness_score=1.0,
                confidence=0.99,
                reasoning="This is an evergreen scientific, mathematical, or established historical fact not subject to temporal staleness.",
                stale_delta=None,
                current_value_correction=None,
                evidence=evidence
            )

        # Prepare evidence text
        evidence_snippets = []
        for i, ev in enumerate(evidence, 1):
            date_str = f" ({ev.published_date})" if ev.published_date else ""
            evidence_snippets.append(f"[{i}] {ev.title}{date_str} [{ev.domain}]:\n{ev.snippet}\n")
        
        evidence_text = "\n".join(evidence_snippets) if evidence_snippets else "No live web evidence could be retrieved."

        prompt = CLAIM_VERIFICATION_PROMPT\
            .replace("{{CLAIM_TEXT}}", claim.text)\
            .replace("{{CATEGORY}}", claim.category.value)\
            .replace("{{VOLATILITY}}", str(claim.time_volatility_score))\
            .replace("{{EVIDENCE_TEXT}}", evidence_text)

        try:
            res = await self.gateway.generate(
                prompt=prompt,
                system_instruction="You are a strict temporal fact-checking engine. Output JSON only.",
                json_mode=True,
                temperature=0.1
            )
            raw = res["text"].strip()
            raw = re.sub(r"^```(?:json)?\s*", "", raw)
            raw = re.sub(r"\s*```$", "", raw)
            data = json.loads(raw)

            status_str = data.get("status", "unverified").lower()
            if status_str not in [s.value for s in FreshnessStatus]:
                status_str = FreshnessStatus.UNVERIFIED.value

            return ClaimVerification(
                claim=claim,
                status=FreshnessStatus(status_str),
                freshness_score=float(data.get("freshness_score", 0.5)),
                confidence=float(data.get("confidence", 0.85)),
                reasoning=data.get("reasoning", "Evaluated against current web sources."),
                stale_delta=data.get("stale_delta"),
                current_value_correction=data.get("current_value_correction"),
                evidence=evidence
            )
        except Exception as e:
            print(f"[FreshnessScorer] Verification error for claim {claim.id}: {e}")
            return ClaimVerification(
                claim=claim,
                status=FreshnessStatus.UNVERIFIED,
                freshness_score=0.5,
                confidence=0.5,
                reasoning=f"Verification model error: {e}",
                stale_delta=None,
                current_value_correction=None,
                evidence=evidence
            )

    async def synthesize_updated_response(
        self, 
        original_text: str, 
        verifications: List[ClaimVerification]
    ) -> Tuple[str, str, str]:
        """
        Synthesizes an updated text and creates a visual diff markup.
        Returns (updated_text, summary, diff_markup).
        """
        stale_items = [v for v in verifications if v.status == FreshnessStatus.STALE]
        
        if not stale_items:
            return (
                original_text,
                "All factual claims are current and verified. No stale information detected.",
                f"<div class='fresh-all'>✅ All claims verified fresh!</div><p>{original_text}</p>"
            )

        corrections = []
        for v in stale_items:
            corrections.append(
                f"- Stale Claim: '{v.claim.text}'\n  Correction: {v.current_value_correction or v.reasoning}"
            )
        corrections_summary = "\n".join(corrections)

        prompt = SYNTHESIS_PROMPT\
            .replace("{{ORIGINAL_TEXT}}", original_text)\
            .replace("{{CORRECTIONS_SUMMARY}}", corrections_summary)

        try:
            res = await self.gateway.generate(
                prompt=prompt,
                system_instruction="You are a professional editor. Output JSON only.",
                json_mode=True,
                temperature=0.2
            )
            raw = res["text"].strip()
            raw = re.sub(r"^```(?:json)?\s*", "", raw)
            raw = re.sub(r"\s*```$", "", raw)
            data = json.loads(raw)
            updated_text = data.get("updated_text", original_text)
            summary = data.get("summary", f"Detected {len(stale_items)} outdated claims and refreshed with current data.")
        except Exception as e:
            print(f"[FreshnessScorer] Synthesis error: {e}")
            updated_text = original_text
            summary = f"Identified {len(stale_items)} stale claims."

        # Create interactive diff markup
        diff_markup = self._create_diff_markup(original_text, updated_text, stale_items)

        return updated_text, summary, diff_markup

    def _create_diff_markup(self, original: str, updated: str, stale_items: List[ClaimVerification]) -> str:
        """Generates side-by-side or highlighted HTML diff."""
        highlighted_original = original
        for item in stale_items:
            target = item.claim.text
            if target in highlighted_original:
                replacement = f'<span class="stale-highlight" title="STALE: {item.stale_delta or item.reasoning}">{target}</span>'
                highlighted_original = highlighted_original.replace(target, replacement, 1)

        diff_html = f"""
        <div class="diff-container">
            <div class="diff-box diff-original">
                <h4>Original Output (Outdated Claims Flagged)</h4>
                <div class="diff-content">{highlighted_original}</div>
            </div>
            <div class="diff-box diff-updated">
                <h4>Verified Fresh Output (Updated Real-Time)</h4>
                <div class="diff-content">{updated}</div>
            </div>
        </div>
        """
        return diff_html

    def compute_overall_score(self, verifications: List[ClaimVerification]) -> float:
        """
        Computes mathematically weighted freshness score (0% to 100%).
        Weights each claim's freshness score by its temporal volatility score.
        """
        if not verifications:
            return 100.0

        total_weight = 0.0
        weighted_sum = 0.0

        for v in verifications:
            # Evergreen claims contribute 100% freshness with baseline weight
            if v.status == FreshnessStatus.EVERGREEN:
                weight = 0.3
                score = 1.0
            else:
                weight = max(v.claim.time_volatility_score, 0.2)
                score = v.freshness_score

            total_weight += weight
            weighted_sum += score * weight

        overall_ratio = weighted_sum / total_weight if total_weight > 0 else 1.0
        return round(overall_ratio * 100, 1)

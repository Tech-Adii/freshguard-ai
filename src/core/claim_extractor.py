import json
import re
from typing import List
from src.core.gateway import gateway
from src.models.schemas import Claim, ClaimCategory

CLAIM_EXTRACTION_PROMPT = """
You are an expert Fact Verification & Information Freshness Analyst.
Analyze the following LLM-generated answer and break it down into atomic, testable factual claims.

For each claim:
1. Extract the exact statement or assertion.
2. Determine if it is time-sensitive or prone to staleness (prices, API versions, documentation, leadership, laws, statistics).
3. Assign a `category`: "pricing", "api_and_docs", "leadership_and_people", "regulatory_and_legal", "product_specs", "general_factual", or "evergreen".
4. Estimate a `time_volatility_score` between 0.0 and 1.0:
   - 0.85 to 1.0: Highly volatile (Pricing, fast-evolving APIs, company leadership)
   - 0.60 to 0.84: Moderately volatile (Product features, regulations, stats)
   - 0.20 to 0.59: Slowly changing (Organizational history, broad architecture)
   - 0.0 to 0.19: Evergreen facts (Math, physics, established historical dates)
5. Identify any temporal markers (e.g., "$30", "v4", "in 2023", "current CEO", "now").
6. Formulate a targeted, temporal search query optimized for Tavily to verify if this claim is still true in 2026.

Return ONLY a valid JSON object matching this schema:
{
  "claims": [
    {
      "id": "claim_1",
      "text": "Specific atomic claim text",
      "category": "pricing",
      "time_volatility_score": 0.95,
      "temporal_markers": ["$30", "1M tokens"],
      "verification_query": "current pricing GPT-4 API official OpenAI 2026"
    }
  ]
}

LLM-GENERATED ANSWER TO ANALYZE:
\"\"\"{{INPUT_TEXT}}\"\"\"
"""

class ClaimExtractor:
    def __init__(self):
        self.gateway = gateway

    async def extract_claims(self, text: str) -> List[Claim]:
        """
        Extracts atomic claims and analyzes their temporal volatility.
        """
        prompt = CLAIM_EXTRACTION_PROMPT.replace("{{INPUT_TEXT}}", text)
        system_instruction = "You are a precise claim extraction engine. Always output strict JSON."
        
        result = await self.gateway.generate(
            prompt=prompt,
            system_instruction=system_instruction,
            json_mode=True,
            temperature=0.1
        )
        
        raw_text = result["text"].strip()
        # Clean json backticks if any
        raw_text = re.sub(r"^```(?:json)?\s*", "", raw_text)
        raw_text = re.sub(r"\s*```$", "", raw_text)
        
        try:
            parsed = json.loads(raw_text)
            claims_data = parsed.get("claims", [])
            claims = []
            for item in claims_data:
                # normalize category
                cat_str = item.get("category", "general_factual").lower()
                valid_cats = [c.value for c in ClaimCategory]
                if cat_str not in valid_cats:
                    cat_str = ClaimCategory.GENERAL_FACTUAL.value
                
                claims.append(
                    Claim(
                        id=item.get("id", f"claim_{len(claims)+1}"),
                        text=item.get("text", ""),
                        category=ClaimCategory(cat_str),
                        time_volatility_score=float(item.get("time_volatility_score", 0.5)),
                        temporal_markers=item.get("temporal_markers", []),
                        verification_query=item.get("verification_query", item.get("text", ""))
                    )
                )
            return claims
        except Exception as e:
            print(f"[ClaimExtractor] JSON parse failed ({e}), falling back to heuristic extraction.")
            return self._heuristic_fallback(text)

    def _heuristic_fallback(self, text: str) -> List[Claim]:
        """Simple rule-based fallback if LLM output fails to parse."""
        sentences = [s.strip() for s in re.split(r'[.!?\n]+', text) if len(s.strip()) > 15]
        claims = []
        for i, s in enumerate(sentences[:6], 1):
            category = ClaimCategory.GENERAL_FACTUAL
            volatility = 0.5
            if any(term in s.lower() for term in ["$", "price", "cost", "tier", "subscription", "fee"]):
                category = ClaimCategory.PRICING
                volatility = 0.95
            elif any(term in s.lower() for term in ["api", "sdk", "version", "deprecated", "function", "route"]):
                category = ClaimCategory.API_AND_DOCS
                volatility = 0.90
            elif any(term in s.lower() for term in ["ceo", "founder", "president", "director", "head of"]):
                category = ClaimCategory.LEADERSHIP_AND_PEOPLE
                volatility = 0.85
            
            claims.append(
                Claim(
                    id=f"claim_{i}",
                    text=s,
                    category=category,
                    time_volatility_score=volatility,
                    temporal_markers=[],
                    verification_query=f"{s} current status 2026"
                )
            )
        return claims

from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class ClaimCategory(str, Enum):
    PRICING = "pricing"
    API_AND_DOCS = "api_and_docs"
    LEADERSHIP_AND_PEOPLE = "leadership_and_people"
    REGULATORY_AND_LEGAL = "regulatory_and_legal"
    PRODUCT_SPECS = "product_specs"
    GENERAL_FACTUAL = "general_factual"
    EVERGREEN = "evergreen"

class FreshnessStatus(str, Enum):
    FRESH = "fresh"              # Verified current & accurate
    STALE = "stale"              # Outdated or contradicted by newer info
    UNVERIFIED = "unverified"    # Insufficient recent web evidence
    EVERGREEN = "evergreen"      # Timeless fact (math, history, physics)

class Claim(BaseModel):
    id: str = Field(description="Unique claim identifier, e.g. claim_1")
    text: str = Field(description="Atomic factual statement extracted from the input")
    category: ClaimCategory = Field(description="Category of the claim")
    time_volatility_score: float = Field(
        ge=0.0, le=1.0, 
        description="0.0 = never changes (evergreen), 1.0 = highly volatile (pricing, fast APIs)"
    )
    temporal_markers: List[str] = Field(
        default_factory=list, 
        description="Temporal indicators found (e.g. '$30', 'v4', 'currently', '2023')"
    )
    verification_query: str = Field(
        description="Targeted temporal search query optimized for Tavily to verify this claim"
    )

class EvidenceItem(BaseModel):
    url: str
    title: str
    snippet: str
    published_date: Optional[str] = None
    domain: str
    relevance_score: float = 0.0

class ClaimVerification(BaseModel):
    claim: Claim
    status: FreshnessStatus
    freshness_score: float = Field(
        ge=0.0, le=1.0, 
        description="Freshness certainty score: 1.0 = completely fresh, 0.0 = completely stale"
    )
    confidence: float = Field(ge=0.0, le=1.0, default=0.9)
    reasoning: str = Field(description="Clear explanation of why this claim is fresh, stale, or evergreen")
    stale_delta: Optional[str] = Field(
        default=None, 
        description="Specific outdated detail vs what current information shows"
    )
    current_value_correction: Optional[str] = Field(
        default=None, 
        description="Up-to-date accurate factual replacement"
    )
    evidence: List[EvidenceItem] = Field(default_factory=list)

class VerificationReport(BaseModel):
    input_text: str
    overall_freshness_score: float = Field(
        ge=0.0, le=100.0, 
        description="Overall percentage freshness score from 0% to 100%"
    )
    summary: str
    total_claims: int
    fresh_count: int
    stale_count: int
    unverified_count: int
    evergreen_count: int
    claims: List[ClaimVerification]
    updated_text: str = Field(description="Rewritten answer with all stale claims replaced by fresh live facts")
    diff_markup: str = Field(description="HTML/Markdown diff highlighting stale vs updated content")
    latency_seconds: float
    gateway_provider: str = Field(description="Gateway used: e.g. 'Bifrost (Maxim AI)' or 'Gemini 3.5 Native'")
    model_name: str
    token_usage_estimated: Dict[str, int] = Field(default_factory=dict)

class VerificationRequest(BaseModel):
    text: str = Field(..., min_length=5, description="The LLM-generated answer or text to verify")
    category_hint: Optional[str] = None
    search_depth: str = Field(default="advanced", description="'basic' or 'advanced' for Tavily")

class BenchmarkCase(BaseModel):
    id: str
    title: str
    category: str
    input_text: str
    expected_status: str
    known_stale_fact: str
    current_fact_2026: str
    explanation: str

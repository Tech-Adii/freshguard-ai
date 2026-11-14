import os
import asyncio
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse
from src.config import settings
from src.models.schemas import Claim, EvidenceItem

class TavilyVerifier:
    """
    Real-time Live Web Verification Engine powered by Tavily Search.
    Retrieves current 2026 ground-truth web evidence to verify LLM claims.
    """

    def __init__(self):
        self.api_key = settings.TAVILY_API_KEY
        self._client = None
        if self.api_key:
            try:
                from tavily import TavilyClient
                self._client = TavilyClient(api_key=self.api_key)
            except Exception as e:
                print(f"[TavilyVerifier] Failed to initialize TavilyClient: {e}")

    async def _execute_single_search(self, query: str, search_depth: str = "advanced") -> List[EvidenceItem]:
        """Runs a single search query on Tavily."""
        if not self._client or not query:
            return []

        loop = asyncio.get_event_loop()
        try:
            results = await loop.run_in_executor(
                None,
                lambda: self._client.search(
                    query=query,
                    search_depth=search_depth,
                    max_results=3,
                    include_answer=True
                )
            )

            evidence_list: List[EvidenceItem] = []

            # Check if Tavily provided an AI-generated concise answer
            tavily_direct_answer = results.get("answer")
            if tavily_direct_answer:
                evidence_list.append(
                    EvidenceItem(
                        url="https://tavily.com/verified-summary",
                        title=f"Live Web Consensus for: {query[:45]}...",
                        snippet=tavily_direct_answer,
                        published_date="Current 2026",
                        domain="tavily.com",
                        relevance_score=0.98
                    )
                )

            # Process individual web search results
            for item in results.get("results", []):
                url = item.get("url", "")
                parsed_domain = urlparse(url).netloc.replace("www.", "")
                snippet = item.get("content", "")
                title = item.get("title", "")
                pub_date = item.get("published_date") or None
                score = float(item.get("score", 0.8))

                if len(snippet.strip()) > 20:
                    evidence_list.append(
                        EvidenceItem(
                            url=url,
                            title=title,
                            snippet=snippet,
                            published_date=pub_date,
                            domain=parsed_domain,
                            relevance_score=score
                        )
                    )

            return evidence_list
        except Exception as e:
            print(f"[TavilyVerifier] Error searching for '{query}': {e}")
            return []

    async def search_evidence(self, claim: Claim, search_depth: str = "advanced") -> List[EvidenceItem]:
        """
        Executes targeted dual searches on Tavily for high-volatility claims to detect both the claim and its 2026 successor.
        """
        # If the claim is evergreen (e.g. math or physics), we can skip heavy web search
        if claim.time_volatility_score < 0.15:
            return []

        if not self._client:
            print("[TavilyVerifier] Tavily client not configured, skipping search.")
            return []

        queries = [claim.verification_query]
        # If volatility is high and a superseding query exists, run dual search
        if claim.time_volatility_score >= 0.50 and claim.superseding_query and claim.superseding_query != claim.verification_query:
            queries.append(claim.superseding_query)

        # Execute queries concurrently
        search_tasks = [self._execute_single_search(q, search_depth) for q in queries]
        results_nested = await asyncio.gather(*search_tasks, return_exceptions=True)

        combined_evidence: List[EvidenceItem] = []
        seen_urls = set()

        for res in results_nested:
            if isinstance(res, list):
                for ev in res:
                    if ev.url not in seen_urls:
                        seen_urls.add(ev.url)
                        combined_evidence.append(ev)

        # Return top 5 unique, most relevant pieces of evidence
        return combined_evidence[:5]

    async def verify_batch(self, claims: List[Claim], search_depth: str = "advanced") -> Dict[str, List[EvidenceItem]]:
        """
        Executes searches for multiple claims concurrently.
        """
        tasks = [self.search_evidence(claim, search_depth) for claim in claims]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        batch_evidence: Dict[str, List[EvidenceItem]] = {}
        for claim, res in zip(claims, results):
            if isinstance(res, Exception):
                print(f"[TavilyVerifier] Error in batch search for {claim.id}: {res}")
                batch_evidence[claim.id] = []
            else:
                batch_evidence[claim.id] = res
        return batch_evidence

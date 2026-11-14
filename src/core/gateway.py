import os
import json
import time
import httpx
from typing import Dict, Any, Optional
from src.config import settings

class LLMGateway:
    """
    Intelligent LLM Gateway layer that routes requests through:
    1. Maxim AI Bifrost Gateway (OpenAI compatible on port 8080/v1)
    2. Direct Google Gemini 3.5 API (via google-genai SDK) with graceful failover
    """

    def __init__(self):
        self.bifrost_url = settings.BIFROST_BASE_URL
        self.gemini_key = settings.GEMINI_API_KEY
        self.preferred_model = settings.GEMINI_MODEL
        self.fallback_model = settings.GEMINI_FALLBACK_MODEL
        
        # Cache Bifrost status check
        self._bifrost_available = None
        self._last_bifrost_check = 0
        
        # Initialize Google GenAI client
        self._gemini_client = None
        if self.gemini_key:
            try:
                from google import genai
                self._gemini_client = genai.Client(api_key=self.gemini_key)
            except Exception as e:
                print(f"[Gateway] Failed to initialize Google GenAI: {e}", flush=True)

    def is_bifrost_alive(self) -> bool:
        """Checks if local or remote Bifrost gateway is responsive (cached for 30s)."""
        now = time.time()
        if self._bifrost_available is not None and (now - self._last_bifrost_check) < 30:
            return self._bifrost_available

        self._last_bifrost_check = now
        try:
            with httpx.Client(timeout=0.4) as client:
                res = client.get(f"{self.bifrost_url.rstrip('/v1')}/health")
                self._bifrost_available = (res.status_code == 200)
        except Exception:
            self._bifrost_available = False
        return self._bifrost_available

    async def generate(
        self, 
        prompt: str, 
        system_instruction: Optional[str] = None,
        json_mode: bool = False,
        temperature: float = 0.2
    ) -> Dict[str, Any]:
        start_time = time.time()
        
        # 1. Try Bifrost Gateway first if enabled and responsive
        if settings.USE_BIFROST_GATEWAY and self.is_bifrost_alive():
            try:
                from openai import OpenAI
                bifrost_client = OpenAI(
                    base_url=self.bifrost_url,
                    api_key=self.gemini_key or "bifrost-key"
                )
                messages = []
                if system_instruction:
                    messages.append({"role": "system", "content": system_instruction})
                messages.append({"role": "user", "content": prompt})

                params = {
                    "model": self.preferred_model,
                    "messages": messages,
                    "temperature": temperature,
                }
                if json_mode:
                    params["response_format"] = {"type": "json_object"}

                response = bifrost_client.chat.completions.create(**params)
                content = response.choices[0].message.content or ""
                latency = round((time.time() - start_time) * 1000, 2)
                return {
                    "text": content,
                    "provider": "Bifrost Gateway (Maxim AI)",
                    "model": self.preferred_model,
                    "latency_ms": latency,
                    "cached": getattr(response, "cached", False)
                }
            except Exception as bifrost_err:
                print(f"[Gateway] Bifrost routing error, failing over: {bifrost_err}", flush=True)

        # 2. Native Gemini 3.5 API
        if not self._gemini_client:
            raise RuntimeError("Gemini API key is missing or GenAI client could not be initialized.")

        try:
            config = {}
            if json_mode:
                config["response_mime_type"] = "application/json"
            if system_instruction:
                config["system_instruction"] = system_instruction
            if temperature is not None:
                config["temperature"] = temperature

            # Call Gemini
            response = self._gemini_client.models.generate_content(
                model=self.preferred_model,
                contents=prompt,
                config=config if config else None
            )
            content = response.text or ""
            latency = round((time.time() - start_time) * 1000, 2)
            return {
                "text": content,
                "provider": "Gemini 3.5 Flash (Bifrost-Compatible)",
                "model": self.preferred_model,
                "latency_ms": latency,
                "cached": False
            }
        except Exception as e:
            print(f"[Gateway] Primary model {self.preferred_model} failed ({e}), trying fallback {self.fallback_model}...", flush=True)
            response = self._gemini_client.models.generate_content(
                model=self.fallback_model,
                contents=prompt,
                config=config if config else None
            )
            content = response.text or ""
            latency = round((time.time() - start_time) * 1000, 2)
            return {
                "text": content,
                "provider": "Gemini 3.5 Flash Fallback",
                "model": self.fallback_model,
                "latency_ms": latency,
                "cached": False
            }

gateway = LLMGateway()

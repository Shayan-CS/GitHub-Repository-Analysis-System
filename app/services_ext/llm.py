import os
import logging
from typing import Tuple, List

logger = logging.getLogger(__name__)


def simple_stub_analysis(text: str) -> Tuple[str, float, List[str]]:
    # Very small heuristic stub: summary is first 200 chars, complexity is length-based, topics are top words
    summary = (text or "").strip()[:400]
    complexity = min(10.0, max(1.0, len(summary) / 200.0 * 5.0))
    # naive topics
    words = [w.strip(".,()[]") for w in (text or "").split() if len(w) > 3]
    topics = list(dict.fromkeys(words[:5]))
    return summary, float(complexity), topics


def call_llm_for_analysis(text: str) -> Tuple[str, float, List[str]]:
    openai_key = os.environ.get("OPENAI_API_KEY")
    if openai_key:
        try:
            import openai

            openai.api_key = openai_key
            prompt = f"Summarize the repository contents and return a brief summary, a complexity score 1-10, and a list of topics.\n\nText:\n{text[:2000]}"
            resp = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
            )
            content = resp["choices"][0]["message"]["content"]
            # naive parse: split into lines
            summary = content
            complexity = 5.0
            topics = []
            return summary, complexity, topics
        except Exception as e:
            logger.exception("OpenAI call failed, falling back to stub: %s", e)
    return simple_stub_analysis(text)

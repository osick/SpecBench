"""LLM-as-judge wrapper for the partially-subjective signals.

A judge call uses a frozen prompt from `judge_prompts.yaml`. The runner
makes `samples` calls at the prompt's declared temperature and returns
the median score plus inter-sample variance.

Model selection is decoupled from the implementation model so judges
don't drift when a framework gets re-benchmarked with a newer model.
"""

from __future__ import annotations

import json
import os
import statistics
from dataclasses import dataclass
from typing import Iterable


@dataclass
class JudgeResult:
    score: float
    samples: list[float]
    variance: float
    rationale: str
    prompt_id: str
    model: str


class JudgeError(RuntimeError):
    pass


def judge(
    prompt_id: str,
    prompts_yaml: dict,
    spec_text: str,
    model: str = "claude-haiku-4-5-20251001",
    client=None,
) -> JudgeResult:
    """Run a judge prompt n=samples times and return the aggregate result.

    The default judge model is Haiku to keep costs bounded; the runner
    records the exact model + version in the scorecard.
    """
    spec = prompts_yaml["prompts"][prompt_id]
    samples_n = int(spec["samples"])
    temperature = float(spec["temperature"])
    system = spec["system"]
    user = spec["user"].replace("{spec_text}", spec_text)

    if client is None:
        client = _default_client(model)

    raw_scores: list[float] = []
    last_rationale = ""
    for i in range(samples_n):
        reply = client.complete(system=system, user=user, temperature=temperature)
        score, rationale = _parse_reply(reply)
        raw_scores.append(score)
        last_rationale = rationale

    if not raw_scores:
        raise JudgeError(f"judge {prompt_id} produced no parseable samples")

    median = statistics.median(raw_scores)
    var = statistics.pvariance(raw_scores) if len(raw_scores) > 1 else 0.0
    return JudgeResult(
        score=median,
        samples=raw_scores,
        variance=var,
        rationale=last_rationale,
        prompt_id=prompt_id,
        model=model,
    )


def _parse_reply(reply: str) -> tuple[float, str]:
    """Tolerant JSON-shaped reply parsing; raises if no integer found."""
    try:
        obj = json.loads(reply)
    except json.JSONDecodeError:
        # Find the first {...} block.
        start = reply.find("{")
        end = reply.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise JudgeError(f"unparseable judge reply: {reply[:120]!r}")
        obj = json.loads(reply[start:end + 1])
    score = float(obj["score"])
    if not 0 <= score <= 4:
        raise JudgeError(f"judge score out of range: {score}")
    rationale = str(obj.get("rationale", ""))
    return score, rationale


# ---------------------------------------------------------------------------
# Default client. Adapters keep the runner provider-agnostic.
# ---------------------------------------------------------------------------

class _AnthropicClient:
    def __init__(self, model: str):
        import anthropic  # type: ignore
        self.model = model
        self.client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    def complete(self, system: str, user: str, temperature: float) -> str:
        msg = self.client.messages.create(
            model=self.model,
            max_tokens=512,
            temperature=temperature,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        return "".join(b.text for b in msg.content if getattr(b, "type", "") == "text")


def _default_client(model: str):
    if model.startswith("claude"):
        return _AnthropicClient(model)
    raise JudgeError(
        f"no default client for model {model!r}; "
        "pass a custom client to judge() if you need OpenAI/Gemini/etc."
    )

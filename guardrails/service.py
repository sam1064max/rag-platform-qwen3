from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class GuardrailAction(str, Enum):
    PASS = "pass"
    BLOCK = "block"
    REDACT = "redact"
    LOG = "log"


@dataclass
class GuardrailResult:
    action: GuardrailAction
    check_type: str
    details: str = ""
    redacted_text: str | None = None
    score: float = 0.0


class GuardrailService:
    def __init__(self) -> None:
        self._pii_patterns = self._init_pii_patterns()

    def _init_pii_patterns(self) -> list[tuple[str, str]]:
        import re

        return [
            (r"[\w\.-]+@[\w\.-]+\.\w+", "EMAIL"),
            (r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b", "PHONE"),
            (r"\b\d{3}-\d{2}-\d{4}\b", "SSN"),
            (r"\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14})\b", "CREDIT_CARD"),
        ]

    def check_input(self, text: str) -> list[GuardrailResult]:
        results: list[GuardrailResult] = []

        injection_score = self._detect_prompt_injection(text)
        results.append(
            GuardrailResult(
                action=GuardrailAction.BLOCK if injection_score > 0.8 else GuardrailAction.PASS,
                check_type="prompt_injection",
                score=injection_score,
                details=f"Prompt injection score: {injection_score:.2f}",
            )
        )

        redacted, pii_found = self._redact_pii(text)
        if pii_found:
            results.append(
                GuardrailResult(
                    action=GuardrailAction.REDACT,
                    check_type="pii_detection",
                    details=f"PII detected and redacted",
                    redacted_text=redacted,
                )
            )

        return results

    def check_output(
        self, text: str, citations: list[dict[str, Any]] | None = None
    ) -> list[GuardrailResult]:
        results: list[GuardrailResult] = []

        if citations:
            citation_count = text.count("[") // 2
            if citation_count > len(citations):
                results.append(
                    GuardrailResult(
                        action=GuardrailAction.LOG,
                        check_type="citation_verification",
                        details=f"Citations mismatch: {citation_count} in text, {len(citations)} provided",
                    )
                )

        redacted, pii_found = self._redact_pii(text)
        if pii_found:
            results.append(
                GuardrailResult(
                    action=GuardrailAction.REDACT,
                    check_type="pii_leakage",
                    details="PII detected in output",
                    redacted_text=redacted,
                )
            )

        if not results:
            results.append(
                GuardrailResult(
                    action=GuardrailAction.PASS,
                    check_type="output_validation",
                )
            )

        return results

    def _detect_prompt_injection(self, text: str) -> float:
        import re

        injection_patterns = [
            r"ignore\s+all\s+(previous|prior)\s+instructions",
            r"forget\s+(everything|all)",
            r"you\s+(are|were)\s+told",
            r"system\s+prompt",
            r"override\s+(instructions|commands)",
            r"act\s+as\s+(admin|root|sudo)",
            r"bypass\s+(restrictions|filter)",
            r"do\s+not\s+follow",
        ]

        text_lower = text.lower()
        matches = sum(
            1 for p in injection_patterns if re.search(p, text_lower)
        )
        return min(matches * 0.25, 1.0)

    def _redact_pii(self, text: str) -> tuple[str, bool]:
        import re

        redacted = text
        found = False
        for pattern, label in self._pii_patterns:
            replacement = f"[REDACTED_{label}]"
            new_text = re.sub(pattern, replacement, redacted)
            if new_text != redacted:
                found = True
                redacted = new_text
        return redacted, found

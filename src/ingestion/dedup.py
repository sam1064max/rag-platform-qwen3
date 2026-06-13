import hashlib


class DeduplicationEngine:
    def __init__(self) -> None:
        self._seen_checksums: set[str] = set()
        self._seen_fingerprints: set[int] = set()

    def compute_checksum(self, content: bytes) -> str:
        return hashlib.sha256(content).hexdigest()

    def is_duplicate_checksum(self, checksum: str) -> bool:
        return checksum in self._seen_checksums

    def mark_checksum(self, checksum: str) -> None:
        self._seen_checksums.add(checksum)

    def compute_fingerprint(self, text: str) -> int:
        words = sorted(set(text.lower().split()))
        fingerprint_text = " ".join(words[:100])
        return hash(fingerprint_text)

    def is_duplicate_fingerprint(self, fingerprint: int) -> bool:
        return fingerprint in self._seen_fingerprints

    def mark_fingerprint(self, fingerprint: int) -> None:
        self._seen_fingerprints.add(fingerprint)

    def reset(self) -> None:
        self._seen_checksums.clear()
        self._seen_fingerprints.clear()

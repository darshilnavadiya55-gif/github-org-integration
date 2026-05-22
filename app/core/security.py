import hashlib
import hmac
import secrets
from typing import Optional


def verify_github_signature(payload: bytes, signature_header: str, webhook_secret: str) -> bool:
    if not signature_header or not webhook_secret:
        return False

    expected_signature = "sha256=" + hmac.new(
        webhook_secret.encode("utf-8"),
        payload,
        digestmod=hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(expected_signature, signature_header)


def generate_state_token() -> str:
    return secrets.token_urlsafe(24)


def xor_encrypt_decrypt(value: str, key: str) -> str:
    """Placeholder reversible obfuscation for MVP only."""
    key_bytes = key.encode("utf-8")
    value_bytes = value.encode("utf-8")
    xored = bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(value_bytes)])
    return xored.hex()


def xor_decrypt(value_hex: str, key: str) -> Optional[str]:
    try:
        key_bytes = key.encode("utf-8")
        raw = bytes.fromhex(value_hex)
        original = bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(raw)])
        return original.decode("utf-8")
    except Exception:
        return None

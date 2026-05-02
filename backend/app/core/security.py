import hashlib
import hmac


def hash_value(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def constant_time_compare(left: str, right: str) -> bool:
    return hmac.compare_digest(left, right)


def authentication_enabled() -> bool:
    return False

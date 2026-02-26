import re

PROTOCOL_AND_DOMAIN_RE = re.compile(r"^(?:\w+:)?//(\S+)$")
LOCALHOST_DOMAIN_RE = re.compile(r"^localhost[:?\d]*(?:[^:?\d]\S*)?$")
NON_LOCALHOST_DOMAIN_RE = re.compile(r"^[^\s.]+\.\S{2,}$")

def is_url(url: str) -> bool:
    if not isinstance(url, str):
        return False

    match = PROTOCOL_AND_DOMAIN_RE.match(url)
    if not match:
        return False

    everything_after_protocol = match.group(1)
    if not everything_after_protocol:
        return False

    if (LOCALHOST_DOMAIN_RE.match(everything_after_protocol) or 
        NON_LOCALHOST_DOMAIN_RE.match(everything_after_protocol)):
        return True

    return False

BASE62_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def encode_base62(num: int) -> str:
    if num == 0:
        return BASE62_ALPHABET[0]
    base62 = []
    while num:
        num, rem = divmod(num, 62)
        base62.append(BASE62_ALPHABET[rem])
    return ''.join(reversed(base62))

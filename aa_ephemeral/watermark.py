import hashlib
import hmac

from django.conf import settings

ZWS = "​"   # zero-width space  = 0
ZWNJ = "‌"  # zero-width non-joiner = 1


def generate_watermark(user_id: int, message_id: int) -> str:
    """
    Generate a short unique code tied to a specific user + message.
    Deterministic — same user + same ping always produces the same code.
    """
    secret = settings.SECRET_KEY.encode()
    payload = f"{user_id}:{message_id}".encode()
    digest = hmac.new(secret, payload, hashlib.sha256).hexdigest()
    return digest[:8].upper()


def encode_invisible(user_id: int, message_id: int) -> str:
    """
    Encode the watermark as a string of zero-width unicode characters.
    Each hex character of the watermark is encoded as 4 bits of ZWS/ZWNJ.
    Completely invisible in Discord but survives copy-paste.
    """
    code = generate_watermark(user_id, message_id)
    bits = bin(int(code, 16))[2:].zfill(len(code) * 4)
    return "".join(ZWNJ if b == "1" else ZWS for b in bits)


def decode_invisible(text: str) -> str | None:
    """
    Extract and decode an invisible watermark from text that was copy-pasted.
    Returns the hex watermark code or None if no watermark found.
    """
    bits = ""
    for ch in text:
        if ch == ZWNJ:
            bits += "1"
        elif ch == ZWS:
            bits += "0"

    if not bits or len(bits) % 4 != 0:
        return None

    try:
        value = int(bits, 2)
        hex_str = hex(value)[2:].upper().zfill(len(bits) // 4)
        return hex_str
    except Exception:
        return None


def inject_watermark(text: str, user_id: int, message_id: int) -> str:
    """
    Inject invisible zero-width watermark characters after the first word of text.
    The watermark is undetectable visually but present in raw copied text.
    """
    invisible = encode_invisible(user_id, message_id)
    # Inject after the first space so it's buried in the middle of the message
    parts = text.split(" ", 1)
    if len(parts) == 1:
        return text + invisible
    return parts[0] + invisible + " " + parts[1]

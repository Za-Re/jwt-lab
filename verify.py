"""Validate a JWT the way an API would. Reads the token from stdin."""
import sys
from pathlib import Path

import jwt

ISSUER = "https://auth.example.com"
AUDIENCE = "orders-api"


def main() -> None:
    token = sys.stdin.read().strip()
    public_key = Path("keys/public.pem").read_text()
    try:
        claims = jwt.decode(
            token, public_key, algorithms=["RS256"], audience=AUDIENCE, issuer=ISSUER
        )
    except jwt.InvalidTokenError as exc:
        print(f"REJECTED  {type(exc).__name__}: {exc}")
        sys.exit(1)
    print(f"ACCEPTED  {claims}")


if __name__ == "__main__":
    main()

"""Issue an RS256-signed JWT (plays the authorization server)."""
import argparse
import time
from pathlib import Path

import jwt

ISSUER = "https://auth.example.com"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sub", default="user-123")
    parser.add_argument("--aud", default="orders-api")
    parser.add_argument("--ttl", type=int, default=300,
                        help="lifetime in seconds; negative = already expired")
    parser.add_argument("--key", default="keys/private.pem")
    args = parser.parse_args()

    now = int(time.time())
    claims = {
        "iss": ISSUER,
        "sub": args.sub,
        "aud": args.aud,
        "iat": now,
        "exp": now + args.ttl,
        "scope": "orders.read",
    }
    private_key = Path(args.key).read_text()
    print(jwt.encode(claims, private_key, algorithm="RS256", headers={"kid": "key-1"}))


if __name__ == "__main__":
    main()
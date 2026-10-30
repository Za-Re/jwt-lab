# jwt-lab

A small hands-on lab for seeing how JWT signing actually protects an API. You play three parts from the terminal:

- Issuer (`sign.py`) signs tokens with the private key.
- API (`verify.py`) checks them with the public key.
- Attacker (`tamper.py`) edits tokens without having the private key.

## Setup

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Generate a key pair. The private key belongs to the issuer only, so lock it down.

```sh
mkdir -p keys
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -out keys/private.pem
openssl pkey -in keys/private.pem -pubout -out keys/public.pem
chmod 600 keys/private.pem
```

Check that everything works. You should see `ACCEPTED` followed by the claims.

```sh
python sign.py | python verify.py
```

## Break it


| # | Attack | Command |
|---|--------|---------|
| A | Change the scope, keep the old signature | `python sign.py \| python tamper.py scope=orders.write \| python verify.py` |
| B | Valid token, but issued for another API | `python sign.py --aud billing-api \| python verify.py` |
| C | Valid token, but expired | `python sign.py --ttl -60 \| python verify.py` |
| D | Strip the signature and set `alg` to none | `python sign.py \| python tamper.py --none \| python verify.py` |
| E | Signed with the attacker's own key | see below |

For scenario E, the attacker makes their own key and signs with it:

```sh
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -out keys/attacker.pem
python sign.py --key keys/attacker.pem | python verify.py
```

### Expected results

| # | Output |
|---|--------|
| A | `REJECTED  InvalidSignatureError: Signature verification failed` |
| B | `REJECTED  InvalidAudienceError: Audience doesn't match` |
| C | `REJECTED  ExpiredSignatureError: Signature has expired` |
| D | `REJECTED  InvalidAlgorithmError: The specified alg value is not allowed` |
| E | `REJECTED  InvalidSignatureError: Signature verification failed` |

Anyone can read and edit a token, since it's only base64. What they can't do is produce a signature that the API's public key will accept.

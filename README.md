# jwt-lab

A small hands-on lab for seeing how JWT signing actually protects an API. You play three parts from the terminal:

- Issuer (`sign.py`) signs tokens with the private key.
- API (`verify.py`) checks them with the public key.
- Attacker (`tamper.py`) edits tokens without having the private key.
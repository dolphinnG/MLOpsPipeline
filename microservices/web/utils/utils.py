import os
import base64
import hashlib

def generate_code_verifier():
    return os.urandom(40).hex()

def generate_code_challenge(code_verifier):
    return (
        base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode("utf-8")).digest())
        .rstrip(b"=")
        .decode("utf-8")
    )

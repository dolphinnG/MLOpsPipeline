import os
import base64
import hashlib

from models.userModel import UserRead


def generate_code_verifier():
    return os.urandom(40).hex()


def generate_code_challenge(code_verifier):
    return (
        base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode("utf-8")).digest())
        .rstrip(b"=")
        .decode("utf-8")
    )


def ldap_entry_to_dict(entry_with_group): # cant do model_validate_json
    entry = entry_with_group[0]
    groups = entry_with_group[1]
    return UserRead(
        name=entry["cn"].value,
        mail=entry["mail"].value,
        title=entry["title"].value,
        location=entry["l"].value,
        telephoneNumber=entry["telephoneNumber"].value,
        groups=groups,
        uid=entry["uid"].value,
    )

"""Message signing utilities for Technocore."""

import base64

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey


def sign_message(
    private_key: Ed25519PrivateKey,
    message: str,
) -> str:
    """Sign a message and return a base64url signature."""

    signature = private_key.sign(message.encode("utf-8"))

    return base64.urlsafe_b64encode(signature).decode("ascii").rstrip("=")

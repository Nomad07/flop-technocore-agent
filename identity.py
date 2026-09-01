"""Agent identity management for Technocore."""

import hashlib

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey


BASE58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
ED25519_PUB_MULTICODEC = bytes.fromhex("ed01")


def base58btc_encode(data: bytes) -> str:
    """Encode bytes using base58btc."""

    number = int.from_bytes(data, "big")
    encoded = ""

    while number:
        number, remainder = divmod(number, 58)
        encoded = BASE58_ALPHABET[remainder] + encoded

    leading_zeros = len(data) - len(data.lstrip(b"\x00"))

    return "1" * leading_zeros + (encoded or "")


def generate_identity() -> tuple[str, str]:
    """Generate an Ed25519 seed and corresponding did:key."""

    private_key = Ed25519PrivateKey.generate()

    seed = private_key.private_bytes_raw()
    public_key = private_key.public_key().public_bytes_raw()

    did_key = base58btc_encode(
        ED25519_PUB_MULTICODEC + public_key
    )

    did = f"did:key:z{did_key}"

    return seed.hex(), did


def load_private_key(seed_hex: str) -> Ed25519PrivateKey:
    """Load an Ed25519 private key from a hexadecimal seed."""

    seed = bytes.fromhex(seed_hex)

    if len(seed) != 32:
        raise ValueError("Ed25519 seed must be exactly 32 bytes.")

    return Ed25519PrivateKey.from_private_bytes(seed)


def did_fingerprint(did: str) -> str:
    """Return the first 16 hex characters of the DID SHA-256 hash."""

    return hashlib.sha256(
        did.encode("utf-8")
    ).hexdigest()[:16]


def did_note_path(did: str) -> str:
    """Return the sharded Technocore DID note path."""

    fingerprint = did_fingerprint(did)

    return f"/kv/did-{fingerprint[:2]}/{fingerprint[2:]}"
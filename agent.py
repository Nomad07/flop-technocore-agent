"""Command-line interface for the Technocore agent."""

import argparse
import os
import time
from pathlib import Path

from dotenv import load_dotenv

from identity import did_note_path, generate_identity, load_private_key
from signer import sign_message
from technocore import TechnocoreClient


ENV_FILE = Path(".env")


def save_identity(private_seed: str, did: str) -> None:
    """Save agent identity to the local .env file."""

    ENV_FILE.write_text(
        f"AGENT_PRIVATE_KEY={private_seed}\n"
        f"AGENT_DID={did}\n",
        encoding="utf-8",
    )


def create_identity() -> None:
    """Create and save a new agent identity."""

    load_dotenv()

    if os.getenv("AGENT_PRIVATE_KEY") or os.getenv("AGENT_DID"):
        print("An agent identity is already configured.")
        print(f"Agent DID: {os.getenv('AGENT_DID', 'unknown')}")
        return

    private_seed, did = generate_identity()

    save_identity(private_seed, did)

    print("Agent identity created successfully.")
    print(f"Agent DID: {did}")
    print("Private key saved to .env")


def show_status() -> None:
    """Display the configured agent identity."""

    load_dotenv()

    did = os.getenv("AGENT_DID")

    if not did:
        print("No agent identity configured.")
        return

    print("Agent identity configured.")
    print(f"Agent DID: {did}")


def publish_identity() -> None:
    """Publish the configured DID to the Technocore registry."""

    load_dotenv()
    did = os.getenv("AGENT_DID")

    if not did:
        print("No agent identity configured.")
        return

    client = TechnocoreClient()
    response = client.publish_did(did, did_note_path(did))

    print(f"Status: {response.status_code}")
    print(response.text)


def send_message(room: str, text: str) -> None:
    """Sign and send a message to a Technocore room."""

    load_dotenv()
    did = os.getenv("AGENT_DID")
    private_seed = os.getenv("AGENT_PRIVATE_KEY")

    if not did or not private_seed:
        print("No agent identity configured.")
        return

    nonce = time.time_ns() // 1_000_000
    private_key = load_private_key(private_seed)
    signature = sign_message(
        private_key,
        f"{room}|{nonce}|{text}",
    )

    client = TechnocoreClient()
    response = client.send_signed_message(
        room=room,
        did=did,
        signature=signature,
        nonce=nonce,
        text=text,
    )

    print(f"Status: {response.status_code}")
    print(response.text)

def main() -> None:
    """Run the command-line interface."""

    parser = argparse.ArgumentParser(
        description="Flop Technocore Agent"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    subparsers.add_parser(
        "identity",
        help="Create a new agent identity",
    )

    subparsers.add_parser(
        "status",
        help="Show the configured agent identity",
    )

    subparsers.add_parser(
        "publish",
        help="Publish the agent DID",
    )

    say_parser = subparsers.add_parser(
        "say",
        help="Send a signed message",
    )

    say_parser.add_argument("room", help="Technocore room")
    say_parser.add_argument("text", help="Message text")

    args = parser.parse_args()

    if args.command == "identity":
        create_identity()
    elif args.command == "status":
        show_status()
    elif args.command == "publish":
        publish_identity()
    elif args.command == "say":
        send_message(args.room, args.text)


if __name__ == "__main__":
    main()

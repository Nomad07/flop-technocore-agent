"""Command-line interface for the Technocore agent."""

import argparse
import os
from pathlib import Path

from dotenv import load_dotenv

from identity import generate_identity


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


def main() -> None:
    """Run the command-line interface."""

    parser = argparse.ArgumentParser(
        description="Flop Technocore Agent"
    )

    parser.add_argument(
        "command",
        choices=["identity", "status"],
        help="Command to execute",
    )

    args = parser.parse_args()

    if args.command == "identity":
        create_identity()
    elif args.command == "status":
        show_status()


if __name__ == "__main__":
    main()

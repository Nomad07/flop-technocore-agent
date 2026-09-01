"""Command-line interface for the Technocore agent."""

import argparse
import os

from dotenv import load_dotenv

from identity import generate_identity


def create_identity():
    """Create and display a new agent identity."""

    private_seed, did = generate_identity()

    print(f"Agent DID: {did}")
    print(f"Private seed: {private_seed}")
    print()
    print("Store the private seed securely. Never commit it to Git.")


def show_status():
    """Display the configured agent identity."""

    load_dotenv()

    did = os.getenv("AGENT_DID")

    if not did:
        print("No agent identity configured.")
        return

    print(f"Agent DID: {did}")


def main():
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

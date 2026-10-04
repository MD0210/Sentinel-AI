"""Sentinel AI command-line entry point with wake-call and authentication."""

from agent.controller import SentinelAgent


def main() -> None:
    sentinel = SentinelAgent()

    print("Sentinel AI starting...")
    print("Say the wake phrase to activate Sentinel.")

    while True:
        wake_text = input("Wake phrase: ")

        if wake_text.strip().lower() in {"exit", "quit"}:
            return

        if sentinel.check_wake_call(wake_text):
            break

        print("Wake phrase not recognized.")

    print("Wake phrase recognized.")
    print("Authentication required.")
    print("Use the secure Q&A fallback to authenticate.")

    if not sentinel.authenticate_fallback_from_environment():
        print("Authentication failed. Sentinel will not accept requests.")
        return

    print("Sentinel authenticated.")

    while True:
        request = input("You: ")

        if request.strip().lower() in {"exit", "quit"}:
            break

        response = sentinel.handle_request(request)
        print(f"Sentinel: {response}")


if __name__ == "__main__":
    main()

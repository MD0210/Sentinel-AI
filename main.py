from agent.controller import SentinelAgent


def main() -> None:
    sentinel = SentinelAgent()

    print("Sentinel AI starting...")
    print(sentinel.authenticate())

    while True:
        request = input("You: ")

        if request.strip().lower() in {"exit", "quit"}:
            break

        response = sentinel.handle_request(request)
        print(f"Sentinel: {response}")


if __name__ == "__main__":
    main()

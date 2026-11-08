"""CLI for vector-clock-scratchpad."""
import sys
import argparse
from .scratchpad import VectorClockScratchpad


def main():
    parser = argparse.ArgumentParser(description="Vector Clock Scratchpad CLI")
    parser.add_argument("--demo", action="store_true", help="Run vector clock causality demo")
    args = parser.parse_args()

    if args.demo:
        s1 = VectorClockScratchpad("agent_1")
        s2 = VectorClockScratchpad("agent_2")

        n1 = s1.write_note("task_goal", "Optimize database indexing")
        n2 = s2.write_note("task_goal", "Refactor GraphQL resolvers")

        rel = s1.compare_clocks(n1.clock, n2.clock)
        print(f"[*] Causal relationship between concurrent writes: {rel}")
        conflicts = s1.merge_remote(s2)
        print(f"[+] Detected concurrent conflicts on merge: {conflicts}")
    else:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()

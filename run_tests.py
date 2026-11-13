"""Run every Lab 8 test file and print a PASS/FAIL summary."""
import subprocess
import sys

TESTS: list[str] = [
    "test_association.py",
    "test_aggregation.py",
    "test_composition.py",
    "test_lsp.py",
    "test_polymorphism.py",
]


def run_test(filename: str) -> bool:
    print(f"\n{'=' * 20} {filename} {'=' * 20}")
    result = subprocess.run([sys.executable, filename])
    return result.returncode == 0


def main() -> None:
    results: dict[str, bool] = {name: run_test(name) for name in TESTS}
    print(f"\n{'=' * 20} SUMMARY {'=' * 20}")
    for name, passed in results.items():
        print(f"{'PASS' if passed else 'FAIL'}  {name}")
    print(f"{sum(results.values())}/{len(results)} test files passed")
    sys.exit(0 if all(results.values()) else 1)


if __name__ == "__main__":
    main()

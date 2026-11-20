"""Run every Lab 8 script test and the Lab 9 automated unit test suite."""
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


def run_unit_tests() -> bool:
    print(f"\n{'=' * 20} tests/ (Lab 9 unittest) {'=' * 20}")
    result = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"])
    return result.returncode == 0


def main() -> None:
    results: dict[str, bool] = {name: run_test(name) for name in TESTS}
    results["tests/ (Lab 9 unittest)"] = run_unit_tests()
    print(f"\n{'=' * 20} SUMMARY {'=' * 20}")
    for name, passed in results.items():
        print(f"{'PASS' if passed else 'FAIL'}  {name}")
    print(f"{sum(results.values())}/{len(results)} test suites passed")
    sys.exit(0 if all(results.values()) else 1)


if __name__ == "__main__":
    main()

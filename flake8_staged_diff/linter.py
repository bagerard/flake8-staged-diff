import argparse
import sys


def run_dummy_check(*args, **kwargs):
    return None, None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("instancefiles", nargs="+", help="JSON or YAML files to check.")

    args = parser.parse_args()

    success, messages = run_dummy_check(args)

    for message in messages:
        print(message)

    if success:
        sys.exit(0)
    else:
        sys.exit(1)

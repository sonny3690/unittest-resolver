import argparse
from parser import doWork

parser = argparse.ArgumentParser(
    description="Run all unit tests specific to a function",
)

parser.add_argument(
    "--module",
    type=str,
    required=True,
    help="Specify the name of the module (must be in same directory for now)"
)

parser.add_argument(
    "--target",
    type=str,
    required=True,
    help="Name of the target function that you want to run unittests on"
)

args = parser.parse_args()

assert args.module and args.target

print(doWork(args.module, args.target))

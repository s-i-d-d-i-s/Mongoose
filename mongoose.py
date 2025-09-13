import argparse
import sys
import os
# To make this runnable, we need to ensure the 'commands' directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from commands import initialize, normalize, generate




def main():
    """Main function to parse arguments and delegate commands."""
    parser = argparse.ArgumentParser(
        description="Mongoose: A CLI tool for calculating capital gains tax, dividends, and interest."
    )
    # Adding a destination for the subparsers is crucial to identify which command was used.
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    subparsers.required = True # Makes sure a command is provided

    # Register each command from its own module
    initialize.register_command(subparsers)
    normalize.register_command(subparsers)
    generate.register_command(subparsers)
    
    # If no arguments are provided, print the help message
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()


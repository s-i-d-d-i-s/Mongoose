def handle_normalize(args):
    """Handles the 'normalize' command."""
    print("Executing 'normalize' command...")
    print(f"  Broker: {args.broker}")
    print(f"  Input File: {args.file}")
    print("This would normally clean and standardize the broker data.")
    print(f"A file like 'normalized/{args.broker}.json' would be created.")
    print("-" * 20)

def register_command(subparsers):
    """Registers the 'normalize' command and its arguments."""
    parser_normalize = subparsers.add_parser(
        'normalize',
        help='Import and normalize raw data from a specific broker.'
    )
    parser_normalize.add_argument(
        '--broker',
        required=True,
        choices=['IBKR', 'T212'],
        help='The broker code for the data file being imported.'
    )
    parser_normalize.add_argument(
        '--file',
        required=True,
        help='The path to the raw data file from the broker.'
    )
    parser_normalize.set_defaults(func=handle_normalize)

from commands import forex_handler, t212_handler
import pandas as pd


def validate_request(args):
    if args.broker == "T212" and not args.file.lower().endswith(".csv"):
        print("Error: Only .csv files are supported for T212 broker.")
        return False
    return True


def normalize_t212(file_path):
    import os, json
    try:
        data = pd.read_csv(file_path)
        forex= forex_handler.ForexHandler()
        trading212_handler = t212_handler.Trading212Handler(data, "USD", forex)
        normalized_data = trading212_handler.get_normalized_data()
        # Ensure the directory exists
        os.makedirs('normalized', exist_ok=True)
        with open(f'normalized/T212.json', 'w') as f:
            f.write(json.dumps(normalized_data))

    except Exception as e:
        print(f"Error reading file: {e}")
        return

def handle_normalize(args):
    """Handles the 'normalize' command."""
    if not validate_request(args):
        return

    print("Executing 'normalize' command...")
    print(f"  Broker: {args.broker}")
    print(f"  Input File: {args.file}")
    print("-" * 20)
    print("We would now clean and standardize the broker data.")

    if args.broker == "T212":
        normalize_t212(args.file)

    print("-" * 20)
    print(f"The cleaned data is stored in 'normalized/{args.broker}.json'")
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

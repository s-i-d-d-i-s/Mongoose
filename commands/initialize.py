from commands import forex_handler


def handle_initialize(args):
    """Handles the 'initialize' command."""
    print("Executing 'initialize' command...")
    forex_handler.ForexHandler()
    print("Forex rates fetched and cached successfully.")
    print("-" * 20)

def register_command(subparsers):
    """Registers the 'initialize' command and its arguments."""
    parser_init = subparsers.add_parser(
        'init',
        help='Initialize Mongoose and fetch necessary external data like Forex rates.'
    )
    parser_init.set_defaults(func=handle_initialize)

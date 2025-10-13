from commands.report_generator import ReportGenerator

def handle_generate(args):
    """Handles the 'generate' command."""
    print("Executing 'generate' command...")
    print(f"  Output Report File: {args.report}")
    print(f"  Currency: {args.currency}")
    print("This would normally calculate capital gains and create the final report.")
    print("-" * 20)
    report_generator = ReportGenerator(args.report, args.currency)
    report_generator.generate_report()
    print("-" * 20)
    print("Report Generation Completed.")
    

def register_command(subparsers):
    """Registers the 'generate' command and its arguments."""
    parser_generate = subparsers.add_parser(
        'generate',
        help='Generate the final tax report from all normalized data.'
    )
    parser_generate.add_argument(
        '--report',
        required=True,
        help='The filename for the output report (e.g., tax_report).'
    )
    parser_generate.add_argument(
        '--currency',
        required=True,
        help='The currency for the final report (e.g., USD, EUR, GBP).'
    )
    parser_generate.set_defaults(func=handle_generate)

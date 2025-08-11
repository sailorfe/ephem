from .cli import parse_arguments
from .config import save_config

def main():
    args = parse_arguments()

    if not vars(args):
        args.print_help()
        args.exit(1)

    if args.save_config:
        save_config(args)
        return

    if hasattr(args, "func"):
        # Dispatch to the subcommand's run function
        args.func(args)
    else:
        # No subcommand provided; show help and exit with error
        args.print_help()
        args.exit(1)


if __name__ == "__main__":
    main()

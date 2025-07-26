import argparse

def init_parser() ->argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="VinayakaHomeServer", description="A Local WAN Home Data Server")
    parser.add_argument("--data-dir", "-dir",
                        default="/media/neeraj-r-rugi/NEERAJ_DRIVE",
                        help="The Directory which the server is to host.")
    parser.add_argument("--password", "-ps",
                        default="Dingus",
                        help="The Password for Logging into your server.")
    parser.add_argument("--exclude-dir", "-ed",
                        nargs="+",
                        help="List The Directories to be Excluded.")
    parser.add_argument("--debug", "-db",
                        action="store_true",
                        help="Enable Debug Mode for Flask")
    return parser
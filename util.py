import argparse
import secrets
import string

def init_parser() ->argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="VinayakaHomeServer", description="A Local WAN Home Data Server")
    parser.add_argument("--data-dir", "-dir",
                        default="./",
                        help="The Directory which the server is to host.")
    parser.add_argument("--password", "-ps",
                        default="Dingus",
                        help="The Password for Logging into your server.")
    parser.add_argument("--exclude-dir", "-ed",
                        nargs="+",
                        default=[],
                        help="List The Directories to be Excluded.")
    parser.add_argument("--debug", "-db",
                        action="store_true",
                        help="Enable Debug Mode for Flask")
    parser.add_argument("--generate", "-gen",
                        action="store_true",
                        help="Generates a Secure 32 character long Password.")
    return parser


def generate_password(len = 32)->str:
    char = string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation
    return ''.join(secrets.choice(char) for _ in range(len))
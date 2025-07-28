# Vinayaka Home Server: A Secure local file server with HTTPS, password hashing & network access. Perfect for students accessing files across devices on trusted networks. 
# Copyright (C) 2024 NEERAJ R RUGI

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
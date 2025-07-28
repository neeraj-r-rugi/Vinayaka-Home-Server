
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


from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, abort, send_file
from pathlib import Path
import os
import secrets
import io
import zipfile
import util
from werkzeug.security import generate_password_hash, check_password_hash
server = Flask(__name__)
server.secret_key = secrets.token_hex(32)

# Configuration
PASSWORD = str()
BASE_DIR = str()
EXCLUDED_DIRS = list()

# Routes
@server.route('/', methods=['GET', 'POST'])
def main():
    if request.method == "POST":
        user_password = request.form['password']
        if check_password_hash(PASSWORD, user_password):
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            return render_template('index.html', error="Accesses Key Invalid.")
    
    return render_template('index.html')


@server.route('/dashboard/', defaults={'req_path': ''})
@server.route('/dashboard/<path:req_path>')
def dashboard(req_path=''):
    if not session.get('logged_in'):
        return redirect(url_for('main'))

    base_path = Path(BASE_DIR).resolve()
    abs_path = (base_path / req_path).resolve()

    # Prevent directory traversal
    if not str(abs_path).startswith(str(base_path)):
        return abort(403)

    if abs_path.is_file():
        return send_from_directory(abs_path.parent, abs_path.name, as_attachment=False)

    if abs_path.is_dir():
        file_links = []
        for f in abs_path.iterdir():
            # Compute the relative path from BASE_DIR for exclusion check
            rel_path = f.relative_to(base_path)
            rel_path_str = str(rel_path).replace("\\", "/").rstrip("/")

            # Exclude if any excluded dir matches the start of the path
            exclude = False
            for ex in EXCLUDED_DIRS:
                ex_norm = ex.strip("/\\")
                # Exclude if the rel_path matches or is a subpath of ex
                if rel_path_str == ex_norm or rel_path_str.startswith(ex_norm + "/"):
                    exclude = True
                    break
            if exclude:
                continue

            display_name = f.name
            link_path = url_for('dashboard', req_path=str(rel_path))
            file_links.append((display_name, link_path, f.is_dir()))

        return render_template('dashboard.html', req_path=req_path, files=file_links)

    return abort(404)


@server.route('/download-zip/', defaults={'req_path': ''})
@server.route('/download-zip/<path:req_path>')
def download_zip(req_path=''):
    if not session.get('logged_in'):
        return redirect(url_for('main'))

    base_path = Path(BASE_DIR).resolve()
    abs_path = (base_path / req_path).resolve()

    # Prevent directory traversal
    if not str(abs_path).startswith(str(base_path)):
        return abort(403)

    if not abs_path.is_dir():
        return abort(404)

    # Prepare normalized excluded paths (as strings, root-relative)
    excluded = [ex.strip("/\\") for ex in EXCLUDED_DIRS]

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for file_path in abs_path.rglob('*'):
            # Compute root-relative path for exclusion
            rel_path_from_root = file_path.relative_to(base_path)
            rel_path_str = str(rel_path_from_root).replace("\\", "/").rstrip("/")

            # Exclude if any excluded dir matches the start of the path
            skip = False
            for ex in excluded:
                if rel_path_str == ex or rel_path_str.startswith(ex + "/"):
                    skip = True
                    break
            if skip or file_path.is_dir():
                continue

            # Path inside the zip should be relative to the zipped folder
            rel_path_in_zip = file_path.relative_to(abs_path)
            zip_file.write(file_path, str(rel_path_in_zip))

    zip_buffer.seek(0)
    folder_name = abs_path.name or 'root'
    return send_file(
        zip_buffer,
        mimetype='application/zip',
        as_attachment=True,
        download_name=f"{folder_name}.zip"
    )


if __name__ == "__main__":
    parser = util.init_parser()
    user_args = parser.parse_args()
    user_args= {"directory":user_args.data_dir, "password": user_args.password, "Exclude":user_args.exclude_dir,
                "debug":user_args.debug, "generate":user_args.generate}
    BASE_DIR = user_args['directory']
    if(user_args['generate']):
        #If User Provides Password and generate tag in argument, Then generate Argument is Overriden.
        passkey = util.generate_password()
        print(f"Your Secure Passkey is: {passkey}")
        PASSWORD = generate_password_hash(passkey, method="pbkdf2:sha256")
    else:
        PASSWORD = generate_password_hash(user_args['password'], method="pbkdf2:sha256")

    EXCLUDED_DIRS = user_args['Exclude']
    if(user_args['debug']):
        server.run(host="0.0.0.0", port=5000, debug=True, ssl_context = "adhoc")
    else:
        server.run(host="0.0.0.0", port=5000, ssl_context = "adhoc")
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, abort, send_file
from pathlib import Path
import os
import secrets
import io
import zipfile
import util

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
        password = request.form['password']
        if password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            return render_template('index.html', error="Invalid Password")
    
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

    # Prepare normalized excluded paths
    excluded = [Path(ex.strip("/\\")).parts for ex in EXCLUDED_DIRS]

    # Create in-memory ZIP
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for file_path in abs_path.rglob('*'):
            rel_path = file_path.relative_to(abs_path)
            rel_parts = rel_path.parts

            # Exclude if any excluded path matches the start of rel_parts
            skip = False
            for ex_parts in excluded:
                if len(ex_parts) > 0 and rel_parts[:len(ex_parts)] == ex_parts:
                    skip = True
                    break
            if skip or file_path.is_dir():
                continue

            zip_file.write(file_path, str(rel_path))

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
                "debug":user_args.debug}
    BASE_DIR = user_args['directory']
    PASSWORD = user_args['password']
    EXCLUDED_DIRS = user_args['Exclude']
    if(user_args['debug']):
        server.run(host="0.0.0.0", port=5000, debug=True)
    else:
        server.run(host="0.0.0.0", port=5000)
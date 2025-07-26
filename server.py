from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, abort, send_file
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

    abs_path = os.path.join(BASE_DIR, req_path)
    
    if not os.path.commonprefix([abs_path, BASE_DIR]) == BASE_DIR:
        return abort(403)

    if os.path.isfile(abs_path):
        return send_from_directory(os.path.dirname(abs_path), os.path.basename(abs_path), as_attachment=False)

    if os.path.isdir(abs_path):
        files = os.listdir(abs_path)
        file_links = []

        for f in files:
            if EXCLUDED_DIRS:
                if f in EXCLUDED_DIRS:
                    continue  # Skip excluded directories
            
            full_path = os.path.join(req_path, f) if req_path else f
            abs_full_path = os.path.join(BASE_DIR, full_path)

            # Determine if it's a directory or file and create appropriate link
            if os.path.isdir(abs_full_path):
                display_name = f
                link_path = url_for('dashboard', req_path=full_path)
            else:
                display_name = f
                link_path = url_for('dashboard', req_path=full_path)
            
            file_links.append((display_name, link_path, os.path.isdir(abs_full_path)))

        return render_template('dashboard.html', req_path=req_path, files=file_links)

    return abort(404)


@server.route('/download-zip/', defaults={'req_path': ''})
@server.route('/download-zip/<path:req_path>')
def download_zip(req_path=''):
    if not session.get('logged_in'):
        return redirect(url_for('main'))

    abs_path = os.path.join(BASE_DIR, req_path) if req_path else BASE_DIR

    if not os.path.commonprefix([abs_path, BASE_DIR]) == BASE_DIR:
        return abort(403)

    if not os.path.isdir(abs_path):
        return abort(404)

    # Create in-memory ZIP
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(abs_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, abs_path)
                zip_file.write(file_path, arcname)

    zip_buffer.seek(0)
    folder_name = os.path.basename(abs_path.rstrip('/')) or 'root'
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
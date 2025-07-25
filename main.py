from flask import Flask, render_template,  request, redirect, url_for, session, send_from_directory, abort, render_template_string
import os
import secrets
server = Flask(__name__)
server.secret_key=secrets.token_hex(32)

#Defines
PASSWORD = "YOUR-PASSWORD"
BASE_DIR = "./YOUR-HARDDRIVE"
EXCLUDED_DIRS = ["YOUR EXCLUDED DIRS"]

@server.route('/', methods=['GET', 'POST'])
def main():
    if request.method == "POST":
        password = request.form['password']
        if password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            return render_template('index.html', error = "Invalid Password")
    
    return render_template('index.html')

@server.route('/dashboard/', defaults={'req_path': ''})
@server.route('/dashboard/<path:req_path>')
def dashboard(req_path):
    abs_path = os.path.join(BASE_DIR, req_path)

    if not session.get('logged_in'):
        return redirect(url_for('main'))

    if not os.path.commonprefix([abs_path, BASE_DIR]) == BASE_DIR:
        return abort(403)

    if os.path.isfile(abs_path):
        return send_from_directory(os.path.dirname(abs_path), os.path.basename(abs_path), as_attachment=False)

    if os.path.isdir(abs_path):
        files = os.listdir(abs_path)
        file_links = []

        for f in files:
            if f in EXCLUDED_DIRS:
                continue  # Skip excluded directories
            full_path = os.path.join(req_path, f)
            abs_full_path = os.path.join(BASE_DIR, full_path)

            display_name = f + "/" if os.path.isdir(abs_full_path) else f
            file_links.append((display_name, f"/dashboard/{full_path}"))

        return render_template('dashboard.html', req_path=req_path, files=file_links)

    return abort(404)

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000)
from flask import render_template, request, redirect, url_for, flash, send_from_directory
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from . import db, socketio, login_manager
from .models import User, Thread, FileUpload
from flask import current_app as app
import os
import time

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def index():
    return redirect(url_for('login'))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.password == request.form['password']:
            login_user(user)
            return redirect(url_for("forum"))
        flash("Invalid credentials")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if User.query.filter_by(username=request.form['username']).first():
            flash("Username already taken")
        else:
            user = User(username=request.form['username'], password=request.form['password'])
            db.session.add(user)
            db.session.commit()
            flash("Registered successfully")
            return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/forum", methods=["GET", "POST"])
@login_required
def forum():
    if request.method == "POST":
        content = request.form['content']
        new_thread = Thread(content=content)
        db.session.add(new_thread)
        db.session.commit()
    threads = Thread.query.order_by(Thread.timestamp.desc()).all()
    return render_template("forum.html", threads=threads, user=current_user)

@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    if request.method == "POST":
        f = request.files['file']
        f.seek(0, os.SEEK_END)
        size = f.tell()
        f.seek(0)

        if size > 100 * 1024 * 1024:
            flash("File too large. Upload here: https://www.dropbox.com/scl/fo/mm5f8x63xf91cl5rxjh82/AG1C9IkSGPEGjP_I9jdZtMk?rlkey=tvxs1j794w1zq8123oz77c1s8&st=gcdumu0u&dl=0")
            return redirect(url_for("upload"))

        filename = secure_filename(f.filename)
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        f.save(save_path)
        db.session.add(FileUpload(filename=filename, path=save_path))
        db.session.commit()
        flash("Upload successful")
    return render_template("upload.html")

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

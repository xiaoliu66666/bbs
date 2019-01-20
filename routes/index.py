import os

from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    flash,
    send_from_directory)

from config import Config

from models.user import User
from werkzeug.utils import secure_filename
from routes import current_user
from utils import log

main = Blueprint('index', __name__)

"""
用户在这里可以
    访问首页
    注册
    登录

用户登录后, 会写入 session, 并且定向到 /profile
"""


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/register", methods=['POST'])
def register():
    form = request.form
    # 用类函数来判断
    User.register(form)
    return redirect(url_for('.index'))


@main.route("/login", methods=['POST'])
def login():
    form = request.form
    log("form: ", form)
    u = User.validate_login(form)
    if u is None:
        # 转到 topic.index 页面
        return redirect(url_for('topic.index'))
    else:
        # session 中写入 user_id
        session['user_id'] = u['_id']
        # 设置 cookie 有效期为 永久
        session.permanent = True
        return redirect(url_for('.profile'))


@main.route('/profile')
def profile():
    u = current_user()
    if u is None:
        return redirect(url_for('.index'))
    else:
        return render_template('profile.html', user=u)


def allow_file(filename):
    suffix = filename.split(".")[-1]
    return suffix in Config.ACCEPT_TYPE


@main.route('/addimg', methods=["POST"])
def add_img():
    u = current_user()

    if u is None:
        return redirect(url_for('.index'))

    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        flash('未选择文件')
        return redirect(request.url)

    if allow_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(Config.UPLOAD_FOLDER, filename))
        u.user_image = filename
        u.save()

    return redirect(url_for('.profile'))


@main.route("/uploads/<filename>")
def uploads(filename):
    return send_from_directory(Config.UPLOAD_FOLDER, filename)

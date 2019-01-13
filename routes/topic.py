from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    abort,
)

from routes import *

from models.topic import Topic


main = Blueprint('topic', __name__)

import uuid
csrf_token = set()


@main.route("/")
def index():
    ms = Topic.all()
    token = str(uuid.uuid4())
    csrf_token.add(token)
    return render_template("topic/index.html", ms=ms, token=token)


@main.route('/<int:id>')
def detail(id):
    topic = Topic.get(id)
    # 传递 topic 的所有 reply 到 页面中
    return render_template("topic/detail.html", topic=topic)


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    u = current_user()
    m = Topic.new(form, user_id=u.id)
    return redirect(url_for('.detail', id=m.id))


@main.route("/delete")
def delete():
    id = int(request.args.get("id"))
    token = request.args.get("token")
    # 判断token是否是我们给的
    if token in csrf_token:
        csrf_token.remove(token)
        u = current_user()
        if u is not None:
            Topic.delete(id)
            return redirect(url_for('.index'))
        else:
            abort(404)
    else:
        abort(403)


@main.route("/new")
def new():
    return render_template("topic/new.html")

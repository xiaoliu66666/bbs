from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    abort,
    flash)
from routes import current_user

from models.board import Board
from models.topic import Topic
import uuid

from utils import log

main = Blueprint('topic', __name__)


csrf_tokens = dict()


@main.route("/")
def index():
    board_id = request.args.get("board_id", -1)
    if board_id == -1:
        ts = Topic.all()
    else:
        ts = Topic.find_all(board_id=board_id)
    bs = Board.all()
    u = current_user()
    if u is not None:
        token = str(uuid.uuid4())
        csrf_tokens[token] = u.id
        return render_template("topic/index.html", ts=ts, token=token, bs=bs)
    else:
        return render_template("topic/index.html", bs=bs)


@main.route('/<int:id>')
def detail(id):
    topic = Topic.get(id)
    board = topic.board()
    user = topic.user()
    return render_template("topic/detail.html",
                           topic=topic, board=board, user=user)


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    u = current_user()
    log("u: ", u)
    m = Topic.new(form, user_id=u.id)
    log("m :", m)
    return redirect(url_for('.detail', id=m.id))


@main.route("/delete")
def delete():
    id = request.args.get("id")
    u = current_user()
    token = request.args.get("token")
    # 判断token是否是我们给的
    if token in csrf_tokens and csrf_tokens[token] == u.id:
        csrf_tokens.pop(token)
        if u is not None:
            Topic.delete(id)
            return redirect(url_for('.index'))
        else:
            abort(404)
    else:
        flash("对不起你没有权限")
        return redirect(url_for('.index'))


@main.route("/new")
def new():
    bs = Board.all()
    return render_template("topic/new.html", bs=bs)

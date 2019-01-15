from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    abort,
)

from models.board import Board
from models.topic import Topic
import uuid
import routes

main = Blueprint('topic', __name__)


csrf_token = set()


@main.route("/")
def index():
    board_id = int(request.args.get("board_id", -1))
    if board_id == -1:
        ts = Topic.all()
    else:
        ts = Topic.find_all(board_id=board_id)
    token = str(uuid.uuid4())
    csrf_token.add(token)
    bs = Board.all()
    return render_template("topic/index.html", ts=ts, token=token, bs=bs)


@main.route('/<int:id>')
def detail(id):
    topic = Topic.get(id)
    board = Board.find(topic.board_id)
    return render_template("topic/detail.html", topic=topic, board=board)


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    u = routes.current_user()
    m = Topic.new(form, user_id=u.id)
    return redirect(url_for('.detail', id=m.id))


@main.route("/delete")
def delete():
    id = int(request.args.get("id"))
    token = request.args.get("token")
    # 判断token是否是我们给的
    if token in csrf_token:
        csrf_token.remove(token)
        u = routes.current_user()
        if u is not None:
            Topic.delete(id)
            return redirect(url_for('.index'))
        else:
            abort(404)
    else:
        abort(403)


@main.route("/new")
def new():
    bs = Board.all()
    return render_template("topic/new.html", bs=bs)

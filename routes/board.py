from flask import (
    request,
    redirect,
    url_for,
    Blueprint,
    render_template,
)


from models.board import Board

main = Blueprint('board', __name__)


@main.route("/")
def index():
    return render_template("board/admin_index.html")


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    b = Board.new(form)
    b.save()
    return redirect(url_for('.index'))

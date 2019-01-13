from flask import (
    Blueprint,
    render_template,
)

main = Blueprint('exception', __name__)


@main.app_errorhandler(404)
def error(e):
    return render_template("error/404.html")

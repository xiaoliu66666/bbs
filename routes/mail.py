from flask import (
    request,
    redirect,
    url_for,
    Blueprint,
    render_template,
)

from routes import current_user

from models.mail import Mail


main = Blueprint('mail', __name__)


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    u = current_user()
    mail = Mail.new(form)
    mail.save()
    # 开始时sender_id被设置为-1，不能直接从request中获取
    mail.set_sender(u.id)
    return redirect(url_for('.index'))


@main.route("/")
def index():
    u = current_user()
    sent = Mail.find_all(sender_id=u.id)
    received = Mail.find_all(receiver_id=u.id)
    return render_template('mail/index.html', sents=sent, receiveds=received)


@main.route("/views/id")
def view(id):
    """
    注意安全问题，首先确定登录的用户是收件人，如果不是就不能标记已读；
    另外只有当用户是收/发件人时，才能查看邮件详情
    :param id: 传入的邮件id
    :return: 对应的邮件
    """
    mail = Mail.find(id)
    u = current_user()
    if u.id == mail.receiver_id:
        mail.mark_read()
    if u.id in [mail.receiver_id, mail.sender_id]:
        return render_template('mail/detail.html', mail=mail)

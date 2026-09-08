from flask import Blueprint, request, render_template, redirect, url_for
from  flask_login import login_required
from models import db, Memo

memo_bp = Blueprint("memo", __name__, url_prefix="/memo")

@memo_bp.route("/", methods=["GET", "POST"])
@login_required
def memo():
    if request.method == "POST":
        content = request.form.get("content", "").strip()
        if content:
            new_memo = Memo(content=content)
            db.session.add(new_memo)
            db.session.commit()
    all_memos = Memo.query.all()
    return render_template("memo.html", memos=all_memos)

@memo_bp.route("/delete/<int:memo_id>", methods=["POST"])
@login_required
def delete_memo(memo_id):
    memo_to_delete = Memo.query.get_or_404(memo_id)
    db.session.delete(memo_to_delete)
    db.session.commit()
    return redirect(url_for("memo.memo"))

@memo_bp.route("/edit/<int:memo_id>", methods=["GET", "POST"])
@login_required
def edit_memo(memo_id):
    memo_to_edit = Memo.query.get_or_404(memo_id)
    if request.method == "POST":
        new_content = request.form.get("content", "").strip()
        if new_content:
            memo_to_edit.content = new_content
            db.session.commit()
            return redirect(url_for("memo.memo"))
    return render_template("edit_memo.html", memo=memo_to_edit)
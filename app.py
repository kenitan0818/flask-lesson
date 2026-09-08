from flask import Flask, render_template, request
from flask_login import LoginManager
from models import db, User
from blueprints.memo_routes import memo_bp

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SECRET_KEY"] = "learning-secret-key-change-later"
db.init_app(app)
app.register_blueprint(memo_bp)

from blueprints.auth_routes import auth_bp
app.register_blueprint(auth_bp)

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def hello():
    return "Hello, Flask!"

@app.route("/about")
def about():
    return "このアプリはFlask学習用のサンプルです。"

@app.route("/user/<name>")
def user_page(name):
    return render_template("greeting.html", name=name, weekday="月曜日")

@app.route("/fruits")
def fruits():
    fruit_list = ["りんご", "みかん", "ぶどう"]
    return render_template("fruits.html", fruits=fruit_list, count=len(fruit_list))

@app.route("/name_form", methods=["GET", "POST"])
def name_form():
    submitted_name = None
    error = None
    from flask import request
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        if username == "":
            error = "名前を入力してください。"
        else:
            submitted_name = username
    return render_template("name_form.html", submitted_name=submitted_name, error=error)

if __name__ == "__main__":
    app.run(debug=True, port=8000)
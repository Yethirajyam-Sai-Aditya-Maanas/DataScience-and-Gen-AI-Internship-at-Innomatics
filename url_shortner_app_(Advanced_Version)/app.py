from flask import Flask, render_template, request, redirect, url_for
from models import db, User, URL
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import validators
import string
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template("home.html")

# ---------------- SIGNUP ----------------
@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if len(username) < 5 or len(username) > 9:
            return "Username must be between 5 to 9 characters long"

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "This username already exists..."

        hashed_password = generate_password_hash(password)

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("signup.html")

# ---------------- LOGIN ----------------
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("dashboard"))

        return "Invalid username or password"

    return render_template("login.html")

# ---------------- LOGOUT ----------------
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

# ---------------- DASHBOARD ----------------
@app.route('/dashboard', methods=["GET", "POST"])
@login_required
def dashboard():
    short_url = None
    error = None

    if request.method == "POST":
        original_url = request.form.get("url")

        if not validators.url(original_url):
            error = "Invalid URL"
        else:
            short_code = generate_short_code()

            new_url = URL(
                original_url=original_url,
                short_code=short_code,
                user_id=current_user.id
            )
            db.session.add(new_url)
            db.session.commit()

            short_url = request.host_url + short_code

    return render_template("dashboard.html", short_url=short_url, error=error)

# ---------------- REDIRECT ----------------
@app.route('/<short_code>')
def redirect_url(short_code):
    url = URL.query.filter_by(short_code=short_code).first()
    if url:
        return redirect(url.original_url)
    return "URL not found"

# ---------------- HISTORY ----------------
@app.route('/history')
@login_required
def history():
    urls = URL.query.filter_by(user_id=current_user.id).all()
    return render_template("history.html", urls=urls)

if __name__ == "__main__":
    app.run(debug=True)
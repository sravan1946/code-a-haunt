import re
from flask import Flask, render_template
from flask_login import LoginManager, login_required, current_user
from auth import auth, login_manager
import os


app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)
login_manager.init_app(app)

app.register_blueprint(auth)


@app.route('/')
def index():
    return render_template('index.html', current_user=current_user)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, port=8000, host="0.0.0.0")


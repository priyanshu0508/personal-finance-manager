from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
from flask_migrate import Migrate

db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

# ➤ You forgot this block earlier (required by Flask-Login)
@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.get(int(user_id))

def create_app():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    project_root = os.path.dirname(base_dir)

    app = Flask(
        __name__,
        template_folder=os.path.join(project_root, "templates"),
        static_folder=os.path.join(project_root, "static"),
    )

    app.config["SECRET_KEY"] = "your_secret_key_here"

    db_path = os.path.join(project_root, "instance", "finance.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    from .auth import auth_blueprint
    from .transactions import transaction_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(transaction_blueprint, url_prefix="/transaction")

    @app.template_filter("inr")
    def inr(amount):
        try:
            return "₹{:,.2f}".format(float(amount))
        except:
            return amount

    return app

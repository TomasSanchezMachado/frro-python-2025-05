from flask import Flask, render_template, redirect, url_for, session
from models import db, User
from auth import auth_bp

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
app.register_blueprint(auth_bp, url_prefix='/auth')


@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('home.html', username=session['username'])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin')
            admin.set_password('1234')
            db.session.add(admin)
            db.session.commit()
    app.run()


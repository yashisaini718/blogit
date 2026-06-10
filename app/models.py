from datetime import datetime, timezone
from flask import current_app, url_for
from itsdangerous import URLSafeTimedSerializer,BadSignature,SignatureExpired
from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User,int(user_id))

class User(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(20), unique=True, nullable=False)
    email=db.Column(db.String(120), unique=True, nullable=False)
    image_file=db.Column(db.String(225), nullable=False, default='default.jpg')
    password=db.Column(db.String(60), nullable=False)
    posts=db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self):
        s=URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id':self.id})
    
    @staticmethod
    def verify_reset_token(token,max_age=1800):
        s=URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            user_id=s.loads(token,max_age=max_age)['user_id']
        except (BadSignature,SignatureExpired):
            return None
        return db.session.get(User,user_id)
    
    @property
    def profile_image(self):
        if self.image_file.startswith("http"):
            return self.image_file
        return url_for("static",filename=f"profile_pics/{self.image_file}")
    

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file})"

class Post(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title=db.Column(db.String(100),nullable=False)
    date_posted=db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    #lambda:datetime.now(timezone.utc))
    content=db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}')"

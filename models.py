from database import db

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    memos = db.relationship('Memo', backref='author', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'
    
class Memo(db.Model):
    __tablename__ = 'memo'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
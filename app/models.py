from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    carbon_footprint = db.Column(db.Float, default=0.0)

    def __repr__(self):
        return f'<User {self.username}>'

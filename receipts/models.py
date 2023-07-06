from main import db
import secrets


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    reset_token = db.Column(db.String(100), nullable=True)

    def get_reset_token(self):
        token = secrets.token_hex(16)
        self.reset_token = token
        db.session.commit()
        return token

    @staticmethod
    def verify_reset_token(token):
        user = User.query.filter_by(reset_token=token).first()
        return user

    def __repr__(self):
        return '<Article %r>' % self.id


class Receipt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_of_receipt = db.Column(db.String(100), nullable=False)
    about_of_receipt = db.Column(db.Text, nullable=False)
    ingredients = db.Column(db.String(100), nullable=False)
    kilocalories = db.Column(db.Integer, nullable=False)
    author_of_receipt = db.Column(db.String(50), db.ForeignKey('user.username'))

    def __repr__(self):
        return '<Receipt %r>' % self.id


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rate = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    receipt_id = db.Column(db.Integer, db.ForeignKey('receipt.id'))
    rating_user_id = db.Column(db.String(50), db.ForeignKey('user.username'))

    def __repr__(self):
        return '<Rating %r>' % self.id

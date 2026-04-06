from extensions import db

# USER TABLE
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    role = db.Column(db.String(20))  # admin, analyst, viewer
    is_active = db.Column(db.Boolean, default=True)


# FINANCIAL RECORD TABLE
class FinancialRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    amount = db.Column(db.Float)
    type = db.Column(db.String(10))  # income / expense
    category = db.Column(db.String(50))
    date = db.Column(db.String(20))
    notes = db.Column(db.String(200))
from flask import Flask
from extensions import db
from flask import request, jsonify
from flask_jwt_extended import JWTManager, create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended import jwt_required, get_jwt
from functools import wraps
from flask_jwt_extended import get_jwt
from flask_jwt_extended import jwt_required, get_jwt_identity

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'supersecretkey'
db.init_app(app)
jwt = JWTManager(app)



import models

def role_required(allowed_roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            claims = get_jwt()
            if claims.get("role") not in allowed_roles:
                return {"error": "Access denied"}, 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper

@app.route('/')
def home():
    return {"message": "Backend running"}

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Check if data exists
    if not data:
        return {"error": "No input data provided"}, 400

    # Required fields
    required_fields = ['name', 'email', 'password']

    for field in required_fields:
        if field not in data or not data[field]:
            return {"error": f"{field} is required"}, 400

    # Check if user already exists
    existing_user = models.User.query.filter_by(email=data['email']).first()
    if existing_user:
        return {"error": "Email already exists"}, 409

    new_user = models.User(
        name=data['name'],
        email=data['email'],
        password=data['password'],
        role=data.get('role', 'viewer')
    )

    db.session.add(new_user)
    db.session.commit()

    return {"message": "User created successfully"}, 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    user = models.User.query.filter_by(email=data['email']).first()

    if not user or user.password != data['password']:
        return {"error": "Invalid credentials"}, 401

    # Check if user is active
    if not user.is_active:
        return {"error": "User is inactive. Contact admin"}, 403

    token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role}
    )

    return {"token": token}

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    claims = get_jwt()
    return {
        "message": "Access granted",
        "role": claims.get("role")
    }

@app.route('/admin', methods=['GET'])
@jwt_required()
def admin_only():
    claims = get_jwt()

    if claims.get("role") != "admin":
        return {"error": "Admins only"}, 403

    return {"message": "Welcome Admin"}

from datetime import datetime

@app.route('/add-record', methods=['POST'])
@jwt_required()
@role_required(['admin'])
def add_record():
    data = request.get_json()

    if not data:
        return {"error": "No input data"}, 400

    required_fields = ['amount', 'type', 'category', 'date']

    for field in required_fields:
        if field not in data or not data[field]:
            return {"error": f"{field} is required"}, 400

    # Validate amount
    try:
        amount = float(data['amount'])
    except:
        return {"error": "amount must be a number"}, 400

    # Validate type
    if data['type'] not in ['income', 'expense']:
        return {"error": "type must be 'income' or 'expense'"}, 400

    # Validate date format (YYYY-MM-DD)
    try:
        datetime.strptime(data['date'], "%Y-%m-%d")
    except:
        return {"error": "date must be in YYYY-MM-DD format"}, 400

    new_record = models.FinancialRecord(
        user_id=get_jwt_identity(),
        amount=amount,
        type=data['type'],
        category=data['category'],
        date=data['date'],
        notes=data.get('notes', '')
    )

    db.session.add(new_record)
    db.session.commit()

    return {"message": "Record added successfully"}, 201

@app.route('/records', methods=['GET'])
@jwt_required()
@role_required(['admin', 'analyst'])
def get_records():
    # Get filters from URL
    record_type = request.args.get('type')
    category = request.args.get('category')
    date = request.args.get('date')

    # Start base query
    query = models.FinancialRecord.query

    # Apply filters if present
    if record_type:
        query = query.filter_by(type=record_type)

    if category:
        query = query.filter_by(category=category)

    if date:
        query = query.filter_by(date=date)

    # Execute query
    records = query.all()

    # Convert to JSON
    result = []
    for r in records:
        result.append({
            "id": r.id,
            "amount": r.amount,
            "type": r.type,
            "category": r.category,
            "date": r.date,
            "notes": r.notes
        })

    return {"records": result}

@app.route('/dashboard', methods=['GET'])
@jwt_required()
@role_required(['viewer', 'analyst', 'admin'])
def dashboard():
    records = models.FinancialRecord.query.all()

    total_income = sum(r.amount for r in records if r.type == "income")
    total_expense = sum(r.amount for r in records if r.type == "expense")

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": total_income - total_expense
    }

from datetime import datetime

@app.route('/update-record/<int:id>', methods=['PUT'])
@jwt_required()
@role_required(['admin'])
def update_record(id):
    data = request.get_json()

    if not data:
        return {"error": "No input data provided"}, 400

    record = models.FinancialRecord.query.get(id)

    if not record:
        return {"error": "Record not found"}, 404

    # Validate and update amount
    if 'amount' in data:
        try:
            record.amount = float(data['amount'])
        except:
            return {"error": "Amount must be a number"}, 400

    # Validate and update type
    if 'type' in data:
        if data['type'] not in ['income', 'expense']:
            return {"error": "type must be 'income' or 'expense'"}, 400
        record.type = data['type']

    # Validate and update category
    if 'category' in data:
        if not data['category']:
            return {"error": "category cannot be empty"}, 400
        record.category = data['category']

    # Validate and update date
    if 'date' in data:
        try:
            datetime.strptime(data['date'], "%Y-%m-%d")
            record.date = data['date']
        except:
            return {"error": "date must be in YYYY-MM-DD format"}, 400

    # Update notes
    if 'notes' in data:
        record.notes = data['notes']

    db.session.commit()

    return {
        "message": "Record updated successfully",
        "updated_record": {
            "id": record.id,
            "amount": record.amount,
            "type": record.type,
            "category": record.category,
            "date": record.date,
            "notes": record.notes
        }
    }, 200

@app.route('/delete-record/<int:id>', methods=['DELETE'])
@jwt_required()
@role_required(['admin'])
def delete_record(id):
    record = models.FinancialRecord.query.get(id)

    if not record:
        return {"error": "Not found"}, 404

    db.session.delete(record)
    db.session.commit()

    return {"message": "Deleted"}

@app.route('/users', methods=['GET'])
@jwt_required()
@role_required(['admin'])
def get_users():
    users = models.User.query.all()

    result = []
    for u in users:
        result.append({
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "role": u.role,
            "is_active": u.is_active
        })

    return {"users": result}

@app.route('/toggle-user/<int:id>', methods=['PUT'])
@jwt_required()
@role_required(['admin'])
def toggle_user(id):
    user = models.User.query.get(id)

    if not user:
        return {"error": "User not found"}, 404

    # Toggle status
    user.is_active = not user.is_active

    db.session.commit()

    return {
        "message": "User status updated",
        "user": {
            "id": user.id,
            "is_active": user.is_active
        }
    }



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
from flask import Flask, jsonify, request, abort
from models.user import User, db
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or not data.get('name'):
        abort(400, description="Name is required")
    
    user = User(name=data['name'])
    db.session.add(user)
    db.session.commit()
    
    return jsonify(user.to_dict()), 201

@app.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_dict())

@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    
    return '', 204

@app.route('/user/<int:id>', methods=['PATCH'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()
    if data.get('name'):
        user.name = data['name']
    
    db.session.commit()
    return jsonify(user.to_dict())

if __name__ == '__main__':
    app.run(debug=True)

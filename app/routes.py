from flask import Blueprint, request, jsonify
from app.models import Item, db

bp = Blueprint('api', __name__)

@bp.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([{'id': i.id, 'name': i.name, 'description': i.description} for i in items])

@bp.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Invalid input'}), 400
    item = Item(name=data['name'], description=data.get('description'))
    db.session.add(item)
    db.session.commit()
    return jsonify({'message': 'Item created', 'id': item.id}), 201

@bp.route('/items/<int:item_id>', methods=['PATCH'])
def update_item(item_id):
    data = request.get_json()
    item = Item.query.get_or_404(item_id)
    if 'name' in data:
        item.name = data['name']
    if 'description' in data:
        item.description = data['description']
    db.session.commit()
    return jsonify({'message': 'Item updated'})

@bp.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item deleted'})

from flask import Flask, request, jsonify

app = Flask(__name__)

# Список для хранения объектов (вместо базы данных для простоты)
items = []
item_id = 1

# GET /items - Получить все элементы
@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items), 200

# POST /items - Создать новый элемент
@app.route('/items', methods=['POST'])
def create_item():
    global item_id
    data = request.get_json()
    if not data or 'name' not in data or 'description' not in data:
        return jsonify({'error': 'Invalid input, name and description are required'}), 400

    new_item = {
        'id': item_id,
        'name': data['name'],
        'description': data['description']
    }
    items.append(new_item)
    item_id += 1
    return jsonify(new_item), 201

# PATCH /items/<id> - Обновить элемент по ID
@app.route('/items/<int:id>', methods=['PATCH'])
def update_item(id):
    data = request.get_json()
    for item in items:
        if item['id'] == id:
            item['name'] = data.get('name', item['name'])
            item['description'] = data.get('description', item['description'])
            return jsonify(item), 200

    return jsonify({'error': 'Item not found'}), 404

# DELETE /items/<id> - Удалить элемент по ID
@app.route('/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    global items
    items = [item for item in items if item['id'] != id]
    return jsonify({'message': 'Item deleted'}), 200

# Запуск приложения Flask
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


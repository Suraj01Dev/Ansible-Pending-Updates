from flask import Flask, request, jsonify
import json
app = Flask(__name__)

data = {}

@app.route('/put_updates', methods=['PUT'])
def handle_put_request():
    request_data = request.get_json()

    if 'key' not in request_data or 'value' not in request_data:
        return jsonify({'error': 'Invalid data. Both "key" and "value" are required.'}), 400

    key = request_data['key']
    value = request_data['value']

    data[key] = value
    db=value.encode().decode().split("\n")
    print(db)
    db_json={f"Pending_Updates (Server: {db[0]})":db[1:]}
    json_data=json.dumps(db_json)

    with open(f"Pending_Updates (Server: {db[0]}).json", "w") as json_file:
        json_file.write(json_data)

    return jsonify({'message': f'Data with key "{key}" successfully updated.'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

    

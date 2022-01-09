from flask import Flask, jsonify, abort, make_response, request
from flask.wrappers import Request

from models import books

app = Flask(__name__)
app.config["SECRET_KEY"] = "ni"

@app.route("/api/v1/lib/", methods=["GET"])
def lib_list_api_v1():
    return jsonify(books.all())

@app.route("/api/v1/lib/", methods=["POST"])
def add_book():
    if not request.json or not 'title' in request.json:
        abort(400)
    book = {
        'id': books.all()[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    books.create(book)
    return jsonify({'book': book})

@app.route("/api/v1/lib/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = books.get(book_id)
    if not book:
        abort(404)
    return jsonify({'book': book})

@app.route("/api/v1/lib/<int:book_id>", methods=["PUT"])
def book_update(book_id):
    book = books.get(book_id)
    if not book:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'title' in data and not isinstance(data.get('title'), str),
        'description' in data and not isinstance(data.get('description'), str),
        'done' in data and not isinstance(data.get('done'), bool)
    ]):
        abort(400)
    book = {
        'title': data.get('title', book['title']),
        'description': data.get('description', book['description']),
        'done': data.get('done', book['done'])
    }
    books.update(book_id, book)
    return jsonify({'book': book})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, request, jsonify
from db import get, create


app = Flask(__name__)

@app.route('/books/', methods=['GET'])
def get_books():
	return get()


@app.route("/add_literature", methods=["POST"])
def add_literature():
	if not request.is_json:
		return jsonify({"msg":"missing json request"}), 400
	create(request.get_json())
	return "Book added"

if __name__ == '__main__':
	app.run(debug=True)




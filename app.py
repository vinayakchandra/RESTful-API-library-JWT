from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from mysql_connect import ConnectSql

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'secret'

jwt = JWTManager(app)
sql = ConnectSql()

users = {
    "admin": {"password": "admin"}
}


# Login route to authenticate and return a JWT token
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username", None)
    password = data.get("password", None)

    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400

    user = users.get(username, None) # {'password': 'admin'}
    if not user or user["password"] != password:
        return jsonify({"msg": "Bad username or password"}), 401

    # Create a new token with the user identity
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200


# Read
@app.route("/")
@jwt_required()
def get_all_books():
    return sql.getAllBooks()


@app.route("/<id>", methods=["GET"])
@jwt_required()  
def get_book(id):
    book = sql.getBook(id)
    return jsonify(book)


# create
@app.route("/new", methods=["POST"])
@jwt_required()  
def insert_book():
    data = request.get_json()
    bookID = data["bookID"]
    bookName = data["bookName"]
    author = data["author"]
    book = sql.insertBook(bookID, bookName, author)
    return jsonify(book)


# delete
@app.route("/delete/<id>", methods=["DELETE"])
@jwt_required()  
def delete_book(id):
    book = sql.deleteBook(id)
    return jsonify(book)


# update
@app.route("/update/<id>", methods=["PATCH"])
@jwt_required()  
def update_book(id):
    data = request.get_json()
    bookName = data["bookName"]
    book = sql.updateBook(id, bookName)
    return jsonify(book)


if __name__ == "__main__":
    app.run()

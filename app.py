from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://harzbooks:123@localhost/harry_potter_db'
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    volume = db.Column(db.Integer, nullable=False)

# Explicitly create application context
with app.app_context():
    # Check if data already exists
    if not Book.query.first():
        # Sample data
        sample_books = [
            {"title": "Harry Potter and the Sorcerer's Stone", "author": "J.K. Rowling", "volume": 1},
            {"title": "Harry Potter and the Chamber of Secrets", "author": "J.K. Rowling", "volume": 2},
            {"title": "Harry Potter and the Prisoner of Azkaban", "author": "J.K. Rowling", "volume": 3},
        ]

        # Create table and insert sample data
        db.create_all()

        for book_data in sample_books:
            book = Book(**book_data)
            db.session.add(book)

        db.session.commit()

# Route to get all books
@app.route('/books', methods=['GET'])
def get_books():
        books = Book.query.all()
        book_list = [
            {"id": book.id, "title": book.title, "author": book.author, "volume": book.volume}
            for book in books
        ]
        return jsonify(book_list)

# Route to add a new book
@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()

    # Convert 'volume' to an integer
    try:
        volume_as_int = int(data['volume'])
    except ValueError:
        return jsonify({"error": "Invalid value for 'volume'. Must be an integer."}), 400

    new_book = Book(title=data['title'], author=data['author'], volume=volume_as_int)
    db.session.add(new_book)
    db.session.commit()

    return jsonify({"message": "Book added successfully", "book": {"id": new_book.id, "title": new_book.title, "author": new_book.author, "volume": new_book.volume}})

@app.route('/books', methods=['DELETE'])
def delete_all_books():
    Book.query.delete()
    db.session.commit()
    return jsonify({"message": "All books deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)


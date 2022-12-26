# Imports

import json
import os
from flask import Flask, request, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


CORS(app)

# create SQLITE3 DataBase

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

# Books table


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    b_name = db.Column(db.String(100))
    author = db.Column(db.String(100))
    year = db.Column(db.Integer)
    loanType = db.Column(db.Integer)
    loans = db.relationship('Loans', backref='Books')

    def __init__(self, b_name, author, year, loanType):
        self.b_name = b_name
        self.author = author
        self.year = year
        self.loanType = loanType

# Customers table


class Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cus_name = db.Column(db.String(100))
    city = db.Column(db.String(100))
    age = db.Column(db.Integer)
    loans = db.relationship('Loans', backref='Customers')

    def __init__(self, cus_name, city, age):
        self.cus_name = cus_name
        self.city = city
        self.age = age

# Loans table


class Loans(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    custumerID = db.Column(db.Integer, db.ForeignKey('customers.id'))
    bookID = db.Column(db.Integer, db.ForeignKey('books.id'))
    loanDate = db.Column(db.Integer)
    returnDate = db.Column(db.Integer)

    def __init__(self, custumerID, bookID, loanDate, returnDate):
        self.custumerID = custumerID
        self.bookID = bookID
        self.loanDate = loanDate
        self.returnDate = returnDate


# Books methods

@app.route('/books/', methods=['GET', 'POST'])
@app.route('/books/<id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def books(id=id):
    if request.method == 'GET':
        books = []
        for book in Books.query.all():
            books.append({"id": book.id, "b_name": book.b_name, "author": book.author,
                         "year": book.year, "loanType": book.loanType})
        return (json.dumps(books))

    if request.method == 'POST':
        show_book = request.get_json()
        b_name = show_book['b_name']
        author = show_book['author']
        year = show_book['year']
        loanType = show_book['loanType']
        new_book = Books(b_name, author, year, loanType)
        db.session.add(new_book)
        db.session.commit()
        return {'text': 'Book added'}

    if request.method == 'PUT':
        upd_book = Books.query.get(id)
        b_name = request.json['b_name']
        author = request.json['author']
        year = request.json['year']
        loanType = request.json['loanType']
        upd_book.b_name = b_name
        upd_book.author = author
        upd_book.year = year
        upd_book.loanType = loanType
        db.session.commit()
        return {'text': 'Book updated'}

    if request.method == 'DELETE':
        del_book = Books.query.get(id)
        db.session.delete(del_book)
        db.session.commit()
        return {'text': 'Book deleted'}

# Customers methods


@app.route('/customers/', methods=['GET', 'POST'])
@app.route('/customers/<id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def customers(id=id):
    if request.method == 'GET':
        customers = []
        for customer in Customers.query.all():
            customers.append({"id": customer.id, "cus_name": customer.cus_name,
                             "city": customer.city, "age": customer.age})
        return (json.dumps(customers))

    if request.method == 'POST':
        show_customer = request.get_json()
        cus_name = show_customer['cus_name']
        city = show_customer['city']
        age = show_customer['age']
        new_customer = Customers(cus_name, city, age, )
        db.session.add(new_customer)
        db.session.commit()
        return {'text': 'Customer added'}

    if request.method == 'PUT':
        upd_customer = Customers.query.get(id)
        cus_name = request.json['cus_name']
        city = request.json['city']
        age = request.json['age']
        upd_customer.cus_name = cus_name
        upd_customer.city = city
        upd_customer.age = age
        db.session.commit()
        return {'text': 'Customer updated'}

    if request.method == 'DELETE':
        del_customer = Customers.query.get(id)
        db.session.delete(del_customer)
        db.session.commit()
        return {'text': 'Customer deleted'}

# Loans methods

@app.route('/loans/', methods=['GET', 'POST'])
@app.route('/loans/<id>', methods=['PATCH'])
def loan(id=id):

    if request.method == 'GET':
        loans = []
        for loan, book in db.session.query(Loans, Books).join(Books).all():
            loans.append({"id": loan.id, "custumerID": loan.custumerID, "bookID": loan.bookID,
                         "loanDate": loan.loanDate, "returnDate": loan.returnDate, "loanType": book.loanType})
        return (json.dumps(loans))

    elif request.method == 'POST':
        show_loan = request.get_json()
        custumerID = show_loan['custumerID']
        bookID = show_loan['bookID']
        loanDate = show_loan['loanDate']
        returnDate = show_loan['returnDate']
        new_loan = Loans(custumerID, bookID, loanDate, returnDate)
        db.session.add(new_loan)
        db.session.commit()
        return "Book Loaned Successfully"

    elif request.method == "PATCH":
        upd_Loan = Loans.query.filter_by(id=id).first()
        tmpLoan = request.get_json()
        upd_Loan.returnDate = tmpLoan["returnDate"]
        db.session.commit()
        return "Book successfully returned"

    # if request.method == 'GET':
    #     loans = []
    #     for loan, book in db.session.query(Loans, Books).join(Books).all():
    #         loans.append({"id": loan.id, "custumerID": loan.custumerID, "bookID": loan.bookID,
    #                      "loanDate": loan.loanDate, "returnDate": loan.returnDate, "loanType": book.loanType})
    #     return (json.dumps(loans))

    # if request.method == 'POST':
    #     show_loan = request.get_json()
    #     custumerID = show_loan['custumerID']
    #     bookID = show_loan['bookID']
    #     loanDate = show_loan['loanDate']
    #     returnDate = show_loan['returnDate']
    #     new_loan = Loans(custumerID, bookID, loanDate, returnDate)
    #     db.session.add(new_loan)
    #     db.session.commit()
    #     return {'text': 'Loan added'}

    # if request.method == 'PUT':
    #     upd_loan = Loans.query.get(id)
    #     custumerID = request.json['custumerID']
    #     bookID = request.json['bookID']
    #     loanDate = request.json['loanDate']
    #     returnDate = request.json['returnDate']
    #     upd_loan.custumerID = custumerID
    #     upd_loan.bookID = bookID
    #     upd_loan.loanDate = loanDate
    #     upd_loan.returnDate = returnDate
    #     db.session.commit()
    #     return {'text': 'Loan updated'}

# there is no "delete" method for loans


@app.route('/')
def home():
    return 'Website is running!'


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

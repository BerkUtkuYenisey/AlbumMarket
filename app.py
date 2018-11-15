from flask import Flask, render_template, request, make_response
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'MainDatabase.db')
db = SQLAlchemy(app)


class Customer(db.Model):
    username = db.Column(db.String, primary_key=True)
    gsm = db.Column(db.Integer)
    email = db.Column(db.String)
    address = db.Column(db.String)
    password = db.Column(db.String)

    def __init__(self, username, gsm, email, address, password):
        self.username = username
        self.gsm = gsm
        self.email = email
        self.address = address
        self.password = password

class Album(db.Model):
    artist = db.Column(db.String(30))
    album_name = db.Column(db.String(30), primary_key=True)
    year = db.Column(db.String(4))
    cost = db.Column(db.Float)
    genre = db.Column(db.String(4))
    rating_avg = db.Column(db.String(4))
    producer_name = db.Column(db.String(4), db.ForeignKey('producer.producer_name'))

    def __init__(self, artist, album_name, year, cost, genre, producer_name):
        self.artist = artist
        self.album_name = album_name
        self.year = year
        self.cost = cost
        self.genre = genre
        self.producer_name = producer_name


class Producer(db.Model):
    producer_name = db.Column(db.String(30), primary_key=True)

    def __init__(self, producer_name):
        self.producer_name = producer_name


class Buy(db.Model):
    buy_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, db.ForeignKey('customer.username'))
    album_name = db.Column(db.String(30), db.ForeignKey('album.album_name'))

    def __init__(self, username, album_name):
        self.username = username
        self.album_name = album_name


class Rate(db.Model):
    rate_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, db.ForeignKey('customer.username'))
    album_name = db.Column(db.String(30), db.ForeignKey('album.album_name'))
    comment = db.Column(db.String)
    rate = db.Column(db.Integer)

    def __init__(self, username, album_name, comment, rate):
        self.username = username
        self.album_name = album_name
        self.comment = comment
        self.rate = rate


@app.route("/")
def get_homePage():
    return render_template("mainpage.html")


@app.route("/login", methods=["GET"])
def get_login():
    return render_template("login.html")


@app.route("/register", methods=["GET"])
def get_register():
    return render_template("register.html")


@app.route("/users/signup", methods=["POST"])
def post_register():
    data = request.json
    username = data['username']
    gsm = data['gsm']
    email = data['email']
    address = data['address']
    password = data['password']

    if not username or not email or not address or not password:
        return make_response('Missing atribute', 401)

    new_customer = Customer(username, gsm, email, address, password)

    db.session.add(new_customer)
    db.session.commit()

    return render_template("login.html")


if __name__ == '__main__':
    app.run(debug=True)


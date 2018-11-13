from flask import Flask, render_template

app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)


@app.route("/")
@app.route("/home")
def home():
    return render_template("mainpage.html")

@app.route("/about")
def about():
    return "<h1>About Page</h1>"


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/register")
def register():
     return render_template("register.html")
from flask import Flask, render_template
from markupsafe import Markup

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('map.html')
    

@app.route("/hello")
def hello():
    return "<h1 style='color:yellow'>Hello There!</h1>"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
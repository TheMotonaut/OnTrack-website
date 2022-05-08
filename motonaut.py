from crypt import methods
from distutils.log import debug
from email import message
from enum import unique
from http import client
from flask import Blueprint, Flask, redirect, render_template, url_for, request, send_from_directory, flash
from flask_sqlalchemy import SQLAlchemy
import flask_login
from flask_login import current_user
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap5
import uuid
from pymysql import NULL
from sqlalchemy import null

from werkzeug.middleware.proxy_fix import ProxyFix


from werkzeug.security import generate_password_hash, gen_salt, check_password_hash

from markupsafe import Markup
import json
import traceback
import os

import random

app = Flask(__name__)

app.config['SECRET_KEY'] = 'MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAOUHFiCkhnOJG2N3CEX7bBKqs2BOjy50OyBRSAMR26+96Wm01WQ6wyHqqk5Uz5jxZNm2Un/ri/cZXpiO/wXD9WkCAwEAAQ'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://OnTrack:ILoveMotorcycles@localhost/OnTrack'

db = SQLAlchemy(app)

login_manager = flask_login.LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

app.config['MQTT_BROKER_URL'] = 'motonaut.se'  # use the free broker from HIVEMQ
app.config['MQTT_BROKER_PORT'] = 1883  # default port for non-tls connection
app.config['MQTT_USERNAME'] = 'OnTrack'  # set the username here if you need authentication for the broker
app.config['MQTT_PASSWORD'] = 'fgh12qwe'  # set the password here if the broker demands authentication
app.config['MQTT_KEEPALIVE'] = 5  # set the time interval for sending a ping to the broker to 5 seconds
app.config['MQTT_TLS_ENABLED'] = False  # set TLS to disabled for testing purposes
app.config['MQTT_CLEAN_SESSION'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Parameters for SSL enabled
# app.config['MQTT_BROKER_PORT'] = 8883
# app.config['MQTT_TLS_ENABLED'] = True
# app.config['MQTT_TLS_INSECURE'] = True
# app.config['MQTT_TLS_CA_CERTS'] = 'ca.crt

bootstrap = Bootstrap5(app)
socketio = SocketIO(app)

app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)

mqtt = Mqtt(app)

map_clients = {}

class Users(flask_login.UserMixin, db.Model):
    __tablename = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), unique = True)
    password = db.Column(db.String(256))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __rep__(self):
        return '<User %r>' % self.username

class Motorcycles(db.Model):
    __tablename = 'motorcycles'
    id = db.Column(db.Integer, primary_key = True)
    model = db.Column(db.String(255))
    brand = db.Column(db.String(255))

    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    UID = db.Column(db.String(255))
    owner = db.Column(db.String(255))


    def __init__(self, brand, model, owner):
        self.owner = owner
        self.brand = brand
        self.model = model

        self.longitude = random.uniform(0.0, 80.0)
        self.latitude = random. uniform(0.0, 12.0)

        uid = uuid.uuid4()
        self.UID = uid.hex

    def __rep__(self):
        return '<Name %r>' % self.name

class Devices(db.Model):
    __tablename = 'devices'
    id = db.Column(db.Integer, primary_key = True)
    productname = db.Column(db.String(255))
    sw_vers = db.Column(db.String(255))
    hw_vers = db.Column(db.String(255))
    UID = db.Column(db.String(255))
    owner = db.Column(db.String(255))
    mc_uid = db.Column(db.String(255))

    def __init__(self, sw_vers, hw_vers, productname):
        self.sw_vers = sw_vers
        self.hw_vers = hw_vers
        self.productname = productname
        uid = uuid.uuid4()
        self.UID = uid.hex
        self.owner = ''
        self.mc_uid = ''

    def __repr__(self):
        return '<Product %r' % self.productname

def update_map():
    print(map_clients)

    if map_clients:
        for map_client in map_clients:
            map_client.emit()


@socketio.on('connect')
def socket_connect(self):
    print('Socket connected!')

    if not current_user.is_authenticated:
        return

    username = current_user.username
    motorcycles = Motorcycles.query.filter_by(owner = username)

    for motorcycle in motorcycles:
        data = {}
        data['longitude'] = motorcycle.longitude
        data['latitude'] = motorcycle.latitude
        data['model'] = motorcycle.model

        json_data = json.dumps(data)

        socketio.emit('location', json_data, to=request.sid)

@socketio.on('disconnect')
def socket_disconnected():
    print('Socket disconnected')

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('/motorcycle/location')
    print('Connected!')

@mqtt.on_message()
def on_message(client, userdata, message):
    if message.topic == '/motorcycles/location':
        payload = message.payload.decode()

        seperated = payload.json

        UID = seperated[0]
        latitude = seperated[1]
        longitude = seperated[2]

        motorcycle = Motorcycles.query.filter_by(UID = UID).first()

        print(payload)

        if(motorcycle):
            motorcycle.longitude = longitude
            motorcycle.latitude = latitude

            user = motorcycle.owner

            db.session.add(motorcycle)
            db.session.commit()


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route('/profile', methods = ['GET', 'POST'])
@flask_login.login_required
def profile():
    username = current_user.username
    data = Motorcycles.query.filter_by(owner=username).all()
    print(data)

    return render_template('profile.html', message=current_user.username, motorcycles=data)

@app.route('/profile/motorcycles', methods = ['GET', 'POST'])
@flask_login.login_required
def motorcycle_list():
    if request.method == 'POST':
        model = request.form.get('model')
        brand = request.form.get('brand')

        username = current_user.username

        print(username)

        newMotorcycle = Motorcycles(brand = brand, model = model, owner = username)
        db.session.add(newMotorcycle)
        db.session.commit()

    username = current_user.username

    print(username)
    motorcycles = Motorcycles.query.filter_by(owner=username).all()

    return render_template('motorcycle_list.html', motorcycle_list = motorcycles)

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html', message='Enter your credentials')

    username = request.form.get('username')
    password = request.form.get('password')

    user = Users.query.filter_by(username=username).first()
    print(user)
    if user:
        return render_template('register.html', message='Username is already taken')

    newUser = Users(username, generate_password_hash(password, method='pbkdf2:sha256', salt_length=16))
    db.session.add(newUser)
    db.session.commit()

    print('hej')

    flask_login.login_user(newUser)

    return redirect(url_for('profile'))

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', message='Enter your credentials')

    username = request.form.get('username')
    password = request.form.get('password')

    user = Users.query.filter_by(username=username).first()
    print(user)
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again')
        return render_template('login.html', message = 'Username or password was entered incorrectly')

    flask_login.login_user(user)

    return redirect(url_for('profile'))

@app.route('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect('/')

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/map')
@flask_login.login_required
def map():
    return render_template('map.html')

@app.route("/locations", methods=['POST', 'GET'])
@flask_login.login_required
def requestLocation():
    return 'Locations'
    
@app.route("/hello")
def hello():
    return "<h1 style='color:yellow'>Hello There!</h1>" 

@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.errorhandler(Exception)
def handle_500(e=None):
    app.logger.error(traceback.format_exc())
    return 'Internal server error occured bajs', 500

#if __name__ == "__main__":
#    import threading, time
#    #app.run(debug=True)
#    threading.start_new_thread(lambda: socketio.run(app), ())
#
#    while True:
#        print('Hej')
#        time.sleep(1)
#        update_map()
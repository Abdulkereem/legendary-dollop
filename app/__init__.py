
from flask import Flask
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "secret key"
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=10)
app.static_folder = 'static'

#COOKIE_TIME_OUT = 60*60*24*7 #7 days
COOKIE_TIME_OUT = 60*5 #5 minutes

from .views import *

import os
from flask import Flask
from flask_pymongo import PyMongo
from flask_bootstrap import Bootstrap5
from apscheduler.schedulers.background import BackgroundScheduler
from flaskr.taskjob import task_job
import time
import RPi.GPIO as GPIO



# declaration global de mongo pour pouvoir l'utiliser dans les autres fichiers
mongo = PyMongo()
gpio = GPIO
gpio.setmode(GPIO.BCM)
#TODO: Changer lorsque le repos redevient privé
secretKey = 'sZxfx,fUHu+9fTOm~cRQh{?}b%~T8t'
delayAnalyse = 0

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='sZxfx,fUHu+9fTOm~cRQh{?}b%~T8t',
    )
    app.config["MONGO_URI"] = "mongodb://localhost:29020/APdatabase"
    mongo.init_app(app)
    bootstrap = Bootstrap5(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import accueil
    app.register_blueprint(accueil.bp)

    from . import historiqueAnalyse
    app.register_blueprint(historiqueAnalyse.bp)

    from . import testAnalyse
    app.register_blueprint(testAnalyse.bp)
    
    from . import stream
    app.register_blueprint(stream.bp)


    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app





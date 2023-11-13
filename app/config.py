import os
import datetime
from datetime import timedelta

UPLOAD_FOLDER = os.path.abspath("./uploads/")
DB_URI = "TBD"

class Config(object):
    DEBUG = True
    SECRET_KEY = '?\xbf,\xb4\x8d\xa3"<\x9c\xb0@\x0f5\xab,w\xee\x8d$0\x13\x8b83'
    # OJO: PARA CUANDO TRABAJE EN MEMORIA   SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:" 
    #SQLALCHEMY_DATABASE_URI = "sqlite:///musicalbox.sqlite3"
    #SQLALCHEMY_DATABASE_URI = "sqlite:///touchcenter.sqlite3"
    #SQLALCHEMY_ECHO=True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = UPLOAD_FOLDER
    TOKEN_EXPIRES = datetime.timedelta(seconds=180)


    

class ProductionConfig(Config):
    
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="miguellperezz",
    password="adminTouchcenter",
    hostname="miguellperezz.mysql.pythonanywhere-services.com",
    databasename="miguellperezz$touchcenter",
)
    SQLALCHEMY_POOL_RECYCLE = 299
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    FLASK_DEBUG = True


class DevelopmentConfigSQLITE(Config):
    FLASK_DEBUG = True
    FLASK_ENV='development'
    DEBUG=True
    SECRET_KEY = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
    SQLALCHEMY_DATABASE_URI = "sqlite:///touchcenter.sqlite3"


class DevelopmentConfigMYSQL(Config):
    FLASK_DEBUG = True
    FLASK_ENV='development'
    DEBUG=True
    SECRET_KEY = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="touchapp",
    password="touchapp",
    hostname="127.0.0.1:3306",
    databasename="touchapp",
)
    SQLALCHEMY_POOL_RECYCLE = 299
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    FLASK_DEBUG = True


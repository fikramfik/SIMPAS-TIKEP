from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import pymysql
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app=Flask('__name__', template_folder='simpas/templates', static_folder='simpas/static')
app.config['SECRET_KEY']="infopasar"

# dbuser="root"
# dbpass=""
# dbhost="localhost"
# dbname="simpas"
# conn="mysql+pymysql://{0}:{1}@{2}/{3}".format(dbuser,dbpass,dbhost,dbname)

# app.config['SQLALCHEMY_DATABASE_URI']=conn
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///simpas.db'

db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

from simpas.admin.routes import radmin
app.register_blueprint(radmin)

from simpas.user.routes import ruser
app.register_blueprint(ruser)
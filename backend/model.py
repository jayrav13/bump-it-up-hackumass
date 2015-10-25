# Imports
# flask
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

# sqlalchemy
from sqlalchemy import Integer, ForeignKey, String, Column, Float
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy

# other
import time
import hashlib

# set up app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///points.db" 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# set up database
db = SQLAlchemy(app)

# set up migration
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('data', MigrateCommand)

class Data(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	acc_x = db.Column(db.Float)
	acc_y = db.Column(db.Float)
	acc_z = db.Column(db.Float)
	lat = db.Column(db.Float)
	lng = db.Column(db.Float)
	time = db.Column(db.String)
	bump = db.Column(db.Float)

	def __init__(self, acc_x, acc_y, acc_z, lat, lng, time):
		self.acc_x = acc_x
		self.acc_y = acc_y
		self.acc_z = acc_z
		self.lat = lat
		self.lng = lng
		self.time = time
		self.bump = 0

if __name__ == "__main__":
	manager.run()

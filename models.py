import os
from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
from flask_migrate import Migrate

database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
  database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
    migrate = Migrate(app, db)


'''
Field Technician
'''
class fieldTech(db.Model):  
  __tablename__ = 'Technicians'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  employeeID = db.Column(db.Integer, nullable=False)
  lead = db.relationship('leadTech', backref='fieldtech', lazy='joined', cascade='all, delete')


  def __init__(self, name, employeeID):
    self.name = name
    self.employeeID = employeeID

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'employeeID': self.employeeID}

  def insert(self):
      db.session.add(self)
      db.session.commit()

  def delete(self):
      db.session.delete(self)
      db.session.commit()

  def update(self):
      db.session.commit()

class leadTech(db.Model):  
  __tablename__ = 'Leads'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  employeeID = db.Column(db.Integer, nullable=False)
  fieldtech_ids = db.Column(db.Integer, db.ForeignKey(fieldTech.id), nullable=False)
  senior = db.relationship('seniorTech', backref='leadtech', lazy='joined', cascade='all, delete')


  def __init__(self, name, employeeID, fieldtech_ids):
    self.name = name
    self.employeeID = employeeID
    self.fieldtech_ids = fieldtech_ids

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'employeeID': self.employeeID,
      'fieldtech_ids': self.fieldtech_ids}

  def insert(self):
      db.session.add(self)
      db.session.commit()

  def delete(self):
      db.session.delete(self)
      db.session.commit()

  def update(self):
      db.session.commit()

class seniorTech(db.Model):  
  __tablename__ = 'Seniors'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  employeeID = db.Column(db.Integer, nullable=False)
  fieldtech_ids = db.Column(db.Integer, db.ForeignKey(fieldTech.id), nullable=False)
  leadtech_ids = db.Column(db.Integer, db.ForeignKey(leadTech.id), nullable=False)


  def __init__(self, name, employeeID, fieldtech_ids, leadtech_ids):
    self.name = name
    self.employeeID = employeeID
    self.fieldtech_ids = fieldtech_ids
    self.leadtech_ids = leadtech_ids

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'employeeID': self.employeeID,
      'fieldtech_ids': self.fieldtech_ids,
      'leadtech_ids': self.leadtech_ids}

  def insert(self):
      db.session.add(self)
      db.session.commit()

  def delete(self):
      db.session.delete(self)
      db.session.commit()

  def update(self):
      db.session.commit()
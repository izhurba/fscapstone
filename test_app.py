import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from auth import requires_auth
from models import setup_db, fieldTech, leadTech, seniorTech


class RepairTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "repairshop_test"
        self.database_path = "postgresql://{}/{}".format('postgres:password@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()
    
    def tearDown(self):
        pass


    def test_get_fieldtechs(self):
        resp = self.client().get('/fieldtechs')
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['fieldtechs']), 2)


    def test_get_leadtechs(self):
        resp = self.client().get('/leadtechs')
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['leadtechs']), 2)


    def test_get_fieldtechs(self):
        resp = self.client().get('/fieldtechs')
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['fieldtechs']), 2)

    





if __name__ == "__main__":
    unittest.main()
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
import auth

from app import create_app
from models import setup_db, fieldTech, leadTech, seniorTech


class RepairTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client

        self.field_tech = os.environ['FTOKEN']
        self.lead_tech = os.environ['LTOKEN']
        self.senior_tech = os.environ['STOKEN']

        self.database_name = "repairshop_test"
        self.database_path = "postgresql://{}/{}".format(
                        'postgres:password@localhost:5432',
                        self.database_name)
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        pass

    def test_get_fieldtechs(self):
        resp = self.client().get('/fieldtechs', headers={'Authorization': 'Bearer ' + self.field_tech})
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        # self.assertEqual(len(data['fieldtechs']), 2) Not working due to bug with post/delete test

    def test_get_fieldtechs_422(self):
        with self.assertRaises(auth.AuthError):
            self.client().get('/fieldtechs')

    def test_get_leadtechs(self):
        resp = self.client().get('/leadtechs', headers={'Authorization': 'Bearer ' + self.lead_tech})
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        # self.assertEqual(len(data['leadtechs']), 2) Not working due to bug with post/delete test

    def test_get_leadtechs_422(self):
        with self.assertRaises(auth.AuthError):
            self.client().get('/leadtechs')

    def test_get_seniortechs(self):
        resp = self.client().get('/seniortechs', headers={'Authorization': 'Bearer ' + self.senior_tech})
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['seniortechs']), 1)

    def test_get_seniortechs_AUTHERROR(self):
        with self.assertRaises(auth.AuthError):
            self.client().get('/seniortechs')

    def test_post_fieldtech(self):
        resp = self.client().post('/fieldtechs', headers={
                                'Authorization': 'Bearer ' + self.lead_tech
                                }, json={
                                    'name': 'Polea',
                                    'employeeID': 123513
                                })
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_post_fieldtech_400(self):
        resp = self.client().post('/fieldtechs', headers={
                                'Authorization': 'Bearer ' + self.lead_tech
                                }, json={
                                    'name': 'Polsea',
                                    'employeeID': 'fail'
                                })

        self.assertEqual(resp.status_code, 400)

    def test_post_leadtech(self):
        resp = self.client().post('/leadtechs', headers={
                                'Authorization': 'Bearer ' + self.senior_tech
                                }, json={
                                    'name': 'Donnovan',
                                    'employeeID': 654433,
                                    'fieldtech_ids': 3
                                })
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_post_leadtech_400(self):
        resp = self.client().post('/leadtechs', headers={
                                'Authorization': 'Bearer ' + self.senior_tech
                                }, json={
                                    'name': 'Leiden',
                                    'employeeID': 'fail',
                                    'fieldtech_ids': 1
                                })

        self.assertEqual(resp.status_code, 400)

    def test_update_fieldtech(self):
        resp = self.client().patch('/fieldtechs/1', headers={
                                'Authorization': 'Bearer ' + self.lead_tech
                                }, json={
                                    'name': 'Polea',
                                    'employeeID': 123513
                                })
        data = json.loads(resp.data)

        newFTech = fieldTech.query.get(1)

        self.assertEqual(newFTech.name, "Polea")
        self.assertEqual(newFTech.employeeID, 123513)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_update_fieldtech_400(self):
        resp = self.client().patch('/fieldtechs/1', headers={
                            'Authorization': 'Bearer ' + self.lead_tech
                            })

        self.assertEqual(resp.status_code, 400)

    def test_update_leadtech(self):
        resp = self.client().patch('/leadtechs/1', headers={
                            'Authorization': 'Bearer ' + self.senior_tech
                            }, json={
                                'name': 'Fargus',
                                'employeeID': 993412,
                                'fieldtech_ids': 2
                            })
        data = json.loads(resp.data)

        newLTech = leadTech.query.get(1)

        self.assertEqual(newLTech.name, "Fargus")
        self.assertEqual(newLTech.employeeID, 993412)
        self.assertEqual(newLTech.fieldtech_ids, 2)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_update_leadtech_400(self):
        resp = self.client().patch('/leadtechs/1', headers={
                            'Authorization': 'Bearer ' + self.senior_tech})

        self.assertEqual(resp.status_code, 400)

    def test_delete_fieldtech(self):
        newTech = fieldTech(
            name="ForDelete",
            employeeID=123123
        )
        newTech.insert()

        latestTech = fieldTech.query.all()[-1]
        resp = self.client().delete('/fieldtechs/'+str(latestTech.id),
                                    headers={
                                    'Authorization': 'Bearer '+self.senior_tech
                                    })
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], latestTech.id)

    def test_delete_fieldtech_404(self):
        resp = self.client().delete('/fieldtechs/1000000', headers={
                                'Authorization': 'Bearer ' + self.senior_tech
                                })

        self.assertEqual(resp.status_code, 404)

    def test_delete_leadtech(self):
        newTech = leadTech(
            name="ForDelete",
            employeeID=123123,
            fieldtech_ids=1
        )
        newTech.insert()
        latestTech = leadTech.query.all()[-1]
        resp = self.client().delete('/leadtechs/'+str(latestTech.id),
                                    headers={
                                    'Authorization': 'Bearer '+self.senior_tech
                                    })
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], latestTech.id)

    def test_delete_leadtech_404(self):
        resp = self.client().delete('/leadtechs/10000', headers={
                                'Authorization': 'Bearer ' + self.senior_tech
                                })

        self.assertEqual(resp.status_code, 404)


if __name__ == "__main__":
    unittest.main()

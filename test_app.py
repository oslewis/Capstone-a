
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
import app
import models as models
from app import create_app
from models import Cashflow, Debt, setup_db

class CapstoneTestCase(unittest.TestCase):
    """This class represents the capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_cashflow = {
            "id": 1,
            "name": "SEC Filing",
            "amount": 542,
            "category": "Administration"
        }

        self.new_debt = {
            "id": 1,
            "name": "W8BEN FORM",
            "amount": 910,
            "category": "Administration"
        }

        self.balancesheet = {
            "total_debt": 60012,
            "total_cashflow": 1000512,
        }


        self.auth_specialist = {
            'Authorization':
            'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJUQXlRa1F5TVRKR1JETTBSa0ZGT0RnNFF6QTFRVVpDTVVJMVFqUkVNMFV6TURFNE9UUTNSZyJ9.eyJpc3MiOiJodHRwczovL2Zyb3N0eS1maXJlZmx5LTQ3NDMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlN2UyNTMwMTkwMWY1MGNjODgzZGRlNyIsImF1ZCI6ImFwaSIsImlhdCI6MTU4NTQ1NDA3NiwiZXhwIjoxNTg1NDYxMjc2LCJhenAiOiJYNnc0bExBcEtYblBWbXl0bzNIbTRVT0UzUkZqMmk4dyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsicG9zdDpjYXNoZmxvdyIsInBvc3Q6ZGVidCIsInJlYWQ6ZGVidCIsInJlYWQ6aW5jb21lIl19.v22noxl1wORjtOo_dhOWOKRL7PvmLR_g09pFVihphVn2NioFim_drKrBY2F5jH0PNHlgfP0LTx4HLgqOCdSp3UvCYWq_lmFi7FdcmGzr0qf-G5GoPqJaPeSR1jFMYr9qxllt0z2UNFG80FjemEJDll87CUPtczLbZxG6bg9QW-1VqCYehusathYudNZIK556k--fEBCuiaQRaTg2JVAJOtRoB0_gfhrbOg0cc9PWdMjjM82OqGJVRDBSLfJWt68y3L--rI7qkMuNn5jRKt2yRS0vC7DBS-OTn7mPp40dD40Ez2lMRnfQAsOZeQN7TdL24FY-PhZGSlTxDhUlzLhDWA'
            }

        self.auth_operations_manager = {
            'Authorization':
            'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJUQXlRa1F5TVRKR1JETTBSa0ZGT0RnNFF6QTFRVVpDTVVJMVFqUkVNMFV6TURFNE9UUTNSZyJ9.eyJpc3MiOiJodHRwczovL2Zyb3N0eS1maXJlZmx5LTQ3NDMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlN2UyNDRlNTkzOTAxMGNjOWMzNjI0YyIsImF1ZCI6ImFwaSIsImlhdCI6MTU4NTQ1MzkwMCwiZXhwIjoxNTg1NDYxMTAwLCJhenAiOiJYNnc0bExBcEtYblBWbXl0bzNIbTRVT0UzUkZqMmk4dyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmRlYnQiLCJkZWxldGU6aW5jb21lIiwicGF0Y2g6ZGVidCIsInBhdGNoOmluY29tZSIsInBvc3Q6Y2FzaGZsb3ciLCJwb3N0OmRlYnQiLCJyZWFkOmJhbGFuY2UiLCJyZWFkOmRlYnQiLCJyZWFkOmluY29tZSJdfQ.3is4tegh_AzbdxrxeYzJEmiQrrNOBy4cGSMQsN_pjRA5_PwDWf5K2mTTHvIkY-BPNGf5RtFwvOaKp3i7Io4jul4NxLfitRuY4trlKJMhrzb75rKkMpoygpFIXfbbYgzXynkfi5JYfzZGblL4Htvf9xrqM3qrasSlzu8y72uql6Sk8C0rRn16JVIvqKJS_54mC3uhQVx5JIIVmO8pZQPJanTMTXABPEHfsu8Z24wM44dcJGG7kTAssjZ1JtCLN3m3HiuV6HdN36h07F427Hb7ZOX18BpygdeEHh0dadLolamAKTteXpfPMkJrlTB6NWbVoEApFxw17iwkbE2eOP4RCA'
        }

        self.auth_admin = {
            'Authorization':
            'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJUQXlRa1F5TVRKR1JETTBSa0ZGT0RnNFF6QTFRVVpDTVVJMVFqUkVNMFV6TURFNE9UUTNSZyJ9.eyJpc3MiOiJodHRwczovL2Zyb3N0eS1maXJlZmx5LTQ3NDMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlN2UyNGViYzBhYjM0MGNkNjY3NjQ4MCIsImF1ZCI6ImFwaSIsImlhdCI6MTU4NTQ1NDIxNCwiZXhwIjoxNTg1NDYxNDE0LCJhenAiOiJYNnc0bExBcEtYblBWbXl0bzNIbTRVT0UzUkZqMmk4dyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmRlYnQiLCJkZWxldGU6aW5jb21lIiwicGF0Y2g6YmFsYW5jZSIsInBhdGNoOmRlYnQiLCJwYXRjaDppbmNvbWUiLCJwb3N0OmNhc2hmbG93IiwicG9zdDpkZWJ0IiwicmVhZDpiYWxhbmNlIiwicmVhZDpkZWJ0IiwicmVhZDppbmNvbWUiXX0.xvnBI0GcAcAMnRocgGi3NBP4_wpL0f4c-zSSNVS2BxIstNuuoKXF-smn5DtrAgagR73bEp8cpsH6RSDGHXAEV-wtmn9L7CD64_au-7oy8V1D1jHHAlQIsSKxqpRoXJfmS-2kS8FKVzMfQ60aRubcDx4TfOOblKziDiaM1WD38Jt4IV4g9Qq5R5F6By54epjOtuLwTtXkrRl49qe0TG8c1Mv08gb2DxbemSCkX3QF0fVe5ryVJlepxsoMQhvzSIS0dRfc4yEoOuxFzA4Buh83XaWZIg7hfUT6Qm6lRh3e8DGk_TR67h_AEys5Yxh0keW3E0wpbi0jghZ1r7klkNvTWg'
            }

        # binds app to current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        pass


    def test_given_behavior(self):
        """Test _____________ """
        res = self.client().get('/')

        self.assertEqual(res.status_code, 200)


    def test_get_paginated_cashflow_items(self):
        res = self.client().get('/cashflow')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_cashflow'])
        self.assertTrue(len(data['cashflow_items']))

    def test_delete_cashflow_item(self):
        res = self.client().delete('/cashflow/1')
        data = json.loads(res.data)

        cashflow = Cashflow.query.filter(Cashflow.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 1)
        self.assertTrue(data['total_cashflow'])
        self.assertEqual(cashflow, None)


    def test_delete_debt_item(self):
        res = self.client().delete('/debt/1')
        data = json.loads(res.data)

        debt = Debt.query.filter(Debt.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 1)
        self.assertTrue(data['total_debt'])
        self.assertEqual(debt, None)


    def test_404_if_cashflow_item_does_not_exist(self):
        res = self.client().delete('/cashflow/10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')


    def test_404_if_debt_item_does_not_exist(self):
        res = self.client().delete('/debt/10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')


    def test_404_if_balancesheet_does_not_exist(self):
        res = self.client().delete('/balance-sheet/10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')


    def _test_create_new_cashflow_item(self):
        res = self.client().post('/cashflow', json=self.new_cashflow)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_cashflow'])

    def _test_create_new_debt_item(self):
        res = self.client().post('/debt', json=self.debt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_debt'])


    def test_422_cashflow_item_creation_fails(self):
        res = self.client().post('/cashflow', json=self.new_cashflow)
        data = json.loads(res.data)
        pass

    def test_422_debt_item_creation_fails(self):
        res = self.client().post('/debt', json=self.new_debt)
        data = json.loads(res.data)
        pass


    def _test_patch_cashflow_item(self):
        res = self.client().patch('/cashflow', json=self.cashflow)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def _test_patch_debt_item(self):
        res = self.client().patch('/debt', json=self.debt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    def _test_patch_balancesheet_(self):
        res = self.client().patch('/balancesheets', json=self.balancesheet)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_422_cashflow_item_patch_fails(self):
        res = self.client().patch('/cashflow', json=self.update_cashflow)
        data = json.loads(res.data)
        pass

    def test_422_debt_item_patch_fails(self):
        res = self.client().patch('/debt', json=self.update_debt)
        data = json.loads(res.data)
        pass

    def test_422_patch_balancesheet_fails(self):
        res = self.client().patch('/balance-sheet', json=self.update_user)
        data = json.loads(res.data)
        pass



if __name__ == "__main__":
    unittest.main()

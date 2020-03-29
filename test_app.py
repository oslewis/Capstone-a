import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import BalanceSheet, Cashflow, Debt, setup_db


class CapstoneTestCase(unittest.TestCase):
    """This class represents the __ test case"""

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = "postgresql://{}/{}".format(
            'localhost:5432', self.database_name
        )
        setup_db(self.app, self.database_path)
        self.auth_specialist = {
            'Authorization':
            'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJUQXlRa1F5TVRKR1JETTBSa0ZGT0RnNFF6QTFRVVpDTVVJMVFqUkVNMFV6TURFNE9UUTNSZyJ9.eyJpc3MiOiJodHRwczovL2Zyb3N0eS1maXJlZmx5LTQ3NDMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlN2UyNTMwMTkwMWY1MGNjODgzZGRlNyIsImF1ZCI6ImFwaSIsImlhdCI6MTU4NTQ1NDA3NiwiZXhwIjoxNTg1NDYxMjc2LCJhenAiOiJYNnc0bExBcEtYblBWbXl0bzNIbTRVT0UzUkZqMmk4dyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsicG9zdDpjYXNoZmxvdyIsInBvc3Q6ZGVidCIsInJlYWQ6ZGVidCIsInJlYWQ6aW5jb21lIl19.v22noxl1wORjtOo_dhOWOKRL7PvmLR_g09pFVihphVn2NioFim_drKrBY2F5jH0PNHlgfP0LTx4HLgqOCdSp3UvCYWq_lmFi7FdcmGzr0qf-G5GoPqJaPeSR1jFMYr9qxllt0z2UNFG80FjemEJDll87CUPtczLbZxG6bg9QW-1VqCYehusathYudNZIK556k--fEBCuiaQRaTg2JVAJOtRoB0_gfhrbOg0cc9PWdMjjM82OqGJVRDBSLfJWt68y3L--rI7qkMuNn5jRKt2yRS0vC7DBS-OTn7mPp40dD40Ez2lMRnfQAsOZeQN7TdL24FY-PhZGSlTxDhUlzLhDWA'
        }
        self.auth_operations_manager = {
            'Authorization':
            'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJUQXlRa1F5TVRKR1JETTBSa0ZGT0RnNFF6QTFRVVpDTVVJMVFqUkVNMFV6TURFNE9UUTNSZyJ9.eyJpc3MiOiJodHRwczovL2Zyb3N0eS1maXJlZmx5LTQ3NDMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlN2UyNDRlNTkzOTAxMGNjOWMzNjI0YyIsImF1ZCI6ImFwaSIsImlhdCI6MTU4NTQ1MzkwMCwiZXhwIjoxNTg1NDYxMTAwLCJhenAiOiJYNnc0bExBcEtYblBWbXl0bzNIbTRVT0UzUkZqMmk4dyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmRlYnQiLCJkZWxldGU6aW5jb21lIiwicGF0Y2g6ZGVidCIsInBhdGNoOmluY29tZSIsInBvc3Q6Y2FzaGZsb3ciLCJwb3N0OmRlYnQiLCJyZWFkOmJhbGFuY2UiLCJyZWFkOmRlYnQiLCJyZWFkOmluY29tZSJdfQ.3is4tegh_AzbdxrxeYzJEmiQrrNOBy4cGSMQsN_pjRA5_PwDWf5K2mTTHvIkY-BPNGf5RtFwvOaKp3i7Io4jul4NxLfitRuY4trlKJMhrzb75rKkMpoygpFIXfbbYgzXynkfi5JYfzZGblL4Htvf9xrqM3qrasSlzu8y72uql6Sk8C0rRn16JVIvqKJS_54mC3uhQVx5JIIVmO8pZQPJanTMTXABPEHfsu8Z24wM44dcJGG7kTAssjZ1JtCLN3m3HiuV6HdN36h07F427Hb7ZOX18BpygdeEHh0dadLolamAKTteXpfPMkJrlTB6NWbVoEApFxw17iwkbE2eOP4RCA'
        }


        self.auth_admin = {
            'Authorization':
            'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJUQXlRa1F5TVRKR1JETTBSa0ZGT0RnNFF6QTFRVVpDTVVJMVFqUkVNMFV6TURFNE9UUTNSZyJ9.eyJpc3MiOiJodHRwczovL2Zyb3N0eS1maXJlZmx5LTQ3NDMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlN2UyNGViYzBhYjM0MGNkNjY3NjQ4MCIsImF1ZCI6ImFwaSIsImlhdCI6MTU4NTQ1NDIxNCwiZXhwIjoxNTg1NDYxNDE0LCJhenAiOiJYNnc0bExBcEtYblBWbXl0bzNIbTRVT0UzUkZqMmk4dyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmRlYnQiLCJkZWxldGU6aW5jb21lIiwicGF0Y2g6YmFsYW5jZSIsInBhdGNoOmRlYnQiLCJwYXRjaDppbmNvbWUiLCJwb3N0OmNhc2hmbG93IiwicG9zdDpkZWJ0IiwicmVhZDpiYWxhbmNlIiwicmVhZDpkZWJ0IiwicmVhZDppbmNvbWUiXX0.xvnBI0GcAcAMnRocgGi3NBP4_wpL0f4c-zSSNVS2BxIstNuuoKXF-smn5DtrAgagR73bEp8cpsH6RSDGHXAEV-wtmn9L7CD64_au-7oy8V1D1jHHAlQIsSKxqpRoXJfmS-2kS8FKVzMfQ60aRubcDx4TfOOblKziDiaM1WD38Jt4IV4g9Qq5R5F6By54epjOtuLwTtXkrRl49qe0TG8c1Mv08gb2DxbemSCkX3QF0fVe5ryVJlepxsoMQhvzSIS0dRfc4yEoOuxFzA4Buh83XaWZIg7hfUT6Qm6lRh3e8DGk_TR67h_AEys5Yxh0keW3E0wpbi0jghZ1r7klkNvTWg'
        }

        self.new_cashflow = {
            "id": 1,
            "name": "Merlin",
            "amount": 891,
            "category": "Investments"
        }

        self.new_debt = {
            "id": 1,
            "name": "Helix",
            "amount": 891,
            "category": "Administration"
        }

        self.balancesheet = {
            "id": 1,
            "total_debt": 60012,
            "total_cashflow": 1000512,
        }


        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_given_behavior(self):
        """Test _____________ """
        res = self.client().get('/')

        self.assertEqual(res.status_code, 200)

    def test_get_cashflow(self):
        """Test _____________ """
        res = self.client().get('/cashflow', headers=self.auth_specialist)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_404_sent_requesting_false_endpoint(self):
        res = self.client().get('/cashflow', headers=self.auth_specialist)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], 'Not found')

    def test_post_cashflow(self):
        res = self.client().post('/cashflow', json={
            'name': 'Helix',
            'amount': 891
        }, headers=self.auth_specialist)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_debt_manager(self):
        self.client().post('/debt', json={
            'name': 'Helix',
            'amount': 891
        }, headers=self.auth_operations_manager)
        res = self.client().get('/debt/1', headers=self.auth_operations_manager)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["name"])


    def test_delete_cashflow(self):
        self.client().post('/cashflow', json={
            'name': 'Helix',
            'amount': 891
        }, headers=self.auth_operations_manager)
        res = self.client().delete('/cashflow/1', headers=self.auth_operations_manager)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_cashflow_with_wrong_id(self):
        res = self.client().delete('/cashflow/9811231', headers=self.auth_operations_manager)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data["message"], 'unprocessable')

    def test_update_cashflow(self):
        self.client().post('/cashflow', json={
            'name': 'Helix',
            'amount': 891
        }, headers=self.auth_operations_manager)
        res = self.client().patch('/cashflow/1', json={
            'name': 'Merlin',
            'amount': 10000
        }, headers=self.auth_operations_manager)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_update_cashflow_with_wrong_id(self):
        res = self.client().patch('/cashflow/101', json={
            'name': 'Helix',
            'amount': 899
        }, headers=self.auth_operations_manager)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data["message"], 'unprocessable')

    def test_get_debt(self):
        res = self.client().get('/debt', headers=self.auth_specialist)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_get_debts(self):
        self.client().post('/debt', json={
            'name': 'Vale',
            'amount': 812,
            'category': 'Technology'
        }, headers=self.auth_specialist)
        res = self.client().get('/debt/1', headers=self.auth_specialist)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["debt"])

    def test_post_debt(self):
        res = self.client().post('/debt', json={
            'name': 'Merlin',
            'amount': 799,
            'category': 'Investments'
        }, headers=self.auth_operations_manager)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Debt Payment Indexed.')

    def test_delete_debt(self):
        self.client().post('/debt', json={
            'name': 'Merlin',
            'amount': 799,
            'cateogry': 'Investments'
        }, headers=self.auth_operations_manager)
        res = self.client().delete('/debt/1', headers=self.auth_operations_manager)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_update_debt(self):
        self.client().post('/debt', json={
            'name': 'Merlin',
            'amount': 899,
            'category': 'Investments'
        }, headers=self.auth_operations_manager)
        res = self.client().patch('/debt/1', json={
            'name': 'Debt Payment indexed.',
            'amount': 812,
            'category': 'Investments'
        }, headers=self.auth_operations_manager)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_get_balance_sheet(self):
        res = self.client().get('/balance-sheet', headers=self.auth_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)


    def test_update_balance_sheet(self):
        self.client().post('/balancesheets', json={
            'total_debt': 60012,
            'total_cashflow': 1000512
        }, headers=self.auth_admin)
        res = self.client().patch('/balancesheets/1', json={
            'total_debt': 70000,
            'total_cashflow': 1001500
        }, headers=self.auth_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)




if __name__ == "__main__":
    unittest.main()

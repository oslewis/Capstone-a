
import os 
import unittest
import json
from flask_sqlalchemy import SQLAlchemy 
import app
import models as models
from app import create_app
from models import Cashflow, Debt, User, setup_db

class Capstone_me_TestCase(unittest.TestCase):
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

        self.new_user = {
            "id": 1,
            "name": "John Doe",
            "email": "john@example.com"
        }


        # binds app to current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        pass
    
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


    def test_delete_user(self):
        res = self.client().delete('/user/1')
        data = json.loads(res.data)

        user = User.query.filter(User.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 1)
        self.assertEqual(user, None)


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

    def test_404_if_user_does_not_exist(self):
        res = self.client().delete('/user/10000')
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

    def _test_create_new_user(self):
        res = self.client().post('/user', json=self.debt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_cashflow_item_creation_fails(self):
        res = self.client().post('/cashflow', json=self.new_cashflow)
        data = json.loads(res.data)
        pass
        
    def test_422_debt_item_creation_fails(self):
        res = self.client().post('/debt', json=self.new_debt)
        data = json.loads(res.data)
        pass

    def test_422_user_creation_fails(self):
        res = self.client().post('/user', json=self.new_user)
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
    
    def _test_patch_user_(self):
        res = self.client().patch('/user', json=self.user)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def _test_patch_balancesheet_(self):
        res = self.client().patch('/balancesheets', json=self.balancesheet)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_user_patch_fails(self):
        res = self.client().patch('/user', json=self.update_user)
        data = json.loads(res.data)
        pass

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
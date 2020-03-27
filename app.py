#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------- Imports ------------------ #
from flask import (
        Flask,
        request,
        abort,
        jsonify
        )
from flask_sqlalchemy import SQLAlchemy
import json
from flask_cors import CORS
from auth import AuthError, requires_auth
from sqlalchemy import func, exc
from models import Account, BalanceSheet, Cashflow, Debt, setup_db
from sqlalchemy.orm import session
from werkzeug.exceptions import HTTPException
from os import environ as env
from functools import wraps
import os
import math


# ------------------------------------------------- #


CASHFLOW_ITEMS_PER_PAGE = 10
DEBT_ITEMS_PER_PAGE = 10

def paginate_cashflow_items(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * CASHFLOW_ITEMS_PER_PAGE
    end = start + CASHFLOW_ITEMS_PER_PAGE

    cashflow_glossary = [cashflow_glossary.format() for cashflow in selection]
    current_cashflow = cashflow_glossary[start:end]

def paginate_debt_items(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * DEBT_ITEMS_PER_PAGE
    end = start + DEBT_ITEMS_PER_PAGE

    debt_glossary = [debt_glossary.format() for debt in selection]
    current_debt = debt_glossary[start:end]


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response


# -------------------------------------------------- #
# ------------- GET Routes ------------------------- #
# -------------------------------------------------- #


    '''
    App route - get data.
    '''

    '''
    Read Cashflow Index.
    '''
    @app.route('/cashflow', methods=['GET'])
    @requires_auth('read:income')
    def retrieve_cashflow(payload):
        current_cashflow = Cashflow.query.order_by(Cashflow.id).all()

        if len(current_cashflow) == 0:
            abort(404)

        cashflow_items = [cashflow.format() for cashflow in current_cashflow]

        return jsonify({
            "success": True,
            "cashflow_items": current_cashflow,
            "total_cashflow": session.query(func.count(Cashflow.amount)),
        }), 200


    '''
    Read Debt Payment.
    '''
    @app.route('/debt', methods=['GET'])
    @requires_auth('read:debt')
    def retrieve_debtflow(payload):
        current_debtflow = Debt.query.order_by(Debt.id).all()

        if len(current_debtflow) == 0:
            abort(404)

        debtflow_items = [debt.format() for debt in current_debtflow]

        return jsonify({
            "success": True,
            "debtflow_items": current_debtflow,
            "total_debt": session.query(func.count(Debt.amount)),
        }), 200


    '''
    View Balance Sheet.
    ''' 
    @app.route('/balance-sheet', methods=['GET'])
    @requires_auth('read:balance')
    def retrieve_balancesheet(payload):
        balancesheet_log = BalanceSheet.query.order_by(BalanceSheet.id).all()

        if len(balancesheet_log) == 0:
            abort(404)
        y = session.query(func.count(Cashflow.amount))
        x = session.query(func.count(Debt.amount))
        z = session.query(func.count(Account.cash))
        balancesheets = [balancesheet.format() for balancesheet in balancesheet_log]

        return jsonify({
            "success": True,
            "balancesheets": balancesheet_log,
            "total_debt": session.query(func.count(Debt.amount)),
            "total_cashflow": session.query(func.count(Cashflow.amount)),
            "time": BalanceSheet.time_left(x,y,z)
        }), 200

# -------------------------------------------------- #
# ------------- DELETE Routes ---------------------- #
# -------------------------------------------------- #

    '''
    App route - Delete.
    '''

    '''
    Delete Cashflow index.
    '''
    @app.route('/cashflow/<id>', methods=['DELETE'])
    @requires_auth('delete:income')
    def delete_cashflow_item(payload, id):
        try:
            cashflow_item = Cashflow.query.filter(Cashflow.id == id).one_or_none()
            if cashflow_item is None:
                abort(404)

            cashflow_item.delete()
            selection = Cashflow.query.order_by(Cashflow.id).all()
            current_cashflow = paginate_cashflow_items(request, selection)
            return jsonify({
                "success": True,
                "delete": id,
                "cashflow_items": current_cashflow,
                "total_cashflow": session.query(func.count(Cashflow.amount))
            }), 200

        except:
            abort(422)



    '''
    Delete Debt Payment.
    '''
    @app.route('/debt/<id>', methods=['DELETE'])
    @requires_auth('delete:debt')
    def delete_debt_item(payload, id):
        try:
            debt_item = Debt.query.filter(Debt.id == id).one_or_none()
            if debt_item is None:
                abort(404)

            debt_item.delete()
            selection = Debt.query.order_by(Debt.id).all()
            current_debt = paginate_debt_items(request, selection)
            return jsonify({
                "success": True,
                "delete": id,
                "debt_items": current_debt,
                "total_debt": session.query(func.count(Debt.amount))
            }), 200

        except:
            abort(422)

# -------------------------------------------------- #
# ------------- POST / Create Routes --------------- #
# -------------------------------------------------- #

    '''
    App routes to add data.
    '''

    '''
    Create Debt payment.
    '''
    @app.route('/debt/create', methods=['POST'])
    @requires_auth('post:debt')
    def create_debt_item(token):
        body = request.get_json()
        new_name = body.get('name', None)
        new_category = body.get('category', None)
        new_amount = body.get('amount', None)
        search = body.get('searchTerm')
        try:
            debt = Debt(name=new_name, category=new_category, amount=new_amount)
            debt.insert()
            selection = Debt.query.order_by(Debt.id).all()
            current_debt = paginate_debt_items(request, selection)
            return jsonify({
                "success": True,
                "create": debt.id,
                "debt": debt.format(),
                "total_debt": session.query(func.count(Debt.amount)),
                "debt_items": current_debt
            }), 201
        except:
            abort(422)

    '''
    Create Cashflow Index.
    '''
    @app.route('/cashflow/create', methods=['POST'])
    @requires_auth('post:cashflow')
    def create_cashflow_item(token):
        body = request.get_json()
        new_name = body.get('name', None)
        new_category = body.get('category', None)
        new_amount = body.get('amount', None)
        search = body.get('searchTerm')
        try:
            cashflow = Cashflow(name=new_name, category=new_category, amount=new_amount)
            cashflow.insert()
            selection = Cashflow.query.order_by(Cashflow.id).all()
            current_cashflow = paginate_cashflow_items(request, selection)
            return jsonify({
                "success": True,
                "create": cashflow.id,
                "cashflow": cashflow.format(),
                "total_cashflow": session.query(func.count(Cashflow.amount)),
                "cashflow_items": current_cashflow
            }), 201
        except:
            abort(422)


# -------------------------------------------------- #
# ------------- Update / PATCH Routes -------------- #
# -------------------------------------------------- #

    '''
    App routes to update data.
    '''

    '''
    Update cashflow payment index.
    '''
    @app.route('/cashflow/<id>', methods=['PATCH'])
    @requires_auth('patch:income')
    def update_cashflow_item(payload, id):
        try:
            body = request.get_json()
            update_name = body.get('name', None)
            update_category = body.get('category', None)
            update_amount = body.get('amount', None)
            cashflow_item = Cashflow.query.filter(Cashflow.id == id).one_or_none()
            if cashflow_item is None:
                abort(404)
            cashflow_item.name = update_name
            cashflow_item.category = update_category
            cashflow_item.amount = update_amount
            cashflow_item.update()
            return jsonify({
                "success": True,
                "id": cashflow_item.id,
                "cashflow": cashflow_item.format()
            }), 200

        except:
            abort(400)

    '''
    Update Debt payment which is due.
    '''
    @app.route('/debt/<id>', methods=['PATCH'])
    @requires_auth('patch:debt')
    def update_debt_item(payload, id):
        try:
            body = request.get_json()
            update_name = body.get('name', None)
            update_category = body.get('category', None)
            update_amount = body.get('amount', None)
            debt_item = Debt.query.filter(Debt.id == id).one_or_none()
            if debt_item is None:
                abort(404)
            debt_item.name = update_name
            debt_item.category = update_category
            debt_item.amount = update_amount
            debt_item.update()
            return jsonify({
                "success": True,
                "id": debt_item.id,
                "debt": debt_item.format()
            }), 200
        except:
            abort(400)


    '''
    Update Balance Sheet, only updating name is possible. As the balance sheet reflects total cash and debt numbers.
    '''
    @app.route('/balancesheets/<id>', methods=['PATCH'])
    @requires_auth('patch:balance')
    def update_balance_sheet(payload, id):
        try:
            body = request.get_json()
            update_name = body.get('name', None)
            balancesheet = BalanceSheet.query.filter(BalanceSheet.id == id).one_or_none()
            if balancesheet is None:
                abort(404)
            balancesheet.name = update_name
            balancesheet.update()
            return jsonify({
                "success": True,
                "id": balancesheet.id,
                "balancesheet": balancesheet.format()
            }), 200
        except:
            abort(400)


# -------------------------------------------------- #
# ------------- Error Handlers --------------------- #
# -------------------------------------------------- #
    '''
    Error Handler - when resource could not be found.
    '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found."
        }), 404

    '''
    Error Handler when request is not processable.
    '''
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
        }), 422

    '''
    Error Handler for a bad request.
    '''
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    '''
    Error Handler - When method is not allowed.
    '''
    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405


    '''
    Error Handler for an internal server error.
    '''
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal server error, please check and try again."
        }), 500


    '''
    Error Handler for AuthError
    '''
    @app.errorhandler(AuthError)
    def auth_error(auth_error):
        return jsonify({
            "success": False,
            "error": auth_error.status_code,
            "message": auth_error.error
        }), auth_error.status_code


    return app

APP = create_app()

if __name__ == '__main__':
   APP.run(host='0.0.0.0', port=8080, debug=True)

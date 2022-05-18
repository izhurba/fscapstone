import os
from flask import Flask, request, abort, jsonify, redirect, session
from models import setup_db, fieldTech, leadTech, seniorTech, db
from auth import AuthError, requires_auth
from flask_cors import CORS
from psycopg2 import errors
import json


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/')
    def landing_page():
        return jsonify({
            'success': True
        }), 200

    @app.route('/login')
    def auth_login():
        return redirect("https://dev-vqzjqwjq.us.auth0.com/authorize?response_type=token&client_id=TUWUbKOBYQXR4oZ0xwB4CjLjwypkx787&redirect_uri="+ os.environ["REDIRECTURL"] + "&audience=repairshop")

    @app.route('/logout')
    def auth_logout():
        return redirect("https://dev-vqzjqwjq.us.auth0.com/v2/logout?client_id=TUWUbKOBYQXR4oZ0xwB4CjLjwypkx787&returnTo="+ os.environ["REDIRECTURL"])

    # Endpoint to get field techs

    @app.route('/fieldtechs')
    @requires_auth('get:fieldtech')
    def get_fieldtechs(jwt):
        try:
            fieldTechs = fieldTech.query.all()

            if not fieldTechs:
                abort(404)

            return jsonify({
                'success': True,
                'fieldtechs': [tech.format() for tech in fieldTechs]
            }), 200
        except Exception as e:
            abort(403)

    # Endpoint to get lead techs

    @app.route('/leadtechs')
    @requires_auth('get:leadtech')
    def get_leadtechs(jwt):
        try:
            leadTechs = leadTech.query.all()

            if not leadTechs:
                abort(404)

            return jsonify({
                'success': True,
                'leadtechs': [tech.format() for tech in leadTechs]
            }), 200
        except Exception as e:
            abort(403)

    # Endpoint to get lead techs

    @app.route('/seniortechs')
    @requires_auth('get:seniortech')
    def get_seniortechs(jwt):
        try:
            sTechs = seniorTech.query.all()
            if not sTechs:
                abort(404)

            return jsonify({
                'success': True,
                'seniortechs': [tech.format() for tech in sTechs]
            }), 200
        except Exception as e:
            print(e)
            abort(403)

    # Endpoint to create a new field tech

    @app.route('/fieldtechs', methods=['POST'])
    @requires_auth('post:fieldtech')
    def post_fieldtech(jwt):
        data = request.get_json()

        try:
            newFTech = fieldTech(
                name=data['name'],
                employeeID=data['employeeID']
            )
            newFTech.insert()

            fieldTechs = fieldTech.query.all()

            return jsonify({
                'success': True,
                'fieldtechs': [tech.format() for tech in fieldTechs]
            }), 200
        except Exception as e:
            print(e)
            abort(400)

    # Endpoint to create a new lead tech

    @app.route('/leadtechs', methods=['POST'])
    @requires_auth('post:leadtech')
    def post_leadtech(jwt):
        data = request.get_json()

        try:
            newLTech = leadTech(
                name=data['name'],
                employeeID=data['employeeID'],
                fieldtech_ids=data['fieldtech_ids']
            )
            newLTech.insert()

            leadTechs = leadTech.query.all()

            return jsonify({
                'success': True,
                'leadtechs': [tech.format() for tech in leadTechs]
            }), 200
        except Exception as e:
            abort(400)

    # Endpoint to update information for an existing field tech

    @app.route('/fieldtechs/<int:id>', methods=['PATCH'])
    @requires_auth('patch:fieldtech')
    def update_fieldtech(jwt, id):
        data = request.get_json()

        fTechUpdate = fieldTech.query.get(id)
        try:
            if not fTechUpdate:
                abort(400)
            if data['name']:
                fTechUpdate.name = data['name']
            if data['employeeID']:
                fTechUpdate.employeeID = data['employeeID']
            fTechUpdate.update()

            fTechs = fieldTech.query.all()

            return jsonify({
                'success': True,
                'fieldtechs': [tech.format() for tech in fTechs]
            }), 200
        except Exception as e:
            abort(422)

    # Endpoint to update information for an existing lead tech

    @app.route('/leadtechs/<int:id>', methods=['PATCH'])
    @requires_auth('patch:leadtech')
    def update_leadtech(jwt, id):
        data = request.get_json()

        lTechUpdate = leadTech.query.get(id)
        try:
            if not lTechUpdate:
                abort(400)
            if data['name']:
                lTechUpdate.name = data['name']
            if data['employeeID']:
                lTechUpdate.employeeID = data['employeeID']
            if data['fieldtech_ids']:
                lTechUpdate.fieldtech_ids = data['fieldtech_ids']
            lTechUpdate.update()

            lTechs = leadTech.query.all()

            return jsonify({
                'success': True,
                'leadtechs': [tech.format() for tech in lTechs]
            }), 200
        except Exception as e:
            abort(422)

    # Endpoint to delete a field tech via fieldTech.id

    @app.route('/fieldtechs/<int:id>', methods=['DELETE'])
    @requires_auth('delete:fieldtech')
    def delete_fieldtech(jwt, id):
        fTech = fieldTech.query.filter(fieldTech.id == id).one_or_none()

        if not fTech:
            abort(404)
        try:
            fTech.delete()
            return jsonify({
                'success': True,
                'delete': id
            }), 200
        except Exception as e:
            abort(400)

    # Endpoint to delete a lead tech via leaddTech.id

    @app.route('/leadtechs/<int:id>', methods=['DELETE'])
    @requires_auth('delete:leadtech')
    def delete_leadtech(jwt, id):
        lTech = leadTech.query.filter(leadTech.id == id).one_or_none()

        if not lTech:
            abort(404)
        try:
            lTech.delete()
            return jsonify({
                'success': True,
                'delete': id
            }), 200
        except Exception as e:
            abort(400)

    # Error Handling

    @app.errorhandler(400)
    def bad_request_error(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': "Bad Request"
        }), 400

    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': "Not Found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 422

    @app.errorhandler(403)
    def authorization_error(error):
        return jsonify({
            'success': False,
            'error': 403,
            'message': "You are not authorized to perform this action"
        }), 403

    return app


app = create_app()

if __name__ == '__main__':
    app.run()

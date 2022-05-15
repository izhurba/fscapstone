import os
from flask import Flask, request, abort, jsonify
from models import setup_db, fieldTech, leadTech, seniorTech
from flask_cors import CORS
from .auth.auth import AuthError, requires_auth


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    # Endpoint to get field techs


    @app.route('/fieldtechs')
    def get_fieldtechs():
        fieldTechs = fieldTech.query.all()

        if not fieldTechs:
            abort(404)

        return jsonify({
            'success': True,
            'fieldtechs': fieldTechs 
        }), 200

    # Endpoint to get lead techs


    @app.route('/leadtechs')
    def get_leadtechs():
        leadTechs = leadTech.query.all()

        if not leadTechs:
            abort(404)

        return jsonify({
            'success': True,
            'leadtechs': leadTechs 
        }), 200

    # Endpoint to get lead techs


    @app.route('/seniortechs')
    @requires_auth('get:seniortech')
    def get_seniortechs():
        try:
            seniorTechs = seniorTech.query.all()

            if not seniorTechs:
                abort(404)

            return jsonify({
                'success': True,
                'seniortechs': seniorTechs 
            }), 200
        except Exception as e:
            print(e)
            abort(400)

    # Endpoint to create a new field tech


    @app.route('/fieldtechs', methods=['POST'])
    @requires_auth('post:fieldtech')
    def post_fieldtech(jwt):
        data = request.get_json()

        try:
            newFTech = fieldTech(
                name = data['name'],
                employeeID= data['employeeID']
            )
            newFTech.insert()

            fieldTechs = fieldTech.query.all()

            return jsonify({
                'success': True,
                'fieldtechs': fieldTechs
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
                name = data['name'],
                employeeID= data['employeeID'],
                fieldtech_ids= ['fieldtech_ids']
            )
            newLTech.insert()

            leadTechs = leadTech.query.all()

            return jsonify({
                'success': True,
                'leadtechs': leadTechs
            }), 200
        except Exception as e:
            print(e)
            abort(400)

    # Endpoint to update information for an existing field tech


    @app.route('/fieldtechs/<int:id>', methods=['PATCH'])
    @requires_auth('patch:fieldtech')
    def update_fieldtech(jwt, id):
        data = request.get_json()
        fTechUpdate = fieldTech.query.get(id)
        try:
            if not fTechUpdate:
                abort(404)
            if data['name']:
                fTechUpdate.title = data['name']
            if data['employeeID']:
                fTechUpdate.recipe = data['employeeID']
            fTechUpdate.update()

            fTechs = fieldTech.query.all()

            return jsonify({
                'success': True,
                'fieldtechs': fTechs
            }), 200
        except Exception as e:
            print(e)
            abort(400)

    # Endpoint to update information for an existing lead tech


    @app.route('/leadtechs/<int:id>', methods=['PATCH'])
    @requires_auth('patch:leadtech')
    def update_leadtech(jwt, id):
        data = request.get_json()
        lTechUpdate = leadTech.query.get(id)
        try:
            if not lTechUpdate:
                abort(404)
            if data['name']:
                lTechUpdate.title = data['name']
            if data['employeeID']:
                lTechUpdate.recipe = data['employeeID']
            if data['fieldtech_ids']:
                lTechUpdate.fieldtech_ids = data['fieldtech_ids']
            lTechUpdate.update()

            lTechs = leadTech.query.all()

            return jsonify({
                'success': True,
                'fieldtechs': lTechs
            }), 200
        except Exception as e:
            print(e)
            abort(400)
    
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
            print(e)
            abort(AuthError)

    # Endpoint to delete a lead tech via leaddTech.id


    @app.route('/leadtechs/<int:id>', methods=['DELETE'])
    @requires_auth('delete:leadtech')
    def delete_fieldtech(jwt, id):
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
            print(e)
            abort(AuthError)
    
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


    @app.errorhandler(AuthError)
    def authorization_error(error):
        return jsonify({
            'success': False,
            'error': AuthError,
            'message': "You are not authorized to perform this action"
            }), 404

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=4455)

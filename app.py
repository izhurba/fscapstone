import os
from flask import Flask, request, abort, jsonify
from models import setup_db, fieldTech, leadTech, seniorTech
from auth import AuthError, requires_auth
from flask_cors import CORS

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # Endpoint to get field techs


    @app.route('/fieldtechs')
    def get_fieldtechs():
        fieldTechs = fieldTech.query.all()

        if not fieldTechs:
            abort(404)

        return jsonify({
            'success': True,
            'fieldtechs': [tech.format() for tech in fieldTechs]
        }), 200

    # Endpoint to get lead techs

    @app.route('/leadtechs')
    def get_leadtechs():
        leadTechs = leadTech.query.all()

        if not leadTechs:
            abort(404)

        return jsonify({
            'success': True,
            'leadtechs': [tech.format() for tech in leadTechs]
        }), 200

    # Endpoint to get lead techs

    @app.route('/seniortechs')
    def get_seniortechs():
        if requires_auth('get:seniortech'):
            sTechs = seniorTech.query.all()
            try:
                if not sTechs:
                    abort(404)

                return jsonify({
                    'success': True,
                    'seniortechs': [tech.format() for tech in sTechs]
                }), 200
            except Exception as e:
                print(e)
                abort(422)
        abort(403)

    # Endpoint to create a new field tech

    @app.route('/fieldtechs', methods=['POST'])
    def post_fieldtech():
        if requires_auth('post:fieldtech'):
            data = request.get_json()

            try:
                newFTech = fieldTech(
                    name= data['name'],
                    employeeID=data['employeeID']
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
        abort(403)

    # Endpoint to create a new lead tech

    @app.route('/leadtechs', methods=['POST'])
    def post_leadtech():
        if requires_auth('post:leadtech'):
            data = request.get_json()

            try:
                newLTech = leadTech(
                    name= data['name'],
                    employeeID=data['employeeID'],
                    fieldtech_ids=['fieldtech_ids']
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
        abort(403)

    # Endpoint to update information for an existing field tech

    @app.route('/fieldtechs/<int:id>', methods=['PATCH'])
    def update_fieldtech(id):
        if requires_auth('patch:fieldtech'):
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
        abort(403)

    # Endpoint to update information for an existing lead tech

    @app.route('/leadtechs/<int:id>', methods=['PATCH'])
    def update_leadtech(id):
        if requires_auth('patch:leadtech'):
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
        abort(403)

    # Endpoint to delete a field tech via fieldTech.id

    @app.route('/fieldtechs/<int:id>', methods=['DELETE'])
    def delete_fieldtech(id):
        if requires_auth('delete:fieldtech'):
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
                abort(400)
        abort(403)

    # Endpoint to delete a lead tech via leaddTech.id

    @app.route('/leadtechs/<int:id>', methods=['DELETE'])
    def delete_fieldtech(id):
        if requires_auth('delete:leadtech'):
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
                abort(400)
        abort(403)

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
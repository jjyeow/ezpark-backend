from flask import Blueprint, request, json, jsonify
from models.user import User
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, jwt_required

users_api_blueprint = Blueprint('users_api',
                             __name__,
                             template_folder='templates')

@users_api_blueprint.route('/', methods=['GET'])
def index():
    return "USERS API"

@users_api_blueprint.route('/signup', methods=['POST'])
def create():
    username = request.json.get('username')
    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')
    email = request.json.get('email')
    password = request.json.get('password')
    hp_number = request.json.get('hp_number')

    user = User(username=username, email=email, first_name = first_name, last_name = last_name, password=password, hp_number=hp_number)

    if user.save():
        # access_token
        responseObj = {
            'status': 'success',
            'message': 'User successfully created',
            'user': {"id": int(user.id), "username": user.username, "email": user.email, "first_name": user.first_name, "last_name": user.last_name, "hp_number": user.hp_number}
        }

        return jsonify(responseObj), 200

    else: 
        responseObj = {
            'status': 'failed',
            'message': user.errors
        }

        return jsonify(responseObj), 400

@users_api_blueprint.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    user = User.get_or_none(username=username)

    if user: 
        if check_password_hash(user.password, password):
             access_token = create_access_token(identity=username)
             responseObj = {
                 'status': 'success',
                 'message': 'Login successfully!',
                 'token': access_token,
                 'user': {"id": int(user.id), "username": user.username, "email": user.email, "first_name": user.first_name, "last_name": user.last_name, "hp_number": user.hp_number}
             }

             return jsonify(responseObj), 200
        else: 
            responseObj = {
                'status': 'failed',
                'message': 'Login failed!'
                }
            return jsonify(responseObj), 400
    
    else: 
        responseObj = {
            'status': 'failed',
            'message': 'Username is incorrect'
        }

        return jsonify(responseObj), 400

@users_api_blueprint.route('/edit_username/<id>', methods=['POST'])
@jwt_required
def edit_username(id):
    username = get_jwt_identity()
    current_user = User.get_or_none(username = username)
    user = User.get_or_none(id)

    if current_user == user: 
        new_username = request.json.get('new_username')
        update = User.update(username = new_username).where(User.id == current_user.id)

        if update.execute():
            responseObj = {
                'status': 'success',
                'message': 'Username updated successfully',
                'user': {"id": int(user.id), "username": user.username, "email": user.email, "first_name": user.first_name, "last_name": user.last_name, "hp_number": user.hp_number}
            }

            return jsonify(responseObj), 200
        
        else: 
            responseObj = {
                'status': 'failed',
                'message': 'Username failed to update'
            }

            return jsonify(responseObj), 400

    else: 
        responseObj = {
            'status': 'failed',
            'message': 'You can\'t update someone\'s profile!'
        }
        
        return jsonify(responseObj), 400

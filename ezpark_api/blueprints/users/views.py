from flask import Blueprint, request, json, jsonify
from models.user import User
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash
import re

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
             access_token = create_access_token(identity=user.id)
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

@users_api_blueprint.route('/edit_username', methods=['POST'])
@jwt_required
def edit_username():
    user_id = get_jwt_identity()
    current_user = User.get_or_none(User.id==user_id)
    errors = []
    new_username = request.json.get('new_username')
    duplicate_username = User.get_or_none(username=new_username)

    if duplicate_username:
        errors.append('Username has been taken')
        responseObj = {
                'status': 'failed',
                'message': errors
            }
        return jsonify(responseObj), 400

    update = User.update(username = new_username).where(User.id == current_user.id)

    if update.execute():
        responseObj = {
            'status': 'success',
            'message': 'Username updated successfully',
            'user': {"id": int(current_user.id), "username": current_user.username, "email": current_user.email, "first_name": current_user.first_name, "last_name": current_user.last_name, "hp_number": current_user.hp_number}
        }

        return jsonify(responseObj), 200
    
    else: 
        responseObj = {
            'status': 'failed',
            'message': 'Username failed to update'
        }

        return jsonify(responseObj), 400

@users_api_blueprint.route('/edit_password', methods = ['POST'])
@jwt_required
def edit_pw():
    user_id = get_jwt_identity()
    current_user = User.get_or_none(User.id==user_id)
    new_password = request.json.get('new_password')
    errors = []

    if len(new_password) < 6:
        errors.append('Password has to be at least 6 characters!')
    elif re.search('[0-9]', new_password) is None:
        errors.append('Password must have at least 1 number!')
    elif re.search('[A-Z]', new_password) is None:
        errors.append('Password must have at least 1 capital letter!')
    elif re.search("[$&+,_:;=?@#\"\\/|'<>.^*()%!-]", new_password) is None:
        errors.append('Password must have at least 1 special character!')

    if len(errors) == 0: 
        new_password_hashed = generate_password_hash(new_password)
        update = User.update(password = new_password_hashed).where(User.id == current_user.id)
        if update.execute():
            responseObj = {
                'status': 'success',
                'message': 'Password updated successfully',
                'user': {"id": int(current_user.id), "username": current_user.username, "email": current_user.email, "first_name": current_user.first_name, "last_name": current_user.last_name, "hp_number": current_user.hp_number}
            }
            return jsonify(responseObj), 200
        
        else: 
            responseObj = {
                'status': 'failed',
                'message': 'Password failed to update'
            }
            return jsonify(responseObj), 400 
    
    else: 
        responseObj = {
                'status': 'failed',
                'message': errors
            }

        return jsonify(responseObj), 400 

@users_api_blueprint.route('/edit_email', methods = ['POST'])
@jwt_required
def edit_email():
    user_id = get_jwt_identity()
    current_user = User.get_or_none(User.id==user_id)
    new_email = request.json.get('new_email')
    errors = []
    duplicate_email = User.get_or_none(email = new_email)
    if duplicate_email: 
        errors.append('Email has been taken')
        responseObj = {
                'status': 'failed',
                'message': errors
            }
        return jsonify(responseObj), 400

    if re.search('[A-Za-z0-9._%+-]+@+[A-Za-z]+[.]+[c][o][m]', new_email) is None:
        errors.append('Invalid email')

    if len(errors) == 0: 
        update = User.update(email = new_email).where(User.id == current_user.id)
        if update.execute():
            responseObj = {
                'status': 'success',
                'message': 'Email updated successfully',
                'user': {"id": int(current_user.id), "username": current_user.username, "email": current_user.email, "first_name": current_user.first_name, "last_name": current_user.last_name, "hp_number": current_user.hp_number}
            }
            return jsonify(responseObj), 200
        
        else: 
            responseObj = {
                'status': 'failed',
                'message': 'Email failed to update'
            }
            return jsonify(responseObj), 400 
    
    else: 
        responseObj = {
                'status': 'failed',
                'message': errors
            }

        return jsonify(responseObj), 400 



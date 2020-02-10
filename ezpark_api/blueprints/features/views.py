from flask import Blueprint, request, json, jsonify
from models.mall import Mall
from models.history import History
from models.parking import Parking
from models.floor import Floor
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash
import re

features_api_blueprint = Blueprint('features_api',
                             __name__,
                             template_folder='templates')

@features_api_blueprint.route('/', methods=['GET'])
def index():
    malls = Mall.select()
    malls_name_arr = [] 
    for mall in malls:
        malls_name_arr.append({"name": mall.outlet})

    responseObj = {
        'status': 'success',
        'mall': malls_name_arr
    }

    return jsonify(responseObj), 200

@features_api_blueprint.route('/history', methods=['GET'])
@jwt_required
def history(): 
    user_id = get_jwt_identity()
    current_user = User.get_by_id(user_id)
    history_obj = History.get_or_none(user_id = user_id)
    history_arr = []

    for history in history_obj: 
        history_list = {
            'floor': Floor.get_by_id(Parking.get_by_id(history.parking_id).floor_id).floor,
            'parking': Parking.get_by_id(history.parking_id).parking_num,
            'start': history.created_at
        }
        history_arr.append(history_list)

    if history_obj: 
        responseObj = {
            'status': 'success',
            'history': history_arr
        }

        return jsonify(responseObj), 200

    else: 
        responseObj = {
            'status': 'success',
            'history': 'No history'
        }
        
        return jsonify(responseObj), 200




from flask import Blueprint, request, json, jsonify
from models.mall import Mall
from models.history import History
from models.parking import Parking
from models.floor import Floor
from models.user import User
from models.mall import Mall
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
    history_obj = History.select().where(user_id == user_id)
    history_arr = []

    if history_obj: 
        for history in history_obj: 
            history_list = {
                'mall': Mall.get_by_id(Floor.get_by_id(Parking.get_by_id(history.parking_id).floor_id).mall_id).outlet,
                'floor': Floor.get_by_id(Parking.get_by_id(history.parking_id).floor_id).floor,
                'parking': Parking.get_by_id(history.parking_id).parking_num,
                'start': history.created_at,
                'id': history.id
            }
            history_arr.append(history_list)

        responseObj = {
            'status': 'success',
            'history': history_arr
        }

        return jsonify(responseObj), 200

    else: 
        responseObj = {
            'status': 'success',
            'history': history_arr
        }
        
        return jsonify(responseObj), 200


@features_api_blueprint.route('/history_add', methods=['POST'])
@jwt_required
def history_add():
    user_id = get_jwt_identity()
    parking_id = [1,2,3,4,5,6,7,8]

    for parking in parking_id: 
        history_inst = History(user_id = user_id, parking_id = parking)
        history_inst.save()
    

@features_api_blueprint.route('/history_delete/<id>', methods=['POST'])
@jwt_required
def history_delete(id):
    user_id = get_jwt_identity()
    history = History.get_by_id(id)
    if history.delete_instance():
        history_obj = History.select().where(user_id == user_id)
        history_arr = []
        if history_obj: 
            for history in history_obj: 
                history_list = {
                    'mall': Mall.get_by_id(Floor.get_by_id(Parking.get_by_id(history.parking_id).floor_id).mall_id).outlet,
                    'floor': Floor.get_by_id(Parking.get_by_id(history.parking_id).floor_id).floor,
                    'parking': Parking.get_by_id(history.parking_id).parking_num,
                    'start': history.created_at,
                    'id': history.id
                }
                history_arr.append(history_list)

        responseObj= {
            'status': 'success',
            'history': history_arr 
        }

        return jsonify(responseObj), 200

    else: 
        responseObj = {
            'status': 'failed',
            'message': 'Failed to delete history!'
        
        }

        return jsonify(responseObj), 400

@features_api_blueprint.route('/find_my_car', methods = ['POST'])
@jwt_required
def find():
    user_id = get_jwt_identity()
    history = History.select().where(user_id == user_id).order_by(History.id.desc())
    
    if history: 
        latest = history[0]
        responseObj = {
            'status': 'success',
            'mall': Mall.get_by_id(Floor.get_by_id(Parking.get_by_id(latest.parking_id).floor_id).mall_id).outlet,
            'floor': Floor.get_by_id(Parking.get_by_id(latest.parking_id).floor_id).floor,
            'parking': Parking.get_by_id(latest.parking_id).parking_num,
            'start': latest.created_at,
            'id': latest.id
        }

        return jsonify(responseObj), 200

    else: 
        responseObj = {
            'status': 'failed',
            'message': 'Failed to retrieve information!'
        
        }

        return jsonify(responseObj), 400



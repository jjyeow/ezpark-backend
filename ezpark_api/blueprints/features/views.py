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
import nexmo
import os

features_api_blueprint = Blueprint('features_api',
                             __name__,
                             template_folder='templates')

client = nexmo.Client(key=os.environ.get('NEXMO_API_KEY'), secret=os.environ.get('NEXMO_API_SECRET'))

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
    history_obj = History.select().where(History.user_id == current_user.id).order_by(History.id.desc())
    history_arr = []

    if history_obj: 
        for history in history_obj: 
            history_list = {
                'mall': Mall.get_by_id(Floor.get_by_id(Parking.get_by_id(history.parking_id).floor_id).mall_id).outlet,
                'floor': Floor.get_by_id(Parking.get_by_id(history.parking_id).floor_id).floor,
                'parking': Parking.get_by_id(history.parking_id).parking_num,
                'date': history.created_at.strftime('%A %d %b %Y'),
                'time': history.created_at.strftime('%X %p'),
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


@features_api_blueprint.route('/history_add_multiple', methods=['POST'])
@jwt_required
def history_add_multiple():
    user_id = get_jwt_identity()
    parking_id = [1,2,3,4,5,6,7,8]

    for parking in parking_id: 
        history_inst = History(user_id = user_id, parking_id = parking)
        history_inst.save()
    
@features_api_blueprint.route('/history_add', methods = ['POST'])
@jwt_required
def history_add():
    user_id = get_jwt_identity()
    user_inst = User.get_by_id(user_id)
    parking_id = request.json.get('parking_id')
    parking_inst = Parking.get_by_id(parking_id)
    floor_inst = Floor.get_by_id(parking_inst.floor_id) 
    mall_inst = Mall.get_by_id(floor_inst.mall_id)
    history_inst = History(user_id = user_id, parking_id = parking_id)

    if history_inst.save():
        responseData = client.send_message({
            'from': 'Nexmo',
            'to': user_inst.hp_number, 
            'text': 'RM0.00 EzPark: Your car is parked in Mall: [' + mall_inst.outlet + '], at Floor: [' + floor_inst.floor +  '], in Parking Bay: [' + parking_inst.parking_num + ']///'
        })

        if responseData["messages"][0]["status"] == "0":
            responseObj = {
                'status': 'success',
                'message': 'Successfully saved your parking!'
            }
            return jsonify(responseObj), 200
        else: 
            responseObj = {
                'status': 'failed',
                'message': 'Message sent failed'
            }
            return jsonify(responseObj), 400

    else: 
        responseObj = {
                'status': 'failed',
                'message': 'Parking failed to save!'
        }

        return jsonify(responseObj), 400

@features_api_blueprint.route('/history_delete/<id>', methods=['POST'])
@jwt_required
def history_delete(id):
    user_id = get_jwt_identity()
    history = History.get_by_id(id)
    if history.delete_instance():
        history_obj = History.select().where(History.user_id == user_id)
        history_arr = []
        if history_obj: 
            for history in history_obj: 
                history_list = {
                    'mall': Mall.get_by_id(Floor.get_by_id(Parking.get_by_id(history.parking_id).floor_id).mall_id).outlet,
                    'floor': Floor.get_by_id(Parking.get_by_id(history.parking_id).floor_id).floor,
                    'parking': Parking.get_by_id(history.parking_id).parking_num,
                    'date': history.created_at.strftime('%A %d %b %Y'),
                    'time': history.created_at.strftime('%X %p'),
                    'id': history.id
                }
                history_arr.append(history_list)

        responseObj= {
            'status': 'success',
            'message': 'Successfully deleted parking history!',
            'history': history_arr 
        }

        return jsonify(responseObj), 200

    else: 
        responseObj = {
            'status': 'failed',
            'message': 'Failed to delete history!'
        
        }

        return jsonify(responseObj), 400

@features_api_blueprint.route('/find_my_car', methods = ['GET'])
@jwt_required
def find():
    user_id = get_jwt_identity()
    history = History.select().where(History.user_id == user_id).order_by(History.id.desc())
    
    if history: 
        latest = history[0]
        responseObj = {
            'status': 'success',
            'mall': Mall.get_by_id(Floor.get_by_id(Parking.get_by_id(latest.parking_id).floor_id).mall_id).outlet,
            'floor': Floor.get_by_id(Parking.get_by_id(latest.parking_id).floor_id).floor,
            'parking': Parking.get_by_id(latest.parking_id).parking_num,
            'date': latest.created_at.strftime('%A %d %b %Y'),
            'time': latest.created_at.strftime('%X %p'),
            'id': latest.id
        }

        return jsonify(responseObj), 200

    else: 
        responseObj = {
            'status': 'failed',
            'message': 'Failed to retrieve information!'
        
        }

        return jsonify(responseObj), 400

@features_api_blueprint.route('/layout', methods = ['POST'])
def layout():
    mall = request.json.get('mall')
    mall_inst = Mall.get_or_none(outlet = mall)
    floors = mall_inst.floor
    floor_arr = []
    for floor in floors: 
        floor_arr.append(floor.floor)

    if mall_inst: 
        responseObj = {
            'status': 'success',
            'mall': mall_inst.outlet,
            'id': mall_inst.id,
            'floor': floor_arr
        }

        return jsonify(responseObj), 200


    else: 
        responseObj = {
            'status': 'failed',
            'message': 'Failed to access the mall layout'
        }

        return jsonify(responseObj), 400

@features_api_blueprint.route('/layout/id', methods = ['POST'])
@jwt_required
def layout_id():
    user_id = get_jwt_identity()
    mall_id = request.json.get('mall_id')
    mall_inst = Mall.get_by_id(mall_id)
    floors = Floor.select().where(Floor.mall_id == mall_inst.id).order_by(Floor.id.asc())
    floor_arr = []
    parking_arr = []
    parking_arr1 = []
    parking_arr2 = []
    for floor in floors: 
        floor_arr.append(floor.floor)
        # for parking in floor.parking:
        #     parking_arr.append({"id": parking.id, "status": parking.status})
    floor1 = Floor.get_or_none(floor = floor_arr[0])
    floor2 = Floor.get_or_none(floor = floor_arr[1])
    parking1 = Parking.select().where(Parking.floor_id == floor1.id).order_by(Parking.id.asc())
    parking2 = Parking.select().where(Parking.floor_id == floor2.id).order_by(Parking.id.asc())

    for i in parking1:
        parking_arr1.append({"id": i.id, "status": i.status}) 

    for i in parking2:
        parking_arr2.append({"id": i.id, "status": i.status}) 

     

    if mall_inst: 
        responseObj = {
            'status': 'success',
            'user': user_id,
            'mall': mall_inst.outlet,
            'id': mall_inst.id,
            'floor': floor_arr,
            'parking1': parking_arr1,
            'parking2': parking_arr2
        }

        return jsonify(responseObj), 200


    else: 
        responseObj = {
            'status': 'failed',
            'message': 'Failed to access the mall layout'
        }

        return jsonify(responseObj), 400
    






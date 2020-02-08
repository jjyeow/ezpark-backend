from flask import Blueprint, request, json, jsonify
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
        malls_name_arr.append(mall.outlet)

    responseObj = {
        'status': 'success',
        'mall': malls_name_arr
    }

    return jsonify(responseObj), 200





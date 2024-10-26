from flask import Blueprint, jsonify,request, make_response
from components import db
import datetime
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

users_collection = db.users  # Collection name

sign = Blueprint('sign', __name__)



@sign.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()  # Get JSON data from the request
    users_collection.insert_one(data)  # Insert the user into the collection
    return jsonify({"message": "User added successfully!"}), 201

@sign.route('/signin', methods=['POST'])
def signin():
    auth = request.get_json()
    print(auth)
    email = auth['email']
    password = auth['password']
    # data = request.get_json()
    user = users_collection.find_one(auth)
    if user:
        access_token = create_access_token(identity=email, expires_delta=datetime.timedelta(min==45))
        refresh_token = create_refresh_token(identity=email)
        return jsonify(access_token=access_token, refresh_token=refresh_token , message="sign-in done"), 200
    else:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})
    

@sign.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)  # Requires a valid refresh token
def refresh():
    identity = get_jwt_identity()  # Get the user identity from the refresh token
    print('identity: ', identity)
    new_access_token = create_access_token(identity=identity)  # Create a new access token
    return jsonify({
        "access_token": new_access_token
    }), 200
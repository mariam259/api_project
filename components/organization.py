from flask import Blueprint, jsonify,request
from components import db
# import datetime
import uuid
from flask_jwt_extended import jwt_required, get_jwt_identity

organization_collection = db.organization  # Collection name
organization = Blueprint('organization', __name__)

@organization.route('/organization', methods=['POST'])
@jwt_required()
def add_organization():
    # print('organization_id: ', organization_id)
    identity = get_jwt_identity()
    # if request.method == 'GET':
    #     organizations = list(organization_collection.find({"user_id": identity}, {"organization_id": organization_id}))
    #     return jsonify(organizations), 200
    # else:
        # identity = get_jwt_identity()
    data = request.get_json()
    if data is None:
        return jsonify({"message": "No data provided"}), 400
    organization_name = data['name']
    organization_description = data['description']
    organization_id = str(uuid.uuid4())
    organization_collection.insert_one({"organization_id": organization_id, "organization_name": organization_name, "organization_description": organization_description, "user_id": identity})
    return jsonify({"organization_id": organization_id}), 201

@organization.route('/organization/<string:organization_id>', methods=['GET'])
@jwt_required()
def get_organization(organization_id):
    print('organization_id: ', organization_id)
    identity = get_jwt_identity()
    organizations = organization_collection.find_one({"organization_id": organization_id})
    print('organizations: ', organizations)
    if organizations:
        organizations['_id'] = str(organizations['_id'])
        return jsonify(organizations), 200
        # return jsonify({"organization": "found"}), 200
    else:
        return jsonify({"message": "Organization not found"}), 404
    
@organization.route('/organization', methods=['GET'])
@jwt_required()
def get_organizations():
    # identity = get_jwt_identity()
    organizations = list(organization_collection.find())
    for organization in organizations:
        organization['_id'] = str(organization['_id'])
    return jsonify(organizations), 200

@organization.route('/organization/<string:organization_id>', methods=['PUT'])
@jwt_required()
def update_organization(organization_id):
    # identity = get_jwt_identity()
    data = request.get_json()
    new_name = data['name']
    new_description = data['description']
    organization_collection.update_one({"organization_id": organization_id}, {"$set": {"organization_name": new_name, "organization_description": new_description}})
    return jsonify({"organization_id": organization_id , "name": new_name, "description":new_description}), 200

@organization.route('/organization/<string:organization_id>', methods=['DELETE'])
@jwt_required()
def delete_organization(organization_id):
    # identity = get_jwt_identity()
    organization_collection.delete_one({"organization_id": organization_id})
    return jsonify({"message": "orgaization has been deleted"}), 200


invitations = []  # Collection name
@organization.route('/organization/<string:organization_id>/invite', methods=['POST'])
@jwt_required()
def invite_user(organization_id):
    identity = get_jwt_identity()
    data = request.get_json()
    email = data['email']
    organization = organization_collection.find_one({"organization_id": organization_id})
    if organization:
        # can use service like sendgrid to send email
        invitations.append({"email": email, "organization_id": organization_id , "invited_by": identity})
        return jsonify({"message": "User has been invited"}), 200
    else:
        return jsonify({"message": "Organization not found"}), 404
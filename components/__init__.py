from flask import Flask
from pymongo import MongoClient
from flask_jwt_extended import JWTManager
import datetime

# Create the Flask app
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'MARIAMJWTSECRETKEY'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(minutes=15)  # Access token validity
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = datetime.timedelta(days=7)  # Refresh token validity

jwt = JWTManager(app)
# MongoDB Atlas connection string
client = MongoClient("mongodb+srv://mariam:api_project_mariam@cluster0.a44bp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# Select the database and collection
db = client.apiProject  # Database name

from components.sign import sign
app.register_blueprint(sign)

from components.organization import organization
app.register_blueprint(organization)

# Route to insert a new user
# @app.route('/add_user', methods=['POST'])
# def add_user():
#     data = request.json  # Get JSON data from the request
#     users_collection.insert_one(data)  # Insert the user into the collection
#     return jsonify({"message": "User added successfully!"}), 201

# Route to retrieve all users
# @app.route('/users', methods=['GET'])
# def get_users():
#     users = list(users_collection.find({}, {"_id": 0}))  # Retrieve all users
#     return jsonify(users), 200
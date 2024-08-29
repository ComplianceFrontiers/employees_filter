from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
from pymongo import DESCENDING, MongoClient, ReturnDocument
from dotenv import load_dotenv
import os

MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 1

app = Flask(__name__)

# Allow requests from specific origins
CORS(app, origins=["https://chess-main.vercel.app","https://chessdemo-alpha.vercel.app","https://chessdemo-l3qrzgj5q-ramyas-projects-4cb2348e.vercel.app","https://chess-main-git-main-ramyas-projects-4cb2348e.vercel.app","http://localhost:3000"])

load_dotenv()

# Get the MongoDB URI from the environment variable
mongo_uri = os.getenv('MONGO_URI')

# MongoDB setup
client = MongoClient(mongo_uri)
db = client.company_db
users_collection = db.employees

@app.route('/')
def home():
    return "Hello, Flask on Vercel!"

@app.route('/filter', methods=['GET'])
def filter_records():
    query = {}

    # Extracting query parameters from the request
    if 'Name' in request.args:
        query['Name'] = request.args.get('Name')
    if 'Gender' in request.args:
        query['Gender'] = request.args.get('Gender')
    if 'Dob' in request.args:
        try:
            dob = datetime.strptime(request.args.get('Dob'), '%d-%b-%y')
            query['Dob'] = dob.strftime('%d-%b-%y')
        except ValueError:
            return jsonify({'error': 'Invalid Dob format. Use DD-MMM-YY format.'}), 400
    if 'Doj' in request.args:
        try:
            doj = datetime.strptime(request.args.get('Doj'), '%d-%b-%y')
            query['Doj'] = doj.strftime('%d-%b-%y')
        except ValueError:
            return jsonify({'error': 'Invalid Doj format. Use DD-MMM-YY format.'}), 400
    if 'Pan' in request.args:
        query['Pan'] = request.args.get('Pan')
    if 'Aadhar' in request.args:
        query['Aadhar'] = request.args.get('Aadhar')
    if 'Uan' in request.args:
        query['Uan'] = int(request.args.get('Uan'))
    if 'Member ID' in request.args:
        query['Member ID'] = request.args.get('Member ID')
    if "Father's/Husband's Name" in request.args:
        query["Father's/Husband's Name"] = request.args.get("Father's/Husband's Name")
    if 'Relation' in request.args:
        query['Relation'] = request.args.get('Relation')
    if 'Marital Status' in request.args:
        query['Marital Status'] = request.args.get('Marital Status')
    if 'Mobile' in request.args:
        query['Mobile'] = int(request.args.get('Mobile'))
    if 'Email ID' in request.args:
        query['Email ID'] = request.args.get('Email ID')
    if 'Bank' in request.args:
        query['Bank'] = request.args.get('Bank')
    if 'Nomination' in request.args:
        query['Nomination'] = request.args.get('Nomination')

    try:
        # Fetching records based on the query
        results = list(users_collection.find(query))
        # Convert ObjectId to string for JSON serialization
        for result in results:
            result['_id'] = str(result['_id'])

        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)


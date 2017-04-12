from flask import Flask, request, Response
import db
import json
import string
import random
from werkzeug.utils import secure_filename
import os
import base64
import data_utils
UPLOAD_FOLDER = 'Uploads/'
app = Flask(__name__)
randomsecretkey = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(50))
app.secret_key = randomsecretkey
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.after_request
def apply_caching(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/')
def home():
    return 'API home screen'


@app.route('/getLifts', methods=['PUT', 'POST'])
def main_page_lifts():
    if request.method == 'POST':
        data = request.get_data()
        d = json.loads(data.decode('UTF-8'))
        js_obj = db.get_main_page_lifts(d['passengerID'])
        return js_obj


@app.route('/availableLifts', methods=['PUT', 'POST'])
def available_lifts():
    if request.method == 'POST':
        data = request.get_data()
        d = json.loads(data.decode('UTF-8'))
        js_obj = db.list_available_lifts(d['passengerID'])
        return js_obj


@app.route('/liftDetails', methods=['PUT', 'POST'])
def lift_details():
    if request.method == 'POST':
        data = request.get_data()
        j = json.loads(data.decode('UTF-8'))
        js_obj = db.getLiftDetails(j['liftID'], j['driverID'])
        return js_obj


@app.route('/registeruser', methods=['PUT', 'POST'])
def registeruser():
    filename = ""
    if request.method == 'POST':
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        email = request.form['email']
        phonenum = request.form['phoneNum']
        password = request.form['password']
        file = request.files['file']
        if file:
            basedir = os.path.abspath(os.path.dirname(__file__))
            filename = secure_filename(email + '.jpg')
            file.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
        js_obj = db.register(first_name, last_name, email, phonenum, password, filename)
        return js_obj
    else:
        return 'POST did not work'


@app.route('/registercar', methods=['PUT', 'POST'])
def register_car():
    if request.method == 'POST':
        user_id = request.form['userID']
        car_make = request.form['carMake']
        car_model = request.form['carModel']
        reg_num = request.form['regNum']
        if car_make is '' or car_model is '' or reg_num is '':
            js_obj = json.dumps({"status": "Not all required elements are entered"})
            return js_obj
        else:
            js_obj = db.register_car_and_driver(user_id, car_make, car_model, reg_num)
            return js_obj


@app.route('/loginuser', methods=['PUT', 'POST'])
def login():
    if request.method == 'POST':
        data = db.process_login(request.form['email_login'], request.form['password_login'])
        return data


@app.route('/logoutuser', methods=['PUT', 'POST'])
def logout():
    if request.method == 'POST':
        data = db.process_logout(request.form['userID'])
        return data


@app.route('/offerLift', methods=['POST'])
def sub_offer_lift():
    if request.method == 'POST':
        data = request.get_json()
        js_obj = db.register_offer_lift(data['userID'], data['start_lat'],data['start_long'], data['start_county'],
                                        data['destination_lat'], data['destination_long'], data['destination_county'],
                                        data['distance'], data['departing'], data['seats'])
        return js_obj


@app.route('/checkcarregistered', methods=['PUT','POST'])
def check_user_registered_car():
    if request.method == 'POST':
        data = request.get_json()
        js_obj = db.check_if_car_exists(data['userid'])
        return js_obj


#     REQUESTS


@app.route('/myRequests', methods=['PUT', 'POST'])
def my_requests():
    if request.method == 'POST':
        js_obj = db.get_my_requests(request.form['userID'])
        return js_obj


@app.route('/requestDetails', methods=['PUT', 'POST'])
def request_details():
    if request.method == 'POST':
        data = request.get_data()
        j = json.loads(data.decode('UTF-8'))
        js_obj = db.get_request_details(j['requestID'])
        return js_obj


@app.route('/requestLift', methods=['PUT', 'POST'])
def request_lift():
    if request.method == 'POST':
        data = db.process_request(request.form['liftID'], request.form['passengerID'])
        return data


@app.route('/availableRequests', methods=['PUT', 'POST'])
def available_requests():
    if request.method == 'POST':
        js_obj = db.list_user_requests(request.form['userID'])
        return js_obj


@app.route('/acceptRequest', methods=['PUT','POST'])
def accept_request():
    if request.method == 'POST':
        js_obj = db.accept_request(request.form['requestID'])
        return js_obj


@app.route('/denyRequest', methods=['PUT', 'POST'])
def deny_request():
    if request.method == 'POST':
        js_obj = db.deny_request(request.form['requestID'])
        return js_obj


# MY GROUPS
@app.route('/myGroups', methods=['PUT', 'POST'])
def my_groups():
    if request.method == 'POST':
        js_obj = db.get_my_groups(request.form['userID'])
        return js_obj


@app.route('/groupDetails', methods=['PUT', 'POST'])
def group_details():
    if request.method == 'POST':
        data = request.get_data()
        j = json.loads(data.decode('UTF-8'))
        js_obj = db.get_group_details(j['liftID'], j['groupID'])
        return js_obj


@app.route('/myCompletedGroups', methods=['PUT', 'POST'])
def my_completed_groups():
    if request.method == 'POST':
        js_obj = db.get_my_completed_groups(request.form['userID'])
        return js_obj

# MY LIFTS


@app.route('/myCompletedLifts', methods=['PUT', 'POST'])
def my_completed_lifts():
    if request.method == 'POST':
        js_obj = db.get_my_completed_lifts(request.form['userID'])
        return js_obj


@app.route('/myLifts', methods=['PUT', 'POST'])
def my_lifts():
    if request.method == 'POST':
        js_obj = db.get_my_lifts(request.form['userID'])
        return js_obj


@app.route('/myLiftDetails', methods=['PUT', 'POST'])
def my_lift_details():
    if request.method == 'POST':
        data = request.get_data()
        j = json.loads(data.decode('UTF-8'))
        js_obj = db.get_my_lift_details(j['liftID'])
        return js_obj


@app.route('/checkIfCanDeleteLift', methods=['PUT', 'POST'])
def check_if_can_delete():
    if request.method == 'POST':
        data = request.get_data()
        j = json.loads(data.decode('UTF-8'))
        js_obj = db.check_can_delete(j['liftID'])
        return js_obj


@app.route('/deleteLift', methods=['PUT', 'POST'])
def deletelift():
    if request.method == 'POST':
        data = request.get_data()
        j = json.loads(data.decode('UTF-8'))
        js_obj = db.delete_lift(j['liftID'])
        return js_obj


@app.route('/completeLift', methods=['PUT', 'POST'])
def complete_lift():
    if request.method == 'POST':
        data = request.get_data()
        j = json.loads(data.decode('UTF-8'))
        js_obj = db.complete_lift(j['liftID'])
        return js_obj


# FINISH LIFT
@app.route('/rateUsers', methods=['PUT', 'POST'])
def rate_users():
    if request.method == 'POST':
        data = request.get_data()
        j = json.loads(data.decode('UTF-8'))
        js_obj = db.rate_group(j['driverID'], j['driverRating'], j['passengerData'])
        return js_obj


@app.route('/checkIfDriver', methods=['PUT', 'POST'])
def check_if_driver():
    if request.method == 'POST':
        data = request.get_data()
        j = json.loads(data.decode('UTF-8'))
        js_obj = db.check_if_user_is_driver(j['liftID'], j['driverID'])
        return js_obj


@app.route('/getExperience', methods=['PUT', 'POST'])
def get_experience():
    if request.method == 'POST':
        data = request.get_data()
        j = json.loads(data.decode('UTF-8'))
        js_obj = db.get_user_experience(j['userID'], j['newExp'], j['distance'], j['numOfPassengers'])
        return js_obj


@app.route('/populateRatingTables', methods=['PUT', 'POST'])
def populate_ratings_table():
    if request.method == 'POST':
        data = request.get_data()
        j = json.loads(data.decode('UTF-8'))
        js_obj = db.pop_ratings_table(j['liftID'], j['userID'])
        return js_obj


# ACTIVE LIFT
@app.route('/getDriver', methods=['PUT', 'POST'])
def get_driver():
    if request.method == 'POST':
        data = request.get_data()
        j = json.loads(data.decode('UTF-8'))
        js_obj = db.get_driver_id(j['liftID'])
        return js_obj


@app.route('/checkIfLiftFinished', methods=['PUT', 'POST'])
def check_if_lift_finished():
    if request.method == 'POST':
        data = request.get_data()
        j = json.loads(data.decode('UTF-8'))
        js_obj = db.check_if_lift_finished(j['liftID'])
        return js_obj


# PROFILE
@app.route('/profile', methods=['PUT', 'POST'])
def user_profile():
    if request.method == 'POST':
        data = request.get_data()
        j = json.loads(data.decode('UTF-8'))
        js_obj = db.get_profile(j['userID'])
        return js_obj


@app.route('/getPicture', methods=['POST', 'PUT'])
def get_profile_picture():
    if request.method == 'POST':
        data = request.get_data()
        j = json.loads(data.decode('UTF-8'))
        filename = db.get_picture(j['userID'])
        basedir = os.path.abspath(os.path.dirname(__file__))
        filepath = os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename)
        with open(filepath, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        return Response(encoded_string, mimetype='image/jpeg', headers={
            "Content-disposition": "attachment: filename="+filepath})


@app.route('/getUserID', methods=['PUT', 'POST'])
def get_user():
    if request.method == 'POST':
        data = request.get_data()
        j = json.loads(data.decode('UTF-8'))
        js_obj = db.get_user_id(j['passengerID'])
        return js_obj


@app.route('/updateInfo', methods=['PUT', 'POST'])
def update_info():
    if request.method == 'POST':
        user_id = request.form['userID']
        phone = request.form['phone']
        email = request.form['email']
        car_make = request.form['carMake']
        car_model = request.form['carModel']
        car_reg = request.form['carReg']
        file = request.files['file']
        if file:
            data_utils.delete_item(email)
            basedir = os.path.abspath(os.path.dirname(__file__))
            filename = secure_filename(email + '.jpg')
            file.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
        js_obj = db.update_details(user_id, phone, car_make, car_model, car_reg)
        return js_obj


@app.route('/leaderboard', methods=['PUT', 'POST'])
def leaderboard():
    if request.method == 'POST':
        js_obj = db.get_leaderboard()
        return js_obj


@app.route('/deleteAccount', methods=['PUT', 'POST'])
def delete_account():
    if request.method == 'POST':
        data = request.get_data()
        j = json.loads(data.decode('UTF-8'))
        js_obj = db.delete_user_account(j['userID'])
        return js_obj


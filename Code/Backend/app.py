from flask import Flask, request, Response, make_response, render_template
import db
import json
import string
import random
from werkzeug.utils import secure_filename
import os
import base64


UPLOAD_FOLDER = 'Uploads/'

app = Flask(__name__)
randomsecretkey = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(50))
app.secret_key = randomsecretkey

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.after_request
def apply_caching(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    # response.addHeader("Access-Control-Allow-Origin", "*")
    return response


@app.route('/')
def home():
    return 'API home screen'


@app.route('/getLifts', methods=['PUT', 'POST'])
def main_page_lifts():
    if request.method == 'POST':
        data = request.get_data()
        d = json.loads(data.decode('UTF-8'))
        jsObj = db.get_main_page_lifts(d['passengerID'])
        print('jsobj', jsObj)
        return jsObj

# TRY REMOVING GET TO FIX ACCESS CONTROL ERRORS
@app.route('/availableLifts', methods=['PUT', 'POST'])
def available_lifts():
    # request.headers['Access-Control-Allow-Origin'] = '*'
    if request.method == 'POST':
        data = request.get_data()
        d = json.loads(data.decode('UTF-8'))
        jsObj = db.list_available_lifts(d['passengerID'])
        print('returning obj', jsObj)
        print('after function')
        return jsObj


@app.route('/liftDetails', methods=['PUT', 'POST'])
def liftDetails():
    print('lift details func')
    if request.method == 'POST':
        data = request.get_data()
        print(type(data))
        print(data)
        j = json.loads(data.decode('UTF-8'))
        print('j', j, 'type', type(j))
        liftID = j['liftID']
        driverID = j['driverID']
        print('lift and driver id ', liftID, driverID)
        jsObj = db.getLiftDetails(liftID, driverID)
        return jsObj





@app.route('/registeruser', methods=['PUT', 'POST'])
def registeruser():
    filename =""
    if request.method == 'POST':
        try:
            print('method == POST')
            # jsObj = {}
            first_name = request.form['firstName']
            last_name = request.form['lastName']
            email = request.form['email']
            phonenum = request.form['phoneNum']
            password = request.form['password']
            file = request.files['file']
            # if first_name is '' or last_name is '' or email is '' or phonenum is 0 or password is '':
            #     jsObj = json.dumps({"status": "Not all required elements are entered"})
            #     return jsObj
            # else:
            print('app going to register function')
            if file:
                print('in file if statement')
                basedir = os.path.abspath(os.path.dirname(__file__))
                filename = secure_filename(email + '.jpg')
                file.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
                filepath = os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename)
            jsObj = db.register(first_name, last_name, email, phonenum, password, filename)
            return jsObj
        except Exception as e:
            print('Error registering user:', e )
    else:
        return 'POST did not work'


@app.route('/registercar', methods=['PUT','POST'])
def registerCar():
    if request.method == 'POST':
        userID = request.form['userID']
        carMake = request.form['carMake']
        carModel = request.form['carModel']
        regNum = request.form['regNum']
        if carMake is '' or carModel is '' or regNum is '':
            jsObj = json.dumps({"status": "Not all required elements are entered"})
            return jsObj
        else:
            jsObj = db.registerCarAndDriver(userID, carMake, carModel, regNum)
            return jsObj


@app.route('/loginuser', methods=['PUT', 'POST'])
def login():
    if request.method == 'POST':
        data = db.process_login(request.form['email_login'], request.form['password_login'])
        print('after process login', data )
        return data


@app.route('/logoutuser', methods=['PUT', 'POST'])
def logout():
    print('logout function')
    if request.method == 'POST':
        userID = request.form['userID']
        data = db.process_logout(userID)
        return data


@app.route('/offerLift', methods=['POST'])
def sub_offer_lift():
    if request.method == 'POST':
        data = request.get_json()
        userID = data['userID']
        startLat = data['start_lat']
        startLong = data['start_long']
        startCounty = data['start_county']
        destinationLat = data['destination_lat']
        destinationLong = data['destination_long']
        destinationCounty = data['destination_county']
        distance = data['distance']
        departing = data['departing']
        seats = data['seats']
        print('recieved: ', userID, startLat, startLong, startCounty, destinationLat, destinationLong,
              destinationCounty, ' distance', distance, departing, seats)

        jsObj = db.register_offer_lift(userID,startLat,startLong, startCounty, destinationLat, destinationLong,
                                       destinationCounty, distance, departing, seats)
        return jsObj


@app.route('/checkcarregistered', methods=['PUT','POST'])
def check_user_registered_car():
    print('check car reg function, before')
    if request.method == 'POST':
        print('before request')
        data = request.get_json()
        print('data', data)
        userID = data['userid']
        print('checking for car', userID)
        jsObj = db.checkIfCarExists(userID)
        return jsObj


#     REQUESTS


@app.route('/myRequests', methods=['PUT', 'POST'])
def myRequests():
    print('my requests func')
    if request.method == 'POST':
        userID = request.form['userID']
        print('data', userID)
        jsObj = db.getMyRequests(userID)
        return jsObj


@app.route('/requestDetails', methods=['PUT', 'POST'])
def requestDetails():
    print('request details func')
    if request.method == 'POST':
        data = request.get_data()
        print('data', data)
        j = json.loads(data.decode('UTF-8'))
        jsObj = db.getRequestDetails(j['requestID'])
        print('js obj', jsObj)
        return jsObj


@app.route('/requestLift', methods=['PUT', 'POST'])
def requestLift():
    print('request lift funct')
    if request.method == 'POST':
        print('in if statement')
        liftID = request.form['liftID']
        passengerID = request.form['passengerID']
        print(liftID, passengerID)
        print('lift: ', liftID, 'passenger:',passengerID)
        data = db.process_request(liftID, passengerID)
        return data


@app.route('/availableRequests', methods=['PUT', 'POST'])
def available_requests():
    print('available requests ')
    if request.method == 'POST':
        userID = request.form['userID']
        print('userID', userID)
        jsObj = db.list_user_requests(userID)
        print('returning obj', jsObj)
        return jsObj


@app.route('/acceptRequest', methods=['PUT','POST'])
def accept_request():
    print('accept request func')
    if request.method == 'POST':
        jsObj = db.acceptRequest(request.form['requestID'])
        print('jsObj', jsObj)
        return jsObj


@app.route('/denyRequest', methods=['PUT', 'POST'])
def deny_request():
    print('deny request func')
    if request.method == 'POST':
        jsObj = db.denyRequest(request.form['requestID'])
        print('jsobj', jsObj)
        return jsObj


# MY GROUPS
@app.route('/myGroups', methods=['PUT', 'POST'])
def my_groups():
    print('my groups func')
    if request.method == 'POST':
        userID = request.form['userID']
        print('userid', userID)
        jsObj = db.getMyGroups(userID)
        print('jsObj', jsObj)
        return jsObj


@app.route('/groupDetails', methods=['PUT', 'POST'])
def group_details():
    print('group details func')
    if request.method == 'POST':
        data = request.get_data()
        j = json.loads(data.decode('UTF-8'))
        jsObj = db.getGroupDetails(j['liftID'], j['groupID'])
        print(jsObj)
        return jsObj


@app.route('/myCompletedGroups', methods=['PUT', 'POST'])
def my_completed_groups():
    if request.method == 'POST':
        jsObj = db.get_my_completed_groups(request.form['userID'])
        print('jsobj', jsObj)
        return jsObj

# MY LIFTS


@app.route('/myCompletedLifts', methods=['PUT', 'POST'])
def my_completed_lifts():
    if request.method == 'POST':
        jsObj = db.getMyCompletedLifts(request.form['userID'])
        print('jsobj', jsObj)
        return jsObj


@app.route('/myLifts', methods=['PUT', 'POST'])
def my_lifts():
    print('my lifts function')
    if request.method == 'POST':
        jsObj = db.getMyLifts(request.form['userID'])
        print('jsobj', jsObj)
        return jsObj


@app.route('/myLiftDetails', methods=['PUT', 'POST'])
def my_lift_details():
    print('my lift details')
    if request.method == 'POST':
        data = request.get_data()
        j = json.loads(data.decode('UTF-8'))
        jsObj = db.getMyLiftDetails(j['liftID'])
        print(jsObj)
        return jsObj


@app.route('/completeLift', methods=['PUT', 'POST'])
def complete_lift():
    if request.method == 'POST':
        data = request.get_data()
        j = json.loads(data.decode('UTF-8'))
        jsObj = db.complete_lift(j['liftID'])
        print(jsObj)
        return jsObj


# FINISH LIFT
@app.route('/rateUsers', methods=['PUT', 'POST'])
def rate_users():
    if request.method == 'POST':
        data = request.get_data()
        j = json.loads(data.decode('UTF-8'))
        print('j', j)
        jsObj = db.rate_group(j['driverID'], j['driverRating'], j['passengerData'])
        return jsObj


@app.route('/checkIfDriver', methods=['PUT', 'POST'])
def check_if_driver():
    if request.method == 'POST':
        data = request.get_data()
        j = json.loads(data.decode('UTF-8'))
        print('j', j)
        jsObj = db.check_if_user_is_driver(j['liftID'], j['driverID'])
        return jsObj


@app.route('/getExperience', methods=['PUT', 'POST'])
def get_experience():
    if request.method == 'POST':
        data = request.get_data()
        j = json.loads(data.decode('UTF-8'))
        print('j', j)
        jsObj = db.get_user_experience(j['userID'], j['newExp'], j['distance'], j['numOfPassengers'])
        return jsObj


@app.route('/populateRatingTables', methods=['PUT', 'POST'])
def populate_ratings_table():
    if request.method == 'POST':
        data = request.get_data()
        j = json.loads(data.decode('UTF-8'))
        print('j', j)
        jsObj = db.pop_ratings_table(j['liftID'], j['userID'])
        return jsObj


# ACTIVE LIFT
@app.route('/getDriver', methods=['PUT', 'POST'])
def get_driver():
    if request.method == 'POST':
        data = request.get_data()
        j = json.loads(data.decode('UTF-8'))
        jsObj = db.get_driver_id(j['liftID'])
        return jsObj


@app.route('/checkIfLiftFinished', methods=['PUT', 'POST'])
def check_if_lift_finished():
    if request.method == 'POST':
        data = request.get_data()
        j = json.loads(data.decode('UTF-8'))
        jsObj = db.check_if_lift_finished(j['liftID'])
        return jsObj


# PROFILE
@app.route('/profile', methods=['PUT', 'POST'])
def user_profile():
    if request.method == 'POST':
        data = request.get_data()
        j = json.loads(data.decode('UTF-8'))
        jsObj = db.get_profile(j['userID'])
        return jsObj


@app.route('/getPicture', methods=['POST', 'PUT'])
def get_profile_picture():
    if request.method == 'POST':
        try:
            data = request.get_data()
            j = json.loads(data.decode('UTF-8'))
            filename = db.get_picture(j['userID'])
            print('path', filename)
            basedir = os.path.abspath(os.path.dirname(__file__))
            filepath = os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename)
            with open(filepath, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
            return Response(encoded_string, mimetype='image/jpeg', headers={"Content-disposition":"attachment: filename="+filepath})
        except Exception as e:
            print('Error sending picture:', e)


@app.route('/getUserID', methods=['PUT', 'POST'])
def get_user():
    if request.method == 'POST':
        data = request.get_data()
        j = json.loads(data.decode('UTF-8'))
        jsObj = db.get_user_id(j['passengerID'])
        return jsObj


@app.route('/updateInfo', methods=['PUT', 'POST'])
def update_info():
    print('in update func')
    if request.method == 'POST':
        user_id = request.form['userID']
        phone = request.form['phone']
        email = request.form['email']
        print('before cars')
        car_make = request.form['carMake']
        car_model = request.form['carModel']
        car_reg = request.form['carReg']
        print('before getting file')
        file = request.files['file']
        print('after file')
        if file:
            print('in file if')
            delete_item(email)
            print('in file if statement')
            basedir = os.path.abspath(os.path.dirname(__file__))
            filename = secure_filename(email + '.jpg')
            file.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
            # filepath = os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename)
        jsObj = db.update_details(user_id, phone, car_make, car_model, car_reg)
        print(jsObj)
        return jsObj


@app.route('/leaderboard', methods=['PUT', 'POST'])
def leaderboard():
    # r = make_response(render_template('base.html'))
    # r.headers['Access-Control-Allow-Origin'] = '*'
    if request.method == 'POST':
        jsObj = db.get_leaderboard()
        print(jsObj)
        return jsObj


def delete_item(email):
    try:
        basedir = os.path.abspath(os.path.dirname(__file__))
        filename = secure_filename(email + '.jpg')
        os.remove(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
    except Exception as e:
        print('Error deleting image from server:', e)
    return 'done'




if __name__ == '__main__':
    app.run(debug=True)


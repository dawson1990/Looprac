from flask import Flask, render_template, make_response, request, session
import db
import json
import string
import random


UPLOAD_FOLDER = '/home/looprac/LoopracAPI/Uploads/'

app = Flask(__name__)
randomsecretkey = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(50))
# app.secret_key = 'fhdgsd;ohfnvervneroigerrenverbner32hrjegb/kjbvr/o'
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


# @app.route('/availableLifts', methods=['PUT', 'POST'])
# def availableLifts():
#     r = make_response(render_template('base.html'))
#     r.headers['Access-Control-Allow-Origin'] = '*'
#     print('available lifts start')
#     if request.method == 'POST':
#         jsObj = db.list_available_lifts()
#         print('after function')
#         return jsObj
#     else:
#         'post did not work'
#


@app.route('/availableLifts', methods=['PUT', 'POST', 'GET'])
def available_lifts():
    r = make_response(render_template('base.html'))
    r.headers['Access-Control-Allow-Origin'] = '*'
    if request.method == 'GET':
        jsObj = db.list_available_lifts()
        print('after function')
        return jsObj


@app.route('/liftDetails', methods=['PUT','POST'])
def liftDetails():
    print('lift details func')
    r = make_response(render_template('base.html'))
    r.headers['Access-Control-Allow-Origin'] = '*'
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
    if request.method == 'POST':
        print('method == POST')
        # jsObj = {}
        fname = request.form['firstName']
        lname = request.form['lastName']
        email = request.form['email']
        phonenum = request.form['phoneNum']
        password = request.form['password']

        if fname is '' or lname is '' or email is '' or phonenum is 0 or password is '':
            jsObj = json.dumps({"status": "Not all required elements are entered"})
            return jsObj
        else:
            print('app going to register function')
            jsObj = db.register(fname, lname, email, phonenum, password)
            return jsObj
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
    print('start of check_email')
    if request.method == 'POST':
        print('method = post')
        email = request.form['email_login']
        password = request.form['password_login']
        data = db.process_login(email, password)
        print('after process login', data )
        return data


@app.route('/logoutuser', methods=['PUT', 'POST'])
def logout():
    print('logout function')
    if request.method == 'POST':
        userID = request.form['userID']
        data = db.process_logout(userID)
        return data

# @app.route('/checkifemailexists', methods=['POST'])
# def check_if_email_exists():
#     print('start of if email exists')
#     if request.method == 'POST':
#         email = request.get_data('data1')
#         print('email', email)
#         return db.check_if_exists(email)


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
        date = data['depart_date']
        time = data['depart_time']
        returnDate = data['return_date']
        returnTime = data['return_time']
        journey_type = data['type']
        seats = data['seats']
        print('recieved: ', userID, startLat, startLong, startCounty, destinationLat, destinationLong,
              destinationCounty, date, time, returnDate, returnTime, journey_type, seats)
        if startLat is '' or destinationLat is '' or date is '' or time is '':
            jsObj = json.dumps({"status": "Not all required elements are entered"})
            return jsObj
        else:
            jsObj = db.register_offer_lift(userID,startLat,startLong, startCounty, destinationLat, destinationLong,
                                           destinationCounty, date, time, returnDate, returnTime,  journey_type, seats)
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

if __name__ == '__main__':
    app.run(debug=True)


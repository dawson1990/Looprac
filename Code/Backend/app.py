from flask import Flask, render_template, make_response, request, session
import db
import json


UPLOAD_FOLDER = '/home/looprac/LoopracAPI/Uploads/'

app = Flask(__name__)
app.secret_key = 'fhdgsd;ohfnvervneroigerrenverbner32hrjegb/kjbvr/o'
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
        print('method == POST')
        jsObj = db.list_available_lifts()
        print('after function')
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
            jsObj = db.registerCar(userID, carMake, carModel, regNum)
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


@app.route('/checkifemailexists', methods=['POST'])
def check_if_email_exists():
    print('start of if email exists')
    if request.method == 'POST':
        email = request.get_data('data1')
        print('email', email)
        return db.check_if_exists(email)


@app.route('/offerLift', methods=['POST'])
def sub_offer_lift():
    if request.method == 'POST':
        # userID = request.form['userID']
        # startLat = request.form['latitude']
        # startLong = request.form['longitude']
        # destinationLat = request.form['destinationLatitude']
        # destinationLong = request.form['destinationLongitude']
        # date = request.form['departDate']
        # print(date)
        # time = request.form['departTime']
        # print(time)
        # journey_type = request.form['liftType']
        # seats = request.form['seats']
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
        journey_type = data['type']
        seats = data['seats']
        print('recieved: ', userID, startLat, startLong, startCounty, destinationLat, destinationLong,
              destinationCounty, date, time, journey_type, seats)
        if startLat is '' or destinationLat is '' or date is '' or time is '':
            jsObj = json.dumps({"status": "Not all required elements are entered"})
            return jsObj
        else:
            jsObj = db.register_offer_lift(userID,startLat,startLong, startCounty, destinationLat, destinationLong,
                                           startCounty, date, time,  journey_type, seats)
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

if __name__ == '__main__':
    app.run(debug=True)


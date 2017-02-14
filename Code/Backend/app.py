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
    return response


@app.route('/')
def home():
    return 'API home screen'


@app.route('/availableLifts')
def availableLifts():
    r = make_response(render_template('base.html'))
    r.headers['Access-Control-Allow-Origin'] = '*'
    availableLiftsList = db.list_available_lifts()
    json_str = json.dumps(availableLiftsList)
    parsed_json = json.loads(json_str)
    return parsed_json


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
        start = request.form['start']
        destination = request.form['destination']
        date = request.form['departDate']
        time = request.form['departTime']
        journey_type = request.form['liftType']
        seats = request.form['seats']
        if start is '' or destination is '' or date is '' or time is '':
            jsObj = json.dumps({"status": "Not all required elements are entered"})
            return jsObj
        else:
            jsObj = db.register_offer_lift(start, destination, date, time,  journey_type, seats)
            return jsObj


@app.route('/checkcarregistered', methods=['PUT','POST'])
def check_user_registered_car():
    print('check car reg function, before')
    if request.method == 'POST':
        print('before request')
        data = request.get_json()
        userID = data['userID']
        print('checking for car', userID)
        db.is_car_registered(userID)
    return 'done'

if __name__ == '__main__':
    app.run(debug=True)


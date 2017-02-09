from flask import Flask, render_template, make_response, request
import db
import json
import datetime


app = Flask(__name__)
app.secret_key = 'fhdgsd;ohfnvervneroigerrenverbner32hrjegb/kjbvr/o'


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


# try without put
@app.route('/registeruser', methods=['PUT', 'POST'])
def registeruser():
    print('regiser user app route')
    if request.method == 'POST':
        # jsObj = {}
        fname = request.form['firstName']
        lname = request.form['lastName']
        email = request.form['email']
        phonenum = request.form['phoneNum']
        password = request.form['password']
        print('request == POST')
        # if request.form['carMake'] != "" and request.form['carModel'] != "" and request.form['regNum'] != "":
        #     db.register_with_car(request.form['firstName'], request.form['lastName'], request.form['email'],
        #                 request.form['phoneNum'], request.form['password'], request.form['carMake'],
        #                 request.form['carModel'], request.form['regNum'])
        # else:
        if fname is '' or lname is '' or email is '' or phonenum is 0 or password is '':
            jsObj = json.dumps({"status": "Not all required elements are entered"})
            return jsObj
        else:
            jsObj = db.register(fname, lname, email, phonenum, password)
            return jsObj
    else:
        return 'POST did not work'


@app.route('/loginuser', methods=['PUT', 'POST'])
def check_email():
    print('start of check_email')
    if request.method == 'POST':
        data = db.check_if_registered(request.form['email_login'], request.form['password_login'])
        # json_str = json.dumps(data,default=myconverter) #optional parameter if it comes across an object it cannot serialize
        # print(type(json_str))
        # parsed_json= json.loads(json_str)
        # print('login funct' + json_str)
        return data


@app.route('/checkifemailexists', methods=['POST'])
def check_if_email_exists():
    print('start of if email exists')
    if request.method == 'POST':
        email = request.get_data('data1')
        print('email', email)
        return db.check_if_exists(email)




if __name__ == '__main__':
    app.run(debug=True)


import DBcm
import json



config = {
    'host': 'Looprac.mysql.pythonanywhere-services.com',
    'user': 'Looprac',
    'password': 'itcarlow',
    'database': 'Looprac$LoopracDB'
}


# MAIN QUERY FUNCTION EXECUTOR
def database_query(query, args=(), one=False):
    with DBcm.UseDatabase(config) as cursor:
        _SQL = query
        cursor.execute(_SQL, args)
        r = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
    return (r[0] if r else None) if one else r


#QUERY TO DISPLAY AVAILABLE LIFTS, CALLS 'DATABASE_QUERY' TO EXECUTE IT
def list_available_lifts():
    my_query = database_query("SELECT LiftID, UserID, Start_County, Destination_County FROM Lift")
    json_output = json.dumps(my_query)
    return json_output


def register(fName: str, lName:str, emailAddr:str, phoneN, passw):
    print('register function')
    firstName = fName.lower()
    lastName = lName.lower()
    emailAddress = emailAddr.lower()
    emailExists = check_if_exists(emailAddress)
    if emailExists is True:
        jsObj = json.dumps({"status": "email exists"})
        return jsObj
    else:
        _User_Register_SQL = """INSERT INTO User
                        (fName, Last_Name, Email, Phone_Number, Password, Date_Created)
                        VALUES
                        (%s, %s, %s, %s, %s, CURRENT_DATE )"""
        with DBcm.UseDatabase(config) as cursor:
            cursor.execute(_User_Register_SQL, (firstName, lastName, emailAddress, phoneN, passw))
            primary_key = cursor.lastrowid
        register_passenger(primary_key)
        jsObj = json.dumps({"status": "registered"})
        return jsObj


# def register_with_car(fName, lName, emailAddr, phoneN, passw, carMake, carModel, carRegistration):
#     # jsObj = {'firstName': fName, 'lastName': lName, 'email': emailAddr, 'phoneNum': phoneN, 'password': passw,
#     #          'carMake': carMake, 'carModel': carModel, 'regNum': carRegistration}
#     # firstName = jsObj['firstName']
#     # lastName = jsObj['lastName']
#     # email = jsObj['email']
#     # phonenum = jsObj['phoneNum']
#     # passwd = jsObj['password']
#     # carmake = jsObj['carMake']
#     # carmodel = jsObj['carModel']
#     # carregistration = jsObj['regNum']
#     _User_Register_SQL = """INSERT INTO User
#                      (First_Name, Last_Name, Email, Phone_Number, Password, Date_Created)
#                      VALUES
#                      (%s, %s, %s, %s, %s, CURRENT_DATE )"""
#     with DBcm.UseDatabase(config) as cursor:
#         cursor.execute(_User_Register_SQL, (fName, lName, emailAddr, phoneN, passw))
#         primary_key = cursor.lastrowid
#         _CarDetails_Registration_SQL = """INSERT INTO CarDetails
#                            (Car_Make, Car_Model, Car_Reg, UserID)
#                            VALUES
#                            (%s, %s, %s, %s)"""
#     with DBcm.UseDatabase(config) as cursor:
#         cursor.execute(_CarDetails_Registration_SQL, (carMake, carModel, carRegistration, primary_key))
#     register_driver(primary_key)
#     register_passenger(primary_key)


def register_driver(userid):
    _Driver_Registration_SQL = """INSERT INTO Driver
                     (UserID)
                     VALUES
                     (%s)"""
    with DBcm.UseDatabase(config) as cursor:
        cursor.execute(_Driver_Registration_SQL, (userid,))


def register_passenger(userid):
    _Passenger_Registration_SQL = """INSERT INTO Passenger
                     (UserID)
                     VALUES
                     (%s)"""
    with DBcm.UseDatabase(config) as cursor:
        cursor.execute(_Passenger_Registration_SQL, (userid,))


def check_if_registered(email, password):
    with DBcm.UseDatabase(config) as cursor:
        _SQL = """SELECT Email FROM User WHERE Email= %s"""
        cursor.execute(_SQL, (email,))
        data = list(cursor.fetchall())
        emaildata = [i[0] for i in data]
    with DBcm.UseDatabase(config) as cursor:
        _SQL = """SELECT Password FROM User WHERE Password= %s"""
        cursor.execute(_SQL, (password,))
        data = list(cursor.fetchall())
        passworddata = [i[0] for i in data]
    if emaildata == [] or passworddata == []:
        jsObj = json.dumps({"status": "wrongemail/password"})
    elif email == emaildata[0] and password == passworddata[0]:
        jsObj = json.dumps({"status": "match"})
    else:
        jsObj = json.dumps({"status": "nomatch"})
    return jsObj


def check_if_exists(email: str):
    print('if exists function')
    exists = False
    with DBcm.UseDatabase(config) as cursor:
        _SQL = """SELECT Email FROM User WHERE Email= %s"""
        cursor.execute(_SQL, (email,))
        data = list(cursor.fetchall())
        emaildata = [i[0] for i in data]
    print('email data', emaildata)
    if emaildata == []:
        print('doesnt exist')
        return exists
    else:
        exists = True
        print('exists',exists)
        return exists
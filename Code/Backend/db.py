import DBcm
import json
from flask import session
import datetime


config = {
    'host': 'Looprac.mysql.pythonanywhere-services.com',
    'user': 'Looprac',
    'password': 'itcarlow',
    'database': 'Looprac$LoopracDB'
}


#QUERY TO DISPLAY AVAILABLE LIFTS
def list_available_lifts():
    _SQL = """SELECT LiftID, DriverID,Start_County, Destination_County, Depart_Date, Depart_Time FROM Lift
              order by Depart_Date"""
    with DBcm.UseDatabase(config) as cursor:
        cursor.execute(_SQL)
        data = cursor.fetchall()
    print('data', type(data))
    d = []
    for item in data:
        d.append({
                'liftID': item[0],
                'driverID': item[1],
                'startCounty': item[2],
                'destinationCounty': item[3],
                'departDate': item[4],
                'departTime': item[5]
        })
    jsObj = json.dumps(d, default=converter)
    print('js obj', type(jsObj), '\n', jsObj)
    return jsObj


def converter(obj):
    return str(obj)


def getLiftDetails(liftID, driverID):
    print('before query')
    _SELECT = """ SELECT Driver.UserID, User.First_Name, User.Last_Name
                  FROM User, Driver
                  WHERE Driver.DriverID= %s"""
    _SQL = """SELECT * FROM Lift WHERE LiftID= %s order by Created_At"""
    # _GETDRIVER_SQL = """ SELECT UserID FROM Driver WHERE DriverID= %s """
    # _GETUSER_SQL = """SELECT First_Name, Last_Name FROM User WHERE UserID= %s"""
    with DBcm.UseDatabase(config) as cursor:
        cursor.execute(_SQL, (liftID,))
        data = cursor.fetchall()
    print('data', data)
    print('after lift query')
    with DBcm.UseDatabase(config) as cursor:
        cursor.execute(_SELECT, (driverID,))
        userDetails = cursor.fetchall()
    print('user', userDetails)
    print('after user query')
    # with DBcm.UseDatabase(config) as cursor:
    #     cursor.execute(_GETDRIVER_SQL, (driverID,))
    #     driverData = cursor.fetchall()
    #     print('data', driverData)
    #     userID = driverData[0][0]
    #     print('driver id', userID)
    # with DBcm.UseDatabase(config) as cursor:
    #     cursor.execute(_GETUSER_SQL, (userID,))
    #     userData = cursor.fetchall()
    d = []
    for item in data:
        for i in userDetails:
            d.append({
                'DriverFName': i[1],
                'DriverLName': i[2],
                'liftID': item[0],
                'driverID': item[1],
                'startLat': item[3],
                'startLng': item[4],
                'startCounty': item[5],
                'destinationLat': item[6],
                'destinationLng': item[7],
                'destinationCounty': item[8],
                'departDate': item[9],
                'returnDate': item[10],
                'departTime': item[11],
                'returnTime': item[12],
                'seats': item[13],
                'liftType': item[14],
                'created': item[15]
            })
    print('after d append')
    print('d', d)
    jsObj = json.dumps(d, default=converter)
    return jsObj



def register(fName, lName, emailAddr, phoneN, passw):
    print('register function')
    firstName = fName.lower()
    lastName = lName.lower()
    emailAddress = emailAddr.lower()
    emailExists = check_if_exists(emailAddress)
    if emailExists is True:
        jsObj = json.dumps({"status": "email exists"})
        return jsObj
    else:
        print('registering')
        _User_Register_SQL = """INSERT INTO User
                        (First_Name, Last_Name, Email, Phone_Number, Password, Date_Created)
                        VALUES
                        (%s, %s, %s, %s, %s, CURRENT_DATE )"""
        with DBcm.UseDatabase(config) as cursor:
            cursor.execute(_User_Register_SQL, (firstName, lastName, emailAddress, phoneN, passw))
            primary_key = cursor.lastrowid
        register_passenger(primary_key)
        jsObj = json.dumps({"status": "registered"})
        return jsObj


def register_passenger(userid):
    _Passenger_Registration_SQL = """INSERT INTO Passenger
                     (UserID)
                     VALUES
                     (%s)"""
    with DBcm.UseDatabase(config) as cursor:
        cursor.execute(_Passenger_Registration_SQL, (userid,))


def process_login(email, password):
    print('login function')
    emaildata, passworddata = [], []
    jsObj = {}
    uID, passengerID, driverID = 0, 0, 0
    uName, uLName = "", ""
    with DBcm.UseDatabase(config) as cursor:
        try:
            _SQL = """SELECT Email FROM User WHERE Email= %s"""
            cursor.execute(_SQL, (email,))
            data = list(cursor.fetchall())
            emaildata = [i[0] for i in data]
            print('email data', data)
        except Exception as e:
            print('Error looking up email:', e)
    with DBcm.UseDatabase(config) as cursor:
        try:
            _SQL = """SELECT Password FROM User WHERE Password= %s"""
            cursor.execute(_SQL, (password,))
            data = list(cursor.fetchall())
            passworddata = [i[0] for i in data]
            print('password data:', data)
        except Exception as e:
            print('error looking up password: ', e)
    if emaildata == [] or passworddata == []:
        jsObj = json.dumps({"status": "wrongemail/password"})
    elif email == emaildata[0] and password == passworddata[0]:
        with DBcm.UseDatabase(config) as cursor:
            try:
                # _SQL = """SELECT u.UserID, u.First_Name, u.Last_Name,p.PassengerID, d.DriverID
                #           FROM User u INNER JOIN Passenger p ON u.UserID = p.PassengerID
                #                       INNER JOIN Driver d ON u.UserID = d.DriverID
                #           WHERE u.Email = %s"""
                _SQL = """SELECT u.UserID, u.First_Name, u.Last_Name,p.PassengerID
                                         FROM User u , Passenger p
                                         WHERE u.Email = %s
                                         AND p.UserID = u.UserID"""
                cursor.execute(_SQL, (email,))
                # data = list(cursor.fetchall())
                data = cursor.fetchall()

                print('login data: ', data)
                # if len(data) == 5:
                #     uID = data[0][0]
                #     uName = data[0][1]
                #     uLName = data[0][2]
                #     passengerID = data[0][3]
                #     driverID = data[0][4]
                # elif len(data) == 4:
                uID = data[0][0]
                uName = data[0][1]
                uLName = data[0][2]
                passengerID = data[0][3]
                jsObj = json.dumps(
                    {"status": "match", "email": email, "user_id": uID, "first_name": uName, "last_name": uLName,
                     "passengerID": passengerID, "driverID": driverID})
            except Exception as e:
                print('error with inner join: ', e)
        print('before update')
        with DBcm.UseDatabase(config) as cursor:
            try:
                _Update_LoggedIn = """UPDATE User SET Logged_In=1 WHERE UserID=%s"""
                cursor.execute(_Update_LoggedIn, (uID,))
                session['logged_in'] = True
            except Exception as e:
                print('error executing update:', e)
        print('after update')
    else:
        jsObj = json.dumps({"status": "nomatch"})
    return jsObj


def process_logout(userID):
    print('process logout func', userID)
    with DBcm.UseDatabase(config) as cursor:
        try:
            _SQL = """UPDATE User SET Logged_In=0 WHERE UserID=%s   """
            cursor.execute(_SQL, (userID,))
            session['logged_in'] = False
            jsObj = json.dumps({"status": "logout successful"})
            return jsObj
        except Exception as err:
            print('sql error:', err)


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
        print('exists', exists)
        return exists


def register_offer_lift(userID,startLat, startLong, startCounty, destinationLat, destinationLong, destinationCounty,
                        date, time, returnDate, returnTime, journey_type, seats):
    print('register function', userID, startLat, startLong, startCounty,destinationLat, destinationLong, destinationCounty,
          date, time, journey_type, seats)
    _GETDRIVER_SQL = """SELECT DriverID FROM Driver WHERE UserID= %s """
    _User_Register_SQL = """INSERT INTO Lift
                       (DriverID, Start_Lat, Start_Long, Start_County, Destination_Lat, Destination_Long,
                       Destination_County, Depart_Date, Depart_Time, Return_Date, Return_Time, Available_Spaces, Return_Single,
                       Created_At)
                       VALUES
                       (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP )"""
    with DBcm.UseDatabase(config) as cursor:
        cursor.execute(_GETDRIVER_SQL, (userID,))
        data = cursor.fetchall()
        print('data', data)
        driverID = data[0][0]
        print('driver id', driverID)
        cursor.execute(_User_Register_SQL, (driverID, startLat, startLong, startCounty, destinationLat, destinationLong,
                                            destinationCounty, date, time, returnDate, returnTime, seats, journey_type))
    jsObj = json.dumps({"status": "registered"})
    return jsObj


# CHECK IF USER HAS A CAR REGISTERED BEFORE OFFERING A LIFT
def is_car_registered(userID):
    print('is car registered func')
    if checkIfCarExists(userID):
        print('car exists')
        jsObj = json.dumps({"status": "car registered"})
    else:
        print('car doesnt exist')
        jsObj = json.dumps({"status": "car not registered"})
    return jsObj


def checkIfCarExists(userID):
    with DBcm.UseDatabase(config) as cursor:
        _SQL = """SELECT * FROM CarDetails WHERE UserID= %s"""
        cursor.execute(_SQL, (userID,))
        data = list(cursor.fetchall())
    print('data from db for car details', data)
    if data == []:
        exists = False
        print('car doesnt exist')
        jsObj = json.dumps({"status": "car not registered"})
    else:
        exists = True
        print('car exists')
        jsObj = json.dumps({"status": "car registered"})
    return jsObj


def registerCarAndDriver(userID, carMake, carModel, regNum):
    carmake_lower = carMake.lower()
    carmodel_lower = carModel.lower()
    reg_lower = regNum.lower()
    _CAR_SQL = """INSERT INTO CarDetails
                       (Car_Make, Car_Model, Car_Reg, UserID)
                       VALUES
                       (%s, %s, %s, %s)"""
    _DRIVER_SQL = """INSERT INTO Driver
                        (UserID, CarID)
                        VALUES
                        (%s, %s)"""
    with DBcm.UseDatabase(config) as cursor:
        cursor.execute(_CAR_SQL, (carmake_lower, carmodel_lower, reg_lower, userID))
        carID = cursor.lastrowid
        cursor.execute(_DRIVER_SQL, (userID, carID))
    jsObj = json.dumps({"status": "registered"})
    return jsObj

def process_request(liftID, passengerID):
    driverID, requestID = 0, 0
    _GETDRIVER_SQL = """SELECT DriverID FROM Lift
                        WHERE LiftID = %s"""
    _REQUEST_SQL = """INSERT INTO Request
                      (DriverID, LiftID, PassengerID)
                      VALUES
                      (%s, %s, %s)"""
    try:
        with DBcm.UseDatabase(config)as cursor:
            try:
                cursor.execute(_GETDRIVER_SQL, (liftID,))
                data = cursor.fetchall()
                print('driverID: ', data)
                driverID = data[0][0]
                print('processed id: ', driverID)
            except Exception as e:
                print('error executing get driver SELECT query:', e)
        with DBcm.UseDatabase(config) as cursor:
            try:
                cursor.execute(_REQUEST_SQL, (driverID, liftID, passengerID))
                requestID = cursor.lastrowid
            except Exception as e:
                print('error executing insert request:', e)
    except Exception as e:
        print('error executing process request queries:', e)
    else:
        return json.dumps({"status": "request completed", "requestID": requestID})



import DBcm
import json
from flask import session
import hashlib

config = {
    'host': 'Looprac.mysql.pythonanywhere-services.com',
    'user': 'Looprac',
    'password': 'itcarlow',
    'database': 'Looprac$LoopracDB'
}


def get_main_page_lifts(passengerID):
    jsObj = {}
    d = []
    _FILTERLIFTLIST_SQL = """SELECT l.LiftID, l.DriverID, l.Start_Lat, l.Start_Long
                 FROM Lift l, Driver d, User u, Passenger p
                 WHERE  l.Available_Spaces > 0
                 AND l.LiftID NOT IN
                 (SELECT LiftID FROM Request WHERE PassengerID = %s)
                   AND p.UserID = u.UserID
                   AND u.UserID = d.UserID
                   AND l.DriverID = d.DriverID
                   AND l.DriverID NOT IN
                   (SELECT d.DriverID
                   FROM Driver d, User u, Passenger p
                   WHERE p.UserID = u.UserID
                   AND u.UserID = d.UserID
                   AND p.PassengerID = %s) """
    with DBcm.UseDatabase(config) as cursor:
        try:
            cursor.execute(_FILTERLIFTLIST_SQL, (passengerID, passengerID ))
            data = cursor.fetchall()
            print('length', len(data), 'data', data)
            for item in data:
                d.append({
                    'liftID': item[0],
                    'driverID': item[1],
                    'startLat': item[2],
                    'startLng': item[3],
                })
                jsObj = json.dumps(d, default=converter)
        except Exception as e:
            print('Error with select lift details that user hasnt requested query: ', e)
        else:
            return jsObj


#QUERY TO DISPLAY AVAILABLE LIFTS
def list_available_lifts(passengerID):
    data, data2, d = [], [], []
    # Query that filters available lifts to only display lifts that have available spaces, they user hasn't already requested or if the user is a driver, not to show their lifts
    _FILTERLIFTLIST_SQL = """SELECT l.LiftID, l.DriverID, l.Start_County, l.Destination_County, l.Depart_Date, l.Depart_Time
              FROM Lift l, Driver d, User u, Passenger p
              WHERE  l.Available_Spaces > 0
              AND l.LiftID NOT IN
              (SELECT LiftID FROM Request WHERE PassengerID = %s)
                AND p.UserID = u.UserID
                AND u.UserID = d.UserID
                AND l.DriverID = d.DriverID
                AND l.DriverID NOT IN
                (SELECT d.DriverID
                FROM Driver d, User u, Passenger p
                WHERE p.UserID = u.UserID
                AND u.UserID = d.UserID
                AND p.PassengerID = %s) """
    with DBcm.UseDatabase(config) as cursor:
        try:
            cursor.execute(_FILTERLIFTLIST_SQL, (passengerID, passengerID))
            data = cursor.fetchall()
            print('length', len(data), 'data', data)
        except Exception as e:
            print('Error with select lift details that user hasnt requested query: ', e)
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
    return jsObj


# for JSON obj, if json.dumps() receives an object it can't process, its sent to this function and converted to str
def converter(obj):
    return str(obj)


def getLiftDetails(liftID, driverID):
    print('liftID', liftID, 'driverID', driverID)
    _DRIVER_DETAILS_SQL = """ SELECT u.UserID, u.First_Name, u.Last_Name, r.Rating
                  FROM User u, Driver d, UserRating r
                  WHERE u.UserID = d.UserID
                  AND r.UserID = u.UserID
                  AND d.DriverID= %s"""
    _LIFT_DETAILS_SQL = """SELECT * FROM Lift WHERE LiftID= %s order by Created_At"""
    with DBcm.UseDatabase(config) as cursor:
        cursor.execute(_LIFT_DETAILS_SQL, (liftID,))
        data = cursor.fetchall()
    print('data', data)
    print('after lift query')
    with DBcm.UseDatabase(config) as cursor:
        cursor.execute(_DRIVER_DETAILS_SQL, (driverID,))
        userDetails = cursor.fetchall()
    print('user', userDetails)
    print('after user query')
    d = []
    for item in data:
        for i in userDetails:
            d.append({
                'DriverFName': i[1],
                'DriverLName': i[2],
                'rating': i[3],
                'liftID': item[0],
                'driverID': item[1],
                'startLat': item[2],
                'startLng': item[3],
                'startCounty': item[4],
                'destinationLat': item[5],
                'destinationLng': item[6],
                'destinationCounty': item[7],
                'departDate': item[8],
                'departTime': item[9],
                'seats': item[10],
                'created': item[11]
            })
    print('after d append')
    print('d', d)
    jsObj = json.dumps(d, default=converter)
    return jsObj


def register(fName, lName, emailAddr, phoneN, passw):
    jsObj = {}
    userID = 0
    print('register function')
    firstName = fName.lower()
    lastName = lName.lower()
    phone = str(phoneN)
    emailAddress = emailAddr.lower()
    hashedPassword = hashlib.sha256(bytes(passw, encoding='utf-8')).hexdigest()
    emailExists = check_if_exists(emailAddress)
    print('posted', firstName, lastName, emailAddress, hashedPassword)
    if emailExists is True:
        jsObj = json.dumps({"status": "email exists"})
        return jsObj
    else:
        print('registering')
        _USER_REGISTER_SQL = """INSERT INTO User
                        (First_Name, Last_Name, Email, Phone_Number, Password, Date_Created)
                        VALUES
                        (%s, %s, %s, %s, %s, CURRENT_DATE )"""
        _PASSENGER_REGISTRATION_SQL = """INSERT INTO Passenger
                           (UserID)
                           VALUES
                           (%s)"""
        USER_RATING_REGISTER_SQL = """INSERT
                                          INTO UserRating
                                          (UserID)
                                          VALUES
                                          (%s)"""
        with DBcm.UseDatabase(config) as cursor:
            try:
                cursor.execute(_USER_REGISTER_SQL, (firstName, lastName, emailAddress, phone, hashedPassword))
                userID = cursor.lastrowid
            except Exception as e:
                print('Error registering user to User table:', e )
        with DBcm.UseDatabase(config) as cursor:
            try:
                cursor.execute(_PASSENGER_REGISTRATION_SQL, (userID,))
            except Exception as e:
                print('Error adding user to Passenger table', e)
        with DBcm.UseDatabase(config) as cursor:
            try:
                cursor.execute(USER_RATING_REGISTER_SQL, (userID,))
            except Exception as e:
                print('Error registering user rating:', e)
            else:
                jsObj = json.dumps({"status": "registered"})
                return jsObj


def process_login(email, password):
    print('login function')
    emaildata, passworddata = [], []
    jsObj = {}
    uID, passengerID, driverID = 0, 0, 0
    uName, uLName = "", ""
    hashedPassword = hashlib.sha256(bytes(password, encoding='utf-8')).hexdigest()

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
            cursor.execute(_SQL, (hashedPassword,))
            data = list(cursor.fetchall())
            passworddata = [i[0] for i in data]
            print('password data:', data)
        except Exception as e:
            print('error looking up password: ', e)
    if emaildata == [] or passworddata == []:
        jsObj = json.dumps({"status": "wrongemail/password"})
    elif email == emaildata[0] and hashedPassword == passworddata[0]:
        with DBcm.UseDatabase(config) as cursor:
            try:
                _GET_USER_DETAILS_SQL = """SELECT u.UserID, u.First_Name, u.Last_Name,p.PassengerID
                                         FROM User u , Passenger p
                                         WHERE u.Email = %s
                                         AND p.UserID = u.UserID"""
                cursor.execute(_GET_USER_DETAILS_SQL, (email,))
                data = cursor.fetchall()
                print('login data: ', data)
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
                        date, time, seats):
    print('register function', userID, startLat, startLong, startCounty,destinationLat, destinationLong, destinationCounty,
          date, time, seats)
    _GETDRIVER_SQL = """SELECT DriverID FROM Driver WHERE UserID= %s """
    _User_Register_SQL = """INSERT INTO Lift
                       (DriverID, Start_Lat, Start_Long, Start_County, Destination_Lat, Destination_Long,
                       Destination_County, Depart_Date, Depart_Time, Available_Spaces,
                       Created_At)
                       VALUES
                       (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,CURRENT_TIMESTAMP )"""
    with DBcm.UseDatabase(config) as cursor:
        cursor.execute(_GETDRIVER_SQL, (userID,))
        data = cursor.fetchall()
        print('data', data)
        driverID = data[0][0]
        print('driver id', driverID)
        cursor.execute(_User_Register_SQL, (driverID, startLat, startLong, startCounty, destinationLat, destinationLong,
                                            destinationCounty, date, time, seats))
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
        print('car doesnt exist')
        jsObj = json.dumps({"status": "car not registered"})
    else:
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


# REQUESTS


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


def list_user_requests(userID):
    driverID = 0
    _GETDRIVER_SQL = """SELECT DriverID FROM Driver WHERE UserID = %s"""
    _GETREQUESTS_SQL = """SELECT r.RequestID, r.DriverID, r.LiftID, r.PassengerID, r.Status, u.First_Name, u.Last_Name
                          FROM Request r, Passenger p, User u
                          WHERE r.PassengerID = p.PassengerID
                          AND u.UserID = p.UserID
                          AND r.DriverID = %s"""
    with DBcm.UseDatabase(config) as cursor:
        try:
            cursor.execute(_GETDRIVER_SQL, (userID, ))
            data = cursor.fetchall()
            driverID = data[0][0]
            print('driverID', driverID)
        except Exception as e:
            print('Error with get driver select query:', e)
    with DBcm.UseDatabase(config) as cursor:
        try:
            cursor.execute(_GETREQUESTS_SQL, (driverID, ))
            requestData = cursor.fetchall()
            print('request data', requestData)
            d = []
            for item in requestData:
                d.append({
                    'requestID': item[0],
                    'driverID': item[1],
                    'liftID': item[2],
                    'passengerID': item[3],
                    'status': item[4],
                    'passengerName': item[5] + ' ' + item[6]
                })
            for i in d:
                print(i)
            jsObj = json.dumps(d)
            print('js obj', jsObj, 'length', len(jsObj))
        except Exception as e:
            print('Error with get requests select query:', e)
        else:
            return jsObj


def getRequestDetails(requestID):
    d, data, liftData = [], [], []
    _GETPASSENGERDETAILS_SQL ="""SELECT u.First_Name, u.Last_Name, u.Phone_Number, p.PassengerID, ur.Rating
                                  FROM User u, Passenger p, Request r, UserRating ur
                                  WHERE u.UserID = p.UserID
                                  AND p.passengerID = r.PassengerID
                                  AND ur.UserID = p.UserID
                                  AND r.requestID = %s"""
    _GETLIFTDETAILS_SQL = """SELECT l.Depart_Date, l.Depart_Time, l.Start_Lat, l.Start_Long, l.Destination_Lat, l.Destination_Long
                              FROM Lift l, Request r
                              WHERE r.LiftID = l.LiftID
                              AND r.RequestID = %s"""
    with DBcm.UseDatabase(config) as cursor:
        try:
            cursor.execute(_GETPASSENGERDETAILS_SQL, (requestID,))
            data = cursor.fetchall()
            print('passenger data:', data)
        except Exception as e:
            print('Error with get passenger details query: ', e)
    with DBcm.UseDatabase(config) as cursor:
        try:
            cursor.execute(_GETLIFTDETAILS_SQL, (requestID,))
            liftData = cursor.fetchall()
            print('lift data:', liftData)
        except Exception as e:
            print('Error with get lift details query: ', e)
        else:
            for item in data:
                for i in liftData:
                    d.append({
                        'passengerID': item[3],
                        'name': item[0] + ' ' + item[1],
                        'rating': item[4],
                        'phoneNum': item[2],
                        'date': i[0],
                        'time': i[1],
                        'startLat': i[2],
                        'startLng': i[3],
                        'destLat': i[4],
                        'destLng': i[5]
                    })
                    jsObj = json.dumps(d, default=converter)
                    return jsObj


def getMyRequests(userID):
    passengerID = 0
    _GETPASSENGER_SQL = """SELECT PassengerID FROM Passenger WHERE UserID = %s"""
    _GETREQUESTS_SQL = """SELECT r.RequestID, r.DriverID, r.LiftID, r.PassengerID, r.Status, u.First_Name, u.Last_Name
                          FROM Request r, Driver d, User u WHERE r.DriverID = d.DriverID
                          AND u.UserID = d.UserID
                          AND r.PassengerID = %s"""
    with DBcm.UseDatabase(config) as cursor:
        try:
            cursor.execute(_GETPASSENGER_SQL, (userID,))
            data = cursor.fetchall()
            passengerID = data[0][0]
            print('passengerID', passengerID)
        except Exception as e:
            print('Error with get passenger select query:', e)
    with DBcm.UseDatabase(config) as cursor:
        try:
            cursor.execute(_GETREQUESTS_SQL, (passengerID, ))
            requestData = cursor.fetchall()
            print('request data', requestData)
            d = []
            for item in requestData:
                d.append({
                    'requestID': item[0],
                    'driverID': item[1],
                    'liftID': item[2],
                    'passengerID': item[3],
                    'status': item[4],
                    'driverFName': item[5],
                    'driverLName': item[6]
                })
            jsObj = json.dumps(d)
            print('js obj', jsObj, 'length', len(jsObj))
        except Exception as e:
            print('Error with get requests select query:', e)
        else:
            return jsObj


def acceptRequest(requestID):
    driverID, passengerID, liftID = 0, 0, 0
    _GETDRIVERPASSENGER_SQL = """SELECT DriverID, PassengerID, LiftID FROM Request WHERE RequestID = %s"""
    _UPDATELIFT_SQL = """UPDATE Lift SET Available_Spaces = Available_Spaces - 1 WHERE LiftID = %s"""
    _ADDTOCARGROUP_SQL = """INSERT INTO CarGroup (LiftID, DriverID, PassengerID) VALUES ( %s, %s, %s)"""
    _UPDATEREQUESTSTATUS_SQL = """UPDATE Request SET Status = 'Accepted' WHERE RequestID = %s"""
    with DBcm.UseDatabase(config) as cursor:
        try:
            cursor.execute(_GETDRIVERPASSENGER_SQL, (requestID,))
            data = cursor.fetchall()
            driverID = data[0][0]
            passengerID = data[0][1]
            liftID = data[0][2]
        except Exception as e:
            print('Error with getting passengerID and liftID: ', e)
        try:
            cursor.execute(_UPDATELIFT_SQL, (liftID,))
        except Exception as e:
            print('Error updating lift with accepted passenger:', e)
        try:
            cursor.execute(_ADDTOCARGROUP_SQL, (liftID, driverID, passengerID))
        except Exception as e:
            print('Error inserting into car group table:', e)
        try:
            cursor.execute(_UPDATEREQUESTSTATUS_SQL, (requestID, ))
        except Exception as e:
            print('Error updating request status:', e)
    jsObj = json.dumps({'status': 'complete'})
    return jsObj


def denyRequest(requestID):
    _UPDATEREQUESTSTATUS_SQL = """UPDATE Request SET Status = 'Denied' WHERE RequestID = %s"""
    with DBcm.UseDatabase(config) as cursor:
        try:
            cursor.execute(_UPDATEREQUESTSTATUS_SQL, (requestID,))
            jsObj = json.dumps({"status": "complete"})
        except Exception as e:
            print('Error with updating request status: ', e)
        else:
            return jsObj


def getMyGroups(userID):
    _GROUPDETAIL_SQL = """SELECT c.GroupID, u.First_Name, u.Last_Name, l.LiftID, l.Depart_Time, l.Depart_Date
                          FROM CarGroup c, Driver d, User u, Lift l, Passenger p
                          WHERE c.DriverID = d.DriverID
                          AND u.UserID = d.UserID
                          AND c.LiftID = l.LiftID
                          AND c.PassengerID = p.PassengerID
                          AND p.UserID = %s"""
    with DBcm.UseDatabase(config) as cursor:
        try:
            cursor.execute(_GROUPDETAIL_SQL, (userID,))
            data = cursor.fetchall()
            d = []
            for item in data:
                d.append({
                    'groupID': item[0],
                    'driverName': item[1] + ' ' + item[2],
                    'liftID': item[3],
                    'departTime': item[4],
                    'departDate': item[5],
                })
            jsObj = json.dumps(d, default=converter)
        except Exception as e:
            print('Error getting group details:', e)
        else:
            return jsObj


def getGroupDetails(liftID, groupID):
    data, driverData = [], []
    print('lift', liftID, 'group', groupID)
    _GETPASSENGERS_SQL = """SELECT u.First_Name, u.Last_Name, u.Phone_Number, r.Rating
                            FROM User u, Passenger p, CarGroup c, UserRating r
                            WHERE c.PassengerID = p.PassengerID
                            AND p.UserID = u.UserID
                            AND r.UserID = u.UserID
                            AND c.LiftID = %s
                           """
    _GETGROUPDETAILS_SQL = """SELECT l.Start_County, l.Destination_County, l.Depart_Date, l.Depart_Time,
                                  l.Start_Lat, l.Start_Long, l. Destination_Lat, l.Destination_Long
                                  FROM Lift l, CarGroup c
                                  WHERE c.LiftID = l.LiftID
                                  AND c.GroupID = %s"""
    _GETDRIVERDETAILS_SQL = """SELECT u.First_Name, u.Last_Name, u.Phone_Number, r.Rating, c.Car_Reg
                               FROM User u, CarDetails c, Driver d, CarGroup g, UserRating r
                               WHERE u.UserID = c.UserID
                               AND u.UserID = d.UserID
                               AND d.DriverID = g.DriverID
                               AND r.UserID = u.UserID
                               AND g.GroupID = %s"""
    with DBcm.UseDatabase(config) as cursor:
        try:
            cursor.execute(_GETGROUPDETAILS_SQL, (groupID, ))
            data = cursor.fetchall()
            print('data', data)

        except Exception as e:
            print('Error getting group details: ', e)
    with DBcm.UseDatabase(config) as cursor:
        try:
            cursor.execute(_GETDRIVERDETAILS_SQL, (groupID,))
            driverData = cursor.fetchall()
            print('driver data', driverData)
        except Exception as e:
            print('Error getting driver details: ', e)
    with DBcm.UseDatabase(config) as cursor:
        try:
            cursor.execute(_GETPASSENGERS_SQL, (liftID,))
            passengerData = cursor.fetchall()
            print('passenger data', passengerData)
            d = []
            for item in data:
                for i in driverData:
                    for it in passengerData:
                        d.append({
                            'groupID': groupID,
                            'liftID': liftID,
                            'driverName': i[0] + ' ' + i[1],
                            'driverPhone': i[2],
                            'driverRating': i[3],
                            'carReg': i[4],
                            'startCounty': item[0],
                            'destCounty': item[1],
                            'departDate': item[2],
                            'departTime': item[3],
                            'startLat': item[4],
                            'startLng': item[5],
                            'destLat': item[6],
                            'destLng': item[7],
                            'passengerName': it[0] + ' ' + it[1],
                            'passengerPhone': it[2],
                            'passengerRating': it[3]
                        })
            jsObj = json.dumps(d, default=converter)
        except Exception as e:
            print('Error getting passenger details: ', e)
        else:
            return jsObj


# MY LIFTS


def getMyLifts(userID):
    _LIFTDETAIL_SQL = """SELECT l.LiftID, l.Start_County, l.Destination_County, l.Depart_Date, l.Depart_Time
                             FROM Lift l, Driver d
                             WHERE l.DriverID = d.DriverID
                             AND d.UserID = %s"""
    with DBcm.UseDatabase(config) as cursor:
        try:
            cursor.execute(_LIFTDETAIL_SQL, (userID,))
            data = cursor.fetchall()
            print('data', data)
            d = []
            for item in data:
                d.append({
                    'userID': userID,
                    'liftID': item[0],
                    'route': item[1] + ' to ' + item[2],
                    'departDate': item[3],
                    'departTime': item[4]
                })
            jsObj = json.dumps(d, default=converter)
        except Exception as e:
            print('Error getting lift list details:', e)
        else:
            return jsObj


def getMyLiftDetails(liftID):
    d, passengerData = [], []
    numOfPassengers = 0
    _GETPASSENGERS_SQL = """SELECT u.First_Name, u.Last_Name, u.Phone_Number
                            FROM User u, Passenger p, CarGroup c
                            WHERE c.PassengerID = p.PassengerID
                            AND p.UserID = u.UserID
                            AND c.LiftID = %s"""
    _GETMYLIFTDETAILS_SQL = """SELECT l.*
                                FROM Lift l
                                WHERE LiftID = %s"""

    with DBcm.UseDatabase(config) as cursor:
        try:
            cursor.execute(_GETPASSENGERS_SQL, (liftID,))
            passengerData = cursor.fetchall()
            print('passenger data', passengerData)
            d = []
        except Exception as e:
            print('Error getting passenger details query: ', e)
    with DBcm.UseDatabase(config) as cursor:
        try:
            cursor.execute(_GETMYLIFTDETAILS_SQL, (liftID, ))
            data = cursor.fetchall()
            print('data', data)
            numOfPassengers = len(passengerData)
            print('number of passengers: ', numOfPassengers)
            if passengerData != []:
                print('has passengers')
                for item in data:
                    for i in passengerData:
                        d.append({
                            'liftID': liftID,
                            'startLat': item[2],
                            'startLng': item[3],
                            'startCounty': item[4],
                            'destLat': item[5],
                            'destLng': item[6],
                            'destCounty': item[7],
                            'departDate': item[8],
                            'departTime': item[9],
                            'spaces': item[10],
                            'created': item[11],
                            'passengerName': i[0] + ' ' + i[1],
                            'passengerPhone': i[2],
                            'numOfPassengers': numOfPassengers
                        })
            else:
                print('has no passengers')
                for item in data:
                    d.append({
                        'liftID': liftID,
                        'startLat': item[2],
                        'startLng': item[3],
                        'startCounty': item[4],
                        'destLat': item[5],
                        'destLng': item[6],
                        'destCounty': item[7],
                        'departDate': item[8],
                        'departTime': item[9],
                        'spaces': item[10],
                        'created': item[11],
                        'passengerName': 'None',
                        'passengerPhone': 'None'
                    })
            jsObj = json.dumps(d, default=converter)
        except Exception as e:
            print('Error getting my lift details:', e)
        else:
            return jsObj
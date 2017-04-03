import DBcm
import json
import hashlib
import datetime
from dateutil.tz import *
config = {
    'host': 'Looprac.mysql.pythonanywhere-services.com',
    'user': 'Looprac',
    'password': 'itcarlow',
    'database': 'Looprac$LoopracDB'
}


def get_main_page_lifts(passengerID):
    jsObj = {}
    d = []
    now = datetime.datetime.now()
    day = now.strftime("%Y-%m-%d")
    time = now.strftime("%Y-%m-%d %H:%M:%S")
    print('day', day, 'time', time)
    _FILTERLIFTLIST_SQL = """SELECT l.LiftID, l.DriverID, l.Start_Lat, l.Start_Long
                 FROM Lift l, Driver d, User u, Passenger p
                 WHERE  l.Available_Spaces > 0
                 AND l.Depart_Date > %s
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
            cursor.execute(_FILTERLIFTLIST_SQL, (time, passengerID, passengerID ))
            data = cursor.fetchall()
            print('length', len(data), 'data', data)
            if data != []:
                for item in data:
                    d.append({
                        'availablelifts': 'yes',
                        'liftID': item[0],
                        'driverID': item[1],
                        'startLat': item[2],
                        'startLng': item[3],
                    })
                    jsObj = json.dumps(d, default=converter)
            else:
                jsObj = json.dumps({"availablelifts": "none"})
        except Exception as e:
            print('Error with select lift details that user hasnt requested query: ', e)
        else:
            return jsObj


#QUERY TO DISPLAY AVAILABLE LIFTS
def list_available_lifts(passengerID):
    data, data2, d = [], [], []
    now = datetime.datetime.now()
    day = now.strftime("%Y-%m-%d")
    time = now.strftime("%Y-%m-%d %H:%M:%S")

    # Query that filters available lifts to only display lifts that have available spaces, they user hasn't already requested or if the user is a driver, not to show their lifts
    _FILTERLIFTLIST_SQL = """SELECT l.LiftID, l.DriverID, l.Start_County, l.Destination_County, l.Depart_Date
                 FROM Lift l, Driver d, User u, Passenger p
                 WHERE  l.Available_Spaces > 0
                 AND l.Depart_Date > %s
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
            cursor.execute(_FILTERLIFTLIST_SQL, (time, passengerID, passengerID))
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
                'departing': item[4],
        })
    jsObj = json.dumps(d, default=converter)
    return jsObj


# for JSON obj, if json.dumps() receives an object it can't process, its sent to this function and converted to str
def converter(obj):
    return str(obj)


def getLiftDetails(liftID, driverID):
    print('liftID', liftID, 'driverID', driverID)
    _DRIVER_DETAILS_SQL = """ SELECT u.UserID, u.First_Name, u.Last_Name, r.Rating, p.PassengerID
                  FROM User u, Driver d, UserRating r, Passenger p
                  WHERE u.UserID = d.UserID
                  AND u.UserID = p.UserID
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
                'driversPassengerID': i[4],
                'liftID': item[0],
                'driverID': item[1],
                'startLat': item[2],
                'startLng': item[3],
                'startCounty': item[4],
                'destinationLat': item[5],
                'destinationLng': item[6],
                'destinationCounty': item[7],
                'distance': item[8],
                'departing': item[9],
                'seats': item[10],
                'created': item[11]
            })
    print('after d append')
    print('d', d)
    jsObj = json.dumps(d, default=converter)
    return jsObj


def register(fName, lName, emailAddr, phoneN, passw, filename):
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
                        (First_Name, Last_Name, Email, Phone_Number, Password, Pic_Path, Date_Created)
                        VALUES
                        (%s, %s, %s, %s, %s, %s, CURRENT_DATE )"""
        _PASSENGER_REGISTRATION_SQL = """INSERT INTO Passenger
                           (UserID)
                           VALUES
                           (%s)"""
        USER_RATING_REGISTER_SQL = """INSERT
                                          INTO UserRating
                                          (UserID)
                                          VALUES
                                          (%s)"""
        _USER_EXPERIENCE_REGISTER_SQL = """INSERT INTO Experience
                                           (UserID)
                                           VALUES
                                           (%s)"""
        with DBcm.UseDatabase(config) as cursor:
            try:
                cursor.execute(_USER_REGISTER_SQL, (firstName, lastName, emailAddress, phone, hashedPassword, filename))
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
        with DBcm.UseDatabase(config) as cursor4:
            try:
                cursor4.execute(_USER_EXPERIENCE_REGISTER_SQL, (userID, ))
            except Exception as e:
                print('Error registering user experience:', e)
            else:
                jsObj = json.dumps({"status": "registered"})
                return jsObj


def process_login(email, password):
    _EMAIL_SQL = """SELECT UserID, Email FROM User WHERE Email= %s"""
    _PASSWORD_SQL = """SELECT Password FROM User WHERE Password= %s"""
    _GET_USER_DETAILS_SQL = """SELECT u.UserID, u.First_Name, u.Last_Name,p.PassengerID
                                           FROM User u , Passenger p
                                           WHERE u.UserID = p.UserID
                                           AND u.UserID = %s"""
    _GET_DRIVER_ID_SQL = """SELECT DriverID FROM Driver WHERE UserID = %s"""
    _UPDATE_LOGIN_SQL = """UPDATE User SET Logged_In=1 WHERE UserID= %s"""
    emaildata, passworddata, driverData = [], [], []
    jsObj = {}
    UserID, passengerID, driverID = 0, 0, 0
    uName, uLName = "", ""
    hashedPassword = hashlib.sha256(bytes(password, encoding='utf-8')).hexdigest()
    with DBcm.UseDatabase(config) as cursor:
        try:
            cursor.execute(_EMAIL_SQL, (email,))
            emaildata = cursor.fetchall()
            UserID = emaildata[0][0]
            print('user ID', UserID, 'email', emaildata[0][1])
        except Exception as e:
            print('Error looking up email:', e)
    with DBcm.UseDatabase(config) as cursor1:
        try:
            cursor1.execute(_PASSWORD_SQL, (hashedPassword,))
            passworddata = cursor1.fetchall()
            print('password data:', passworddata)
        except Exception as e:
            print('error looking up password: ', e)
    if emaildata == [] or passworddata == []:
        jsObj = json.dumps({"status": "wrongemail/password"})
    elif email == emaildata[0][1] and hashedPassword == passworddata[0][0]:
        print('in main part ')
        with DBcm.UseDatabase(config) as cursor2:
            try:
                cursor2.execute(_GET_DRIVER_ID_SQL, (UserID,))
                driverData = cursor2.fetchall()
                print('driver data', driverData)
            except Exception as e:
                print('Error getting driver id:', e)
        with DBcm.UseDatabase(config) as cursor3:
            try:
                cursor3.execute(_GET_USER_DETAILS_SQL, (UserID,))
                print('email', email, 'type', type(email))
                data = cursor3.fetchall()
                print('login data: ', data, 'len ', len(data))
                if driverData != []:
                    for i in data:
                        for it in driverData:
                            UserID = i[0]
                            uName = i[1]
                            uLName = i[2]
                            passengerID = i[3]
                            driverID = it[0]
                        print('my driver id', driverID)
                        jsObj = json.dumps(
                            {"status": "match", "email": email, "user_id": UserID, "first_name": uName.capitalize(), "last_name": uLName.capitalize(),
                                "passengerID": passengerID, "myDriverID": driverID})
                else:
                    for i in data:
                        UserID = i[0]
                        uName = i[1]
                        uLName = i[2]
                        passengerID = i[3]
                        driverID = 0
                        jsObj = json.dumps(
                            {"status": "match", "email": email, "user_id": UserID, "first_name": uName.capitalize(), "last_name": uLName.capitalize(),
                             "passengerID": passengerID, "myDriverID": driverID})
            except Exception as e:
                print('error with getting login information: ', e)
            else:
                with DBcm.UseDatabase(config) as cursor4:
                    try:
                        cursor4.execute(_UPDATE_LOGIN_SQL, (UserID,))
                    except Exception as e:
                        print('error executing update:', e)
                    else:
                        return jsObj
    else:
        jsObj = json.dumps({"status": "nomatch"})
    return jsObj


def process_logout(userID):
    print('process logout func', userID)
    with DBcm.UseDatabase(config) as cursor:
        try:
            _SQL = """UPDATE User SET Logged_In=0 WHERE UserID=%s   """
            cursor.execute(_SQL, (userID,))
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
                        distance, departing, seats):
    print('register function', userID, startLat, startLong, startCounty,destinationLat, destinationLong, destinationCounty,
          departing, seats)
    _GETDRIVER_SQL = """SELECT DriverID FROM Driver WHERE UserID= %s """
    _User_Register_SQL = """INSERT INTO Lift
                       (DriverID, Start_Lat, Start_Long, Start_County, Destination_Lat, Destination_Long,
                       Destination_County, Distance, Depart_Date, Available_Spaces,
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
                                            destinationCounty, distance, departing, seats))
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
    carID, driverID = 0, 0
    _CAR_SQL = """INSERT INTO CarDetails
                       (Car_Make, Car_Model, Car_Reg, UserID)
                       VALUES
                       (%s, %s, %s, %s)"""
    _DRIVER_SQL = """INSERT INTO Driver
                        (UserID, CarID)
                        VALUES
                        (%s, %s)"""
    _GET_DRIVER_ID_SQL = """SELECT DriverID FROM Driver WHERE UserID = %s"""
    with DBcm.UseDatabase(config) as cursor:
        try:
            cursor.execute(_CAR_SQL, (carmake_lower, carmodel_lower, reg_lower, userID))
            carID = cursor.lastrowid
        except Exception as e:
            print('Error registering car:', e)
    with DBcm.UseDatabase(config) as cursor1:
        try:
            cursor1.execute(_DRIVER_SQL, (userID, carID))
        except Exception as e:
            print('Error registering user as driver:', e)
    with DBcm.UseDatabase(config) as cursor2:
        try:
            cursor2.execute(_GET_DRIVER_ID_SQL, (userID, ))
            driverData = cursor2.fetchall()
            driverID = driverData[0]
        except Exception as e:
            print('Error getting driver ID:', e)
        else:
            jsObj = json.dumps({"status": "registered", "driverID": driverID})
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
    _GETLIFTDETAILS_SQL = """SELECT l.Depart_Date, l.Start_Lat, l.Start_Long, l.Destination_Lat, l.Destination_Long
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
                        'departing': i[0],
                        'startLat': i[1],
                        'startLng': i[2],
                        'destLat': i[3],
                        'destLng': i[4]
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


# MY GROUPS

def getMyGroups(userID):
    _GROUPDETAIL_SQL = """SELECT c.GroupID, u.First_Name, u.Last_Name, l.LiftID, l.Depart_Date
                          FROM CarGroup c, Driver d, User u, Lift l, Passenger p
                          WHERE c.DriverID = d.DriverID
                          AND u.UserID = d.UserID
                          AND c.LiftID = l.LiftID
                          AND c.PassengerID = p.PassengerID
                          AND p.UserID = %s
                          AND l.LiftID NOT IN
                          (SELECT cl.LiftID FROM CompletedLifts cl, Lift l WHERE cl.LiftID = l.LiftID )"""
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
                    'departing': item[4],
                })
            jsObj = json.dumps(d, default=converter)
        except Exception as e:
            print('Error getting group details:', e)
        else:
            return jsObj


def getGroupDetails(liftID, groupID):
    data, driverData = [], []
    print('lift', liftID, 'group', groupID)
    _GETPASSENGERS_SQL = """SELECT u.First_Name, u.Last_Name, u.Phone_Number, r.Rating, p.PassengerID
                            FROM User u, Passenger p, CarGroup c, UserRating r
                            WHERE c.PassengerID = p.PassengerID
                            AND p.UserID = u.UserID
                            AND u.UserID = r.UserID
                            AND c.LiftID = %s
                           """
    _GETGROUPDETAILS_SQL = """SELECT l.Start_County, l.Destination_County, l.Depart_Date,l.Start_Lat, l.Start_Long,
                              l. Destination_Lat, l.Destination_Long
                                  FROM Lift l, CarGroup c
                                  WHERE c.LiftID = l.LiftID
                                  AND c.GroupID = %s"""
    _GETDRIVERDETAILS_SQL = """SELECT u.First_Name, u.Last_Name, u.Phone_Number, r.Rating, c.Car_Reg, d.DriverID, p.PassengerID
                               FROM User u, CarDetails c, Driver d, CarGroup g, UserRating r, Passenger p
                               WHERE u.UserID = c.UserID
                               AND u.UserID = p.UserID
                               AND u.UserID = d.UserID
                               AND d.DriverID = g.DriverID
                               AND r.UserID = u.UserID
                               AND g.GroupID = %s"""
    with DBcm.UseDatabase(config) as cursor1:
        try:
            cursor1.execute(_GETGROUPDETAILS_SQL, (groupID, ))
            data = cursor1.fetchall()
            print('data', data)

        except Exception as e:
            print('Error getting group details: ', e)
    with DBcm.UseDatabase(config) as cursor2:
        try:
            cursor2.execute(_GETDRIVERDETAILS_SQL, (groupID,))
            driverData = cursor2.fetchall()
            print('driver data', driverData)
        except Exception as e:
            print('Error getting driver details: ', e)
    with DBcm.UseDatabase(config) as cursor3:
        try:
            cursor3.execute(_GETPASSENGERS_SQL, (liftID,))
            passengerData = cursor3.fetchall()
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
                            'driverID': i[5],
                            'driverPassengerID': i[6],
                            'startCounty': item[0],
                            'destCounty': item[1],
                            'departing': item[2],
                            'startLat': item[3],
                            'startLng': item[4],
                            'destLat': item[5],
                            'destLng': item[6],
                            'passengerName': it[0] + ' ' + it[1],
                            'passengerPhone': it[2],
                            'passengerRating': it[3],
                            'passengerID': it[4]
                        })
            jsObj = json.dumps(d, default=converter)
        except Exception as e:
            print('Error getting passenger details: ', e)
        else:
            return jsObj


def get_my_completed_groups(userID):
    d, liftData = [], []
    _MY_COMPLETED_GROUPS_LIST_SQL = """SELECT u.First_Name, u.Last_Name, l.LiftID, l.Depart_Date
                                      FROM CarGroup c, Driver d, User u, Lift l, Passenger p, CompletedLifts cl
                                      WHERE c.DriverID = d.DriverID
                                      AND u.UserID = d.UserID
                                      AND c.LiftID = l.LiftID
                                      AND c.PassengerID = p.PassengerID
                                      AND cl.PassengerID = p.PassengerID
                                      AND cl.LiftID = c.LiftID
                                      AND p.UserID = %s
                                 """
    with DBcm.UseDatabase(config) as cursor:
        try:
            cursor.execute(_MY_COMPLETED_GROUPS_LIST_SQL, (userID,))
            completedGroupData = cursor.fetchall()
            print('completedGroupData', completedGroupData)
            for item in completedGroupData:
                d.append({
                    'driverName': item[0] + ' ' + item[1],
                    'liftID': item[2],
                    'departed': item[3]
                })
        except Exception as e:
            print('Error getting completed groups:', e)
        else:

            return json.dumps(d, default=converter)

# MY LIFTS


def getMyCompletedLifts(userID):
    d, liftData = [], []
    _MY_COMPLETED_LIFT_LIST_SQL = """SELECT l.LiftID, l.Start_County, l.Destination_County, l.Depart_Date
                             FROM Lift l, Driver d, CompletedLifts c
                             WHERE c.DriverID = d.DriverID
                             AND c.LiftID = l.LiftID
                             AND d.UserID = %s
                             """
    with DBcm.UseDatabase(config) as cursor:
        try:
            cursor.execute(_MY_COMPLETED_LIFT_LIST_SQL, (userID, ))
            liftData = cursor.fetchall()
            print('lift data', liftData)
        except Exception as e:
            print('Error getting completed lifts:', e)
        else:
            for item in liftData:
                d.append({
                    'liftID': item[0],
                    'route': item[1] + ' to ' + item[2],
                    'departing': item[3],
                })
            return json.dumps(d, default=converter)



def getMyLifts(userID):
    now = datetime.datetime.now()
    day = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M")
    _LIFTDETAIL_SQL = """SELECT l.LiftID, l.Start_County, l.Destination_County, l.Depart_Date
                             FROM Lift l, Driver d
                             WHERE l.DriverID = d.DriverID
                             AND l.Depart_Date > %s
                             AND d.UserID = %s
                             AND l.LiftID NOT IN
                             (SELECT LiftID FROM CompletedLifts cl WHERE cl.LiftID = l.LiftID)"""
    with DBcm.UseDatabase(config) as cursor:
        try:
            cursor.execute(_LIFTDETAIL_SQL, (day, userID,))
            data = cursor.fetchall()
            print('data', data)
            d = []
            for item in data:
                d.append({
                    'userID': userID,
                    'liftID': item[0],
                    'route': item[1] + ' to ' + item[2],
                    'departing': item[3],
                })
            jsObj = json.dumps(d, default=converter)
        except Exception as e:
            print('Error getting lift list details:', e)
        else:
            return jsObj


def getMyLiftDetails(liftID):
    d, passengerData, liftData = [], [], []
    numOfPassengers = 0
    _GETPASSENGERS_SQL = """SELECT u.First_Name, u.Last_Name, u.Phone_Number, r.Rating, p.PassengerID
                            FROM User u, Passenger p, CarGroup c, UserRating r
                            WHERE c.PassengerID = p.PassengerID
                            AND r.UserID = p.UserID
                            AND p.UserID = u.UserID
                            AND c.LiftID = %s"""
    _GETMYLIFTDETAILS_SQL = """SELECT l.*, cd.Car_Reg, u.First_Name, u.Last_Name, r.Rating, p.PassengerID
                                FROM Lift l, CarDetails cd, Driver d, User u, UserRating r, Passenger p
                                WHERE l.LiftID = %s
                                AND l.DriverID = d.DriverID
                                AND d.UserID = u.UserID
                                AND r.UserID = u.UserID
                                AND d.UserID = cd.UserID
                                AND u.UserID = p.UserID"""
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
            liftData = cursor.fetchall()
            print('data', liftData)
            numOfPassengers = len(passengerData)
            print('number of passengers: ', numOfPassengers)
            if passengerData != []:
                print('has passengers')
                for item in liftData:
                    for i in passengerData:
                        d.append({
                            'liftID': liftID,
                            'startLat': item[2],
                            'startLng': item[3],
                            'startCounty': item[4],
                            'destLat': item[5],
                            'destLng': item[6],
                            'destCounty': item[7],
                            'distance': item[8],
                            'departing': item[9],
                            'spaces': item[10],
                            'created': item[11],
                            'car reg': item[12],
                            'driverName': item[13] + ' ' + item[14],
                            'driverRating': item[15],
                            'driverPassengerID': item[16],
                            'passengerName': i[0] + ' ' + i[1],
                            'passengerPhone': i[2],
                            'passengerRating': i[3],
                            'passengerID': i[4],
                            'numOfPassengers': numOfPassengers
                        })
            else:
                print('has no passengers')
                for item in liftData:
                    d.append({
                        'liftID': liftID,
                        'startLat': item[2],
                        'startLng': item[3],
                        'startCounty': item[4],
                        'destLat': item[5],
                        'destLng': item[6],
                        'destCounty': item[7],
                        'distance': item[8],
                        'departing': item[9],
                        'spaces': item[10],
                        'created': item[11],
                        'car reg': item[12],
                        'driverName': item[13] + ' ' + item[14],
                        'driverRating': item[15],
                        'driverPassengerID': item[16],
                        'passengerName': 'None',
                        'passengerPhone': 'None'
                    })
            jsObj = json.dumps(d, default=converter)
        except Exception as e:
            print('Error getting my lift details:', e)
        else:
            return jsObj


def check_can_delete(liftID):
    group_data = []
    _CHECK_IF_ACTIVE_SQL = """SELECT * FROM CarGroup WHERE LiftID = %s"""
    with DBcm.UseDatabase(config) as cursor:
        try:
            cursor.execute(_CHECK_IF_ACTIVE_SQL, (liftID,))
            group_data = cursor.fetchall()
            print('group data', group_data)
        except Exception as e:
            print('Error checking if lift is active:', e)
        else:
            if group_data == []:
                return json.dumps({'active': 'false'})
            else:
                return json.dumps({'active': 'true'})

def delete_lift(liftID):
    _DELETE_LIFT_SQL= """DELETE FROM Lift WHERE LiftID = %s"""
    with DBcm.UseDatabase(config) as cursor:
        try:
            cursor.execute(_DELETE_LIFT_SQL, (liftID,))
        except Exception as e:
            print('Error deleting lift:', e)
        else:
            return json.dumps({'status': 'deleted'})

def complete_lift(liftID):
    print('COMPLETE LIFT FUNCTION')
    d, passengerIDs, driverIdData, distance_data = [], [], [], []
    driverID, driverIdForCompletedLift = 0, 0
    distance = 0.0
    # query to get drivers id to insert into completed lifts
    _GET_DRIVER_ID_SQL = """SELECT DISTINCT c.DriverID
                        FROM Driver d, CarGroup c
                        WHERE c.DriverID = d.DriverID
                         AND c.LiftID = %s
                        """
    _GET_PASSENGER_IDS_SQL ="""SELECT DISTINCT c.PassengerID
                                FROM Passenger p, CarGroup c
                                 WHERE c.PassengerID = p.PassengerID
                                 AND c.LiftID = %s"""
    _GET_DISTANCE_SQL = """SELECT Distance FROM Lift WHERE LiftID = %s"""
    _INSERT_COMPLETED_LIFT_DRIVER_SQL = """INSERT INTO CompletedLifts (LiftID, DriverID, Distance_Kilometers)
                                VALUES (%s, %s, %s)"""
    _INSERT_COMPLETED_LIFT_PASSENGERS_SQL = """INSERT INTO CompletedLifts (LiftID, PassengerID, Distance_Kilometers)
                                                VALUES (%s, %s, %s)"""

    with DBcm.UseDatabase(config) as cursor1:
        try:
            cursor1.execute(_GET_DRIVER_ID_SQL, (liftID, ))
            driverIdData = cursor1.fetchall()
            print('driver ID data', driverIdData)
            driverIdForCompletedLift = driverIdData[0][0]
            print('driver id for complete lift', driverIdForCompletedLift)
        except Exception as e:
            print('Error getting driver user ID for insert:', e)
    with DBcm.UseDatabase(config) as cursor2:
        try:
            cursor2.execute(_GET_DISTANCE_SQL, (liftID, ))
            distance_data = cursor2.fetchall()
            distance = distance_data[0][0]
        except Exception as e:
            print('Error getting distance information:', e)
    if driverIdData:
        with DBcm.UseDatabase(config) as cursor3:
            try:
                cursor3.execute(_INSERT_COMPLETED_LIFT_DRIVER_SQL, (liftID, driverIdForCompletedLift, distance))
            except Exception as e:
                print('Error inserting driver to completed Lifts:', e)
    with DBcm.UseDatabase(config) as cursor4:
        try:
            cursor4.execute(_GET_PASSENGER_IDS_SQL, (liftID, ))
            passengerIDsData = cursor4.fetchall()
            print('passenger IDs:', passengerIDsData)
            for item in passengerIDsData:
                passengerIDs.append(item[0])
            print('passenger IDs: ', passengerIDs)
        except Exception as e:
            print('Error getting passenger IDs:', e)
    with DBcm.UseDatabase(config) as cursor5:
        try:
            for item in passengerIDs:
                print('item in passengerIDs ', item)
                cursor5.execute(_INSERT_COMPLETED_LIFT_PASSENGERS_SQL, (liftID, item, distance))
        except Exception as e:
            print('Error inserting passengers to completed Lifts:', e)
        else:
            return json.dumps({'completed lift registering': 'complete'})


def pop_ratings_table(liftID, userID):
    groupData, driverdata, d = [], [], []
    driverID = 0
    _GET_CAR_GROUP_SQL = """SELECT DISTINCT c.PassengerID, u.First_Name, u.Last_Name
                        FROM User u, Passenger p, CarGroup c, Lift l
                          WHERE c.PassengerID = p.PassengerID
                            AND p.UserID = u.UserID
                            AND l.LiftID = c.LiftID
                            AND p.UserID NOT IN
                                (SELECT u.UserID
                                FROM User u, CarGroup c, Passenger p
                                WHERE c.LiftID = %s
                                AND c.PassengerID = p.PassengerID
                                AND p.UserID = u.UserID
                                AND u.UserID = %s)
                            AND l.LiftID = %s
                      """
    # query to filter list, if the user is the driver
    _GET_DRIVER_SQL ="""SELECT DISTINCT c.DriverID, u.First_Name, u.Last_Name
                        FROM Driver d, CarGroup c, Lift l, User u
                        WHERE c.DriverID = d.DriverID
                        AND d.UserID = u.UserID
                         AND d.UserID NOT IN
                                (SELECT u.UserID
                                FROM User u, CarGroup c, Driver d
                                WHERE c.LiftID = %s
                                AND c.DriverID = d.DriverID
                                AND d.UserID = u.UserID
                                AND u.UserID = %s)
                         AND c.LiftID = %s"""
    with DBcm.UseDatabase(config) as cursor:
        try:
            cursor.execute(_GET_CAR_GROUP_SQL, (liftID, userID, liftID))
            groupData = cursor.fetchall()
            print('groupdata ', groupData)
        except Exception as e:
            print('Error getting car group details:', e)
    with DBcm.UseDatabase(config) as cursor2:
            try:
                cursor2.execute(_GET_DRIVER_SQL, (liftID, userID, liftID ))
                driverdata = cursor2.fetchall()
                if driverdata != []:
                    driverID = driverdata[0][0]
                    print('driver data', driverdata, 'driverID', driverID)
                    if groupData != []:
                        for item in groupData:
                            for i in driverdata:
                                d.append({
                                    'passengerID': item[0],
                                    'passengerName': item[1] + ' ' + item[2],
                                    'driverID': i[0],
                                    'driverName': i[1] + ' ' + i[2],
                                })
                    else:
                        for i in driverdata:
                            d.append({
                                'passengerID': 'None',
                                'passengerName': 'None',
                                'driverID': i[0],
                                'driverName': i[1] + ' ' + i[2],
                            })
                else:
                    for item in groupData:
                            d.append({
                                'passengerID': item[0],
                                'passengerName': item[1] + ' ' + item[2],
                                'driverID': 'None',
                                'driverName': 'None',
                            })
                return json.dumps(d, default=converter)
            except Exception as e:
                print('Error getting car group driver:', e)





def rate_group(driverID, driverRating, passengerData):
    # driverStar, passengerStar = '', ''
    star = ''
    driverStarCount, passengerStarCount = 0, 0
    driverUserID, passengerUserID, passengerRating = 0, 0, 0
    driverStars = {}
    if driverRating != 0:
        star = str(driverRating)
    passengerStar = str(3)
    _GET_DRIVER_USERID_SQL = """SELECT UserID FROM Driver WHERE DriverID = %s"""
    _UPDATE_DRIVER_STAR_COUNT_SQL = """UPDATE UserRating
                              SET """ + star + """_Star =  """ + star + """_Star + 1,
                              Number_of_Ratings = Number_of_Ratings +1
                              WHERE UserID = %s"""
    _GET_PASSENGERS_USERID_SQL = """SELECT UserID FROM Passenger WHERE PassengerID = %s"""

    _GET_STAR_COUNT_SQL = """SELECT 1_Star, 2_Star, 3_Star, 4_Star, 5_Star FROM UserRating WHERE UserID = %s"""
    _UPDATE_RATING_SQL = """UPDATE UserRating
                                    SET rating = %s
                                    WHERE UserID = %s"""
    try:
        if driverID != 0:
            with DBcm.UseDatabase(config) as cursor:
                try:
                    cursor.execute(_GET_DRIVER_USERID_SQL, (driverID, ))
                    driverData = cursor.fetchall()
                    driverUserID = driverData[0][0]
                except Exception as e:
                    print('Error getting drivers UserID:', e)
            with DBcm.UseDatabase(config) as cursor:
                try:
                    cursor.execute(_UPDATE_DRIVER_STAR_COUNT_SQL, (driverUserID, ))
                except Exception as e:
                    print('Error updating driver star count:', e)
            with DBcm.UseDatabase(config) as cursor:
                try:
                    cursor.execute(_GET_STAR_COUNT_SQL, (driverUserID,))
                    driverStarCountData = cursor.fetchall()
                    for item in driverStarCountData:
                        driverStars = {
                            '1': item[0],
                            '2': item[1],
                            '3': item[2],
                            '4': item[3],
                            '5': item[4]
                        }
                    driverRating = calculateRating(driverStars)
                    print('driver rating: ', driverRating)
                except Exception as e:
                    print('Error getting driver star count:', e)
            with DBcm.UseDatabase(config) as cursor:
                try:
                    cursor.execute(_UPDATE_RATING_SQL, (driverRating, driverUserID))
                except Exception as e:
                    print('Error updating driver rating:', e)
        for item in passengerData:
            star = str(item[1])
            print('star', star, 'type', type(star))
            _UPDATE_PASSENGER_STAR_COUNT_SQL = """UPDATE UserRating
                                             SET """ + star + """_Star =  """ + star + """_Star + 1,
                                             Number_of_Ratings = Number_of_Ratings +1
                                             WHERE UserID = %s"""
            with DBcm.UseDatabase(config) as cursor:
                try:
                    print('passenger id', item[0])
                    cursor.execute(_GET_PASSENGERS_USERID_SQL, (item[0],))
                    passengerData = cursor.fetchall()
                    passengerUserID = passengerData[0][0]
                    print('passenger userID', passengerUserID)
                except Exception as e:
                    print('Error getting passengers UserID:', e)
            with DBcm.UseDatabase(config) as cursor:
                try:
                    cursor.execute(_UPDATE_PASSENGER_STAR_COUNT_SQL, (passengerUserID, ))
                except Exception as e:
                    print('Error updating passenger star count:', e)
            with DBcm.UseDatabase(config) as cursor:
                try:
                    cursor.execute(_GET_STAR_COUNT_SQL, (passengerUserID,))
                    passengerStarCountData = cursor.fetchall()
                    print('passenger star count data', passengerStarCountData)
                    for i in passengerStarCountData:
                        passengerStars = {
                            '1': i[0],
                            '2': i[1],
                            '3': i[2],
                            '4': i[3],
                            '5': i[4]
                        }
                    print('passenger star dict', passengerStars)
                    passengerRating = calculateRating(passengerStars)
                    print('passenger rating: ', passengerRating)
                except Exception as e:
                    print('Error getting passenger star count:', e)
            with DBcm.UseDatabase(config) as cursor:
                try:
                    cursor.execute(_UPDATE_RATING_SQL, (passengerRating, passengerUserID))
                except Exception as e:
                    print('Error updating passenger rating:', e)
    except Exception as e:
        print('Error with rating function:', e)
    else:
        return json.dumps({'ratings': 'complete'})


def calculateRating(starCountData):
    # weighted average
    return (5*starCountData['5'] + 4 * starCountData['4'] + 3 * starCountData['3'] + 2 * starCountData['2'] + 1 *
            starCountData['1']) / (starCountData['5'] + starCountData['4'] + starCountData['3'] + starCountData['2']
                                   + starCountData['1'])


def check_if_user_is_driver(liftID, driverID):
    driverData, distanceData = [], []
    # see if user was the driver
    _SEE_IF_USER_IS_DRIVER_SQL = """SELECT DriverID FROM CarGroup
                                    WHERE LiftID = %s
                                    AND DriverID = %s"""
    _GET_DISTANCE_SQL = """SELECT Distance FROM Lift WHERE LiftID = %s"""
    with DBcm.UseDatabase(config) as cursor:
        try:
            cursor.execute(_GET_DISTANCE_SQL, (liftID, ))
            distanceData = cursor.fetchall()
            print('driver data', driverData)
        except Exception as e:
            print('Error checking if user is the driver:', e)
    with DBcm.UseDatabase(config) as cursor1:
        try:
            cursor1.execute(_SEE_IF_USER_IS_DRIVER_SQL, (liftID, driverID))
            driverData = cursor1.fetchall()
            print('driver data', driverData)
        except Exception as e:
            print('Error checking if user is the driver:', e)
        else:
            if driverData != []:
                for item in distanceData:
                    return json.dumps({'is driver': 'true', 'distance': str(item[0])})
            else:
                for i in distanceData:
                    return json.dumps({'is driver': 'false', 'distance': str(i[0])})


def get_user_experience(userID, newExp, distance, numOfPassengers):
    experienceData, d = [], []
    _UPDATE_EXPERIENCE_SQL = """UPDATE Experience
                                SET Experience = Experience + %s, Overall_Distance_kilo = Overall_Distance_kilo + %s, Overall_Passengers = Overall_Passengers + %s
                                WHERE UserID = %s"""
    _GET_NEW_EXPERIENCE_SQL = """SELECT Overall_Distance_kilo, Overall_Passengers, Experience
                                 FROM Experience
                                 WHERE UserID = %s"""
    with DBcm.UseDatabase(config) as cursor:
        try:
            cursor.execute(_UPDATE_EXPERIENCE_SQL, (newExp, distance, numOfPassengers, userID))
        except Exception as e:
            print('Error updating users experience:', e)
    with DBcm.UseDatabase(config) as cursor1:
        try:
            cursor1.execute(_GET_NEW_EXPERIENCE_SQL, (userID, ))
            experienceData = cursor1.fetchall()
        except Exception as e:
            print('Error getting users experience: ', e)
        else:
            for item in experienceData:
                d.append({
                    'overall distance': item[0],
                    'overallpassengers': item[1],
                    'experience': item[2]
                })
            return json.dumps(d, default=converter)


# ACTIVE LIFT


def get_driver_id(liftID):
    _GET_DRIVER_ID_SQL ="""SELECT DriverID FROM Lift WHERE LiftID = %s"""
    with DBcm.UseDatabase(config) as cursor:
        try:
            cursor.execute(_GET_DRIVER_ID_SQL, (liftID,))
            data = cursor.fetchall()
        except Exception as e:
            print('Error getting driver ID for lift:', e)
        else:
            return json.dumps({'driverID': data[0][0]})


def check_if_lift_finished(liftID):
    _CHECK_IF_LIFTID_IN_COMPLETED_SQL = """SELECT  * FROM CompletedLifts WHERE LiftID = %s"""
    with DBcm.UseDatabase(config) as cursor:
        try:
            cursor.execute(_CHECK_IF_LIFTID_IN_COMPLETED_SQL, (liftID,))
            data = cursor.fetchall()
        except Exception as e:
            print('Error checking if liftID in CompletedLifts table:', e)
        else:
            if data != []:
                return json.dumps({"status": "lift finished"})
            else:
                return json.dumps({"status": "not finished"})


def get_profile(user_id):
    car_data, user_data = [], []
    _GET_USER_DETAILS_SQL = """SELECT u.First_Name, u.Last_Name, u.Email, u.Phone_Number, u.Date_Created, r.Rating,
                                r.Number_of_Ratings, e.Experience, e.Overall_Distance_kilo, e.Overall_Passengers
                                FROM User u, UserRating r, Experience e
                                WHERE u.UserID = r.UserID
                                AND u.UserID = e.UserID
                                AND u.UserID = %s"""
    _GET_CAR_DETAILS_SQL = """SELECT Car_Make, Car_Model, Car_Reg FROM CarDetails WHERE UserID = %s"""
    with DBcm.UseDatabase(config) as cursor:
        try:
            cursor.execute(_GET_CAR_DETAILS_SQL, (user_id, ))
            car_data = cursor.fetchall()
        except Exception as e:
            print('Error getting users car information:', e)
    with DBcm.UseDatabase(config) as cursor1:
        try:
            cursor1.execute(_GET_USER_DETAILS_SQL, (user_id, ))
            user_data = cursor1.fetchall()
        except Exception as e:
            print('Error getting user profile information:', e)
        else:
            if car_data != []:
                for item in user_data:
                    for i in car_data:
                        return json.dumps({
                            'name': item[0] + ' ' + item[1],
                            'email': item[2],
                            'phone': item[3],
                            'created': item[4],
                            'rating': item[5],
                            'numOfRatings': item[6],
                            'experience': item[7],
                            'overallDistance': item[8],
                            'overallPassengers': item[9],
                            'carMake': i[0],
                            'carModel': i[1],
                            'carReg': i[2]
                        }, default=converter)
            else:
                for item in user_data:
                    return json.dumps({
                        'name': item[0] + ' ' + item[1],
                        'email': item[2],
                        'phone': item[3],
                        'created': item[4],
                        'rating': item[5],
                        'numOfRatings': item[6],
                        'experience': item[7],
                        'overallDistance': item[8],
                        'overallPassengers': item[9],
                        'carMake': 'None'
                    }, default=converter)


def get_picture(user_id):
    _GET_PICTURE_PATH_SQL = """SELECT Pic_Path FROM User WHERE UserID = %s"""
    with DBcm.UseDatabase(config) as cursor:
        try:
            cursor.execute(_GET_PICTURE_PATH_SQL, (user_id,))
            data = cursor.fetchall()
            print('data', data)
        except Exception as e:
            print('Error getting users car information:', e)
        else:
            return data[0][0]


def get_user_id(passenger_id):
    _GET_USER_ID_SQL = """SELECT UserID from Passenger WHERE PassengerID =%s"""
    with DBcm.UseDatabase(config) as cursor:
        try:
            cursor.execute(_GET_USER_ID_SQL, (passenger_id,))
            data = cursor.fetchall()
        except Exception as e:
            print('Error getting user ID:', e)
        else:
            return json.dumps({'userID': data[0][0]})


def update_details(user_id, phone, car_make, car_model, car_reg):
    car_data = []
    _UPDATE_PHONE_SQL = """UPDATE User SET Phone_Number = %s WHERE UserID = %s"""
    _CHECK_IF_CAR_REGISTERED_SQL ="""SELECT * FROM CarDetails WHERE UserID = %s"""
    _UPDATE_CAR_SQL = """UPDATE CarDetails SET Car_Make = %s, Car_Model = %s, Car_Reg = %s WHERE UserID = %s"""
    with DBcm.UseDatabase(config) as cursor:
        try:
            cursor.execute(_UPDATE_PHONE_SQL, (phone, user_id))
            print('update done')
        except Exception as e:
            print('Error updating user information:', e)
    with DBcm.UseDatabase(config) as cursor1:
        try:
            cursor1.execute(_CHECK_IF_CAR_REGISTERED_SQL, (user_id, ))
            car_data = cursor1.fetchall()
        except Exception as e:
            print('Error check if car exists:', e)
    if car_make != "" and car_data != []:
        print('in car update')
        with DBcm.UseDatabase(config) as cursor2:
            try:
                cursor2.execute(_UPDATE_CAR_SQL, (car_make, car_model, car_reg, user_id))
            except Exception as e:
                print('Error updating car details:', e)
    return json.dumps({'update': 'complete'})


def delete_user_account(user_id):
    driver_data = []
    driver_id = 0
    _CHECK_IF_DRIVER_SQL = """SELECT DriverID FROM Driver WHERE UserID = %s"""
    _DELETE_DRIVER_LIFT_SQL = """DELETE FROM Lift WHERE DriverID = %s"""
    _DELETE_DRIVER_CAR_SQL = """DELETE FROM CarDetails WHERE UserID = %s"""
    _DELETE_DRIVER_SQL = """DELETE FROM Driver WHERE UserID = %s"""


    _DELETE_USERRATING_SQL = """DELETE FROM UserRating WHERE UserID = %s"""
    _DELETE_Passenger_SQL = """DELETE FROM Passenger WHERE UserID = %s"""
    _DELETE_EXPERIENCE_SQL = """DELETE FROM Experience WHERE UserID = %s"""
    _DELETE_USER_SQL = """DELETE FROM User WHERE UserID = %s"""
    with DBcm.UseDatabase(config) as cursor:
        try:
            cursor.execute(_CHECK_IF_DRIVER_SQL, (user_id, ))
            driver_data = cursor.fetchall()
            driver_id = driver_data[0][0]
            print('driver id', driver_id)
        except Exception as e:
            print('Error checking if a driver:', e)
    if driver_data != []:
        print('is a driver')
        with DBcm.UseDatabase(config) as cursor:
            try:
                cursor.execute(_DELETE_DRIVER_LIFT_SQL, (driver_id,))
            except Exception as e:
                print('Error deleting user and driver data:', e)
        with DBcm.UseDatabase(config) as cursor:
            try:
                cursor.execute(_DELETE_DRIVER_CAR_SQL, (user_id,))
            except Exception as e:
                print('Error deleting user and driver data:', e)
        with DBcm.UseDatabase(config) as cursor:
            try:
                cursor.execute(_DELETE_DRIVER_SQL, (user_id,))
            except Exception as e:
                print('Error deleting user and driver data:', e)
        with DBcm.UseDatabase(config) as cursor:
            try:
                cursor.execute(_DELETE_USERRATING_SQL, (user_id,))
            except Exception as e:
                print('Error deleting user and driver data:', e)
        with DBcm.UseDatabase(config) as cursor:
            try:
                cursor.execute(_DELETE_Passenger_SQL, (user_id,))
            except Exception as e:
                print('Error deleting user passenger data:', e)
        with DBcm.UseDatabase(config) as cursor:
            try:
                cursor.execute(_DELETE_EXPERIENCE_SQL, (user_id,))
            except Exception as e:
                print('Error deleting user experience data:', e)
        with DBcm.UseDatabase(config) as cursor:
            try:
                cursor.execute(_DELETE_USER_SQL, (user_id,))
            except Exception as e:
                print('Error deleting user  data:', e)
    else:
        print('is a passenger')
        with DBcm.UseDatabase(config) as cursor:
            try:
                cursor.execute(_DELETE_USERRATING_SQL, (user_id,))
            except Exception as e:
                print('Error deleting user rating data:', e)
        with DBcm.UseDatabase(config) as cursor:
            try:
                cursor.execute(_DELETE_Passenger_SQL, (user_id,))
            except Exception as e:
                print('Error deleting user passenger data:', e)
        with DBcm.UseDatabase(config) as cursor:
            try:
                cursor.execute(_DELETE_EXPERIENCE_SQL, (user_id,))
            except Exception as e:
                print('Error deleting user experience data:', e)
        with DBcm.UseDatabase(config) as cursor:
            try:
                cursor.execute(_DELETE_USER_SQL, (user_id,))
            except Exception as e:
                print('Error deleting user  data:', e)
    return json.dumps({'status': 'complete'})



def get_leaderboard():
    d =[]
    _GET_USERS_SQL_ = """SELECT u.First_Name, u.Last_Name, p.PassengerID, e.Experience
                         FROM User u, Passenger p, Experience e
                         WHERE u.UserID = p.UserID
                         AND u.UserID = e.UserID
                         ORDER BY e.Experience DESC"""
    with DBcm.UseDatabase(config) as cursor:
        try:
            cursor.execute(_GET_USERS_SQL_)
            data = cursor.fetchall()
            print(data)
            for item in data:
                d.append({
                    'name': item[0] + ' ' + item[1],
                    'passengerID': item[2],
                    'experience': str(item[3])
                })
        except Exception as e:
            print('Error check if car exists:', e)
        else:
            return json.dumps(d)
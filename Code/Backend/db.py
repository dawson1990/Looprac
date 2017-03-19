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
def list_available_lifts(passengerID):
    data, requestData = [], []
    # _CHECKIFREQUESTED_SQL = """SELECT LiftID FROM Request WHERE PassengerID = %s"""
    _SQL = """SELECT LiftID, DriverID,Start_County, Destination_County, Depart_Date, Depart_Time FROM Lift
              WHERE  Available_Spaces > 0
              AND LiftID NOT IN
              (SELECT LiftID FROM Request WHERE PassengerID = %s)"""
    with DBcm.UseDatabase(config) as cursor:
        try:
            cursor.execute(_SQL, (passengerID,))
            data = cursor.fetchall()
            print('data', data)
        except Exception as e:
            print('Error with select lift details query: ', e)
    d = []
    for item in data:
        print(item, 'appended')
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


def converter(obj):
    return str(obj)


def getLiftDetails(liftID, driverID):
    print('liftID', liftID, 'driverID', driverID)
    _SELECT = """ SELECT u.UserID, u.First_Name, u.Last_Name
                  FROM User u, Driver d
                  WHERE u.UserID = d.UserID
                  AND d.DriverID= %s"""
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
                'startLat': item[2],
                'startLng': item[3],
                'startCounty': item[4],
                'destinationLat': item[5],
                'destinationLng': item[6],
                'destinationCounty': item[7],
                'departDate': item[8],
                'returnDate': item[9],
                'departTime': item[10],
                'returnTime': item[11],
                'seats': item[12],
                'liftType': item[13],
                'created': item[14]
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
    data, liftData = [], []
    _GETPASSENGERDETAILS_SQL ="""SELECT u.First_Name, u.Last_Name, u.Phone_Number, p.PassengerID
                                  FROM User u, Passenger p, Request r
                                  WHERE u.UserID = p.UserID
                                  AND p.passengerID = r.PassengerID
                                  AND r.requestID = %s"""
    _GETLIFTDETAILS_SQL = """SELECT l.Depart_Date, l.Depart_Time FROM Lift l, Request r
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
    jsObj = json.dumps({'passengerID': data[0][3], 'name': data[0][0] + ' ' + data[0][1], 'phoneNum': data[0][2],
                        'date': liftData[0][0], 'time': liftData[0][1]}, default=converter)
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
    _GETPASSENGERS_SQL = """SELECT u.First_Name, u.Last_Name, u.Phone_Number FROM User u, Passenger p, CarGroup c
                            WHERE c.PassengerID = p.PassengerID
                            AND p.UserID = u.UserID
                            AND c.LiftID = %s
                           """
    _GETGROUPDETAILS_SQL = """SELECT l.Start_County, l.Destination_County, l.Depart_Date, l.Depart_Time, l.Return_Date,
                                  l.Return_Time, l.Start_Lat, l.Start_Long, l. Destination_Lat, l.Destination_Long
                                  FROM Lift l, CarGroup c
                                  WHERE c.LiftID = l.LiftID
                                  AND c.GroupID = %s"""
    _GETDRIVERDETAILS_SQL = """SELECT u.First_Name, u.Last_Name, u.Phone_Number, c.Car_Reg
                               FROM User u, CarDetails c, Driver d, CarGroup g
                               WHERE u.UserID = c.UserID
                               AND u.UserID = d.UserID
                               AND d.DriverID = g.DriverID
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
                            'carReg': i[3],
                            'startCounty': item[0],
                            'destCounty': item[1],
                            'departDate': item[2],
                            'departTime': item[3],
                            'returnDate': item[4],
                            'returnTime': item[5],
                            'startLat': item[6],
                            'startLng': item[7],
                            'destLat': item[8],
                            'destLng': item[9],
                            'passengerName': it[0] + ' ' + it[1],
                            'passengerPhone': it[2]
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
    _GETPASSENGERS_SQL = """SELECT u.First_Name, u.Last_Name, u.Phone_Number
                            FROM User u, Passenger p, CarGroup c
                            WHERE c.PassengerID = p.PassengerID
                            AND p.UserID = u.UserID
                            AND c.LiftID = %s"""
    _GETMYLIFTDETAILS_SQL = """SELECT l.*
                                FROM Lift l
                                WHERE LiftID = %s"""
    # _GETMYLIFTDETAILS_SQL = """SELECT l.*, u.First_Name, u.Last_Name, u.Phone_Number
    #                             FROM Lift l, User u, CarGroup c, Passenger p
    #                             WHERE c.PassengerID = p.PassengerID
    #                             AND p.UserID = u.UserID
    #                             AND l.LiftID = c.LiftID
    #                             AND l.LiftID = %s"""
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
                            'returnDate': item[9],
                            'departTime': item[10],
                            'returnTime': item[11],
                            'spaces': item[12],
                            'type': item[13],
                            'created': item[14],
                            'passengerName': i[0] + ' ' + i[1],
                            'passengerPhone': i[2]
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
                        'returnDate': item[9],
                        'departTime': item[10],
                        'returnTime': item[11],
                        'spaces': item[12],
                        'type': item[13],
                        'created': item[14],
                        'passengerName': 'None',
                        'passengerPhone': 'None'
                    })
            jsObj = json.dumps(d, default=converter)
        except Exception as e:
            print('Error getting my lift details:', e)
        else:
            return jsObj
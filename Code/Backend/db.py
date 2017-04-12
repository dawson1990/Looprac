import DBcm
import json
import hashlib
import datetime
import data_utils

config = {
    'host': 'Looprac.mysql.pythonanywhere-services.com',
    'user': 'Looprac',
    'password': 'itcarlow',
    'database': 'Looprac$LoopracDB'
}


def get_main_page_lifts(passenger_id):
    js_obj = {}
    d = []
    now = datetime.datetime.now()
    time = now.strftime("%Y-%m-%d %H:%M:%S")
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
            cursor.execute(_FILTERLIFTLIST_SQL, (time, passenger_id, passenger_id ))
            data = cursor.fetchall()
            if data != []:
                for item in data:
                    d.append({
                        'availablelifts': 'yes',
                        'liftID': item[0],
                        'driverID': item[1],
                        'startLat': item[2],
                        'startLng': item[3],
                    })
                    js_obj = json.dumps(d, default=converter)
            else:
                js_obj = json.dumps({"availablelifts": "none"})
        except Exception as e:
            print('Error with select lift details that user hasnt requested query: ', e)
        else:
            return js_obj


# QUERY TO DISPLAY AVAILABLE LIFTS
def list_available_lifts(passenger_id):
    data, data2, d = [], [], []
    now = datetime.datetime.now()
    time = now.strftime("%Y-%m-%d %H:%M:%S")
    # Query that filters available lifts to only display lifts that have available spaces, they user hasn't already
    # requested or if the user is a driver, not to show their lifts
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
            cursor.execute(_FILTERLIFTLIST_SQL, (time, passenger_id, passenger_id))
            data = cursor.fetchall()
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
    js_obj = json.dumps(d, default=converter)
    return js_obj


# for JSON obj, if json.dumps() receives an object it can't process, its sent to this function and converted to str
def converter(obj):
    return str(obj)


def getLiftDetails(lift_id, driver_id):
    _DRIVER_DETAILS_SQL = """ SELECT u.UserID, u.First_Name, u.Last_Name, r.Rating, p.PassengerID
                  FROM User u, Driver d, UserRating r, Passenger p
                  WHERE u.UserID = d.UserID
                  AND u.UserID = p.UserID
                  AND r.UserID = u.UserID
                  AND d.DriverID= %s"""
    _LIFT_DETAILS_SQL = """SELECT * FROM Lift WHERE LiftID= %s order by Created_At"""
    with DBcm.UseDatabase(config) as cursor:
        cursor.execute(_LIFT_DETAILS_SQL, (lift_id,))
        data = cursor.fetchall()
    with DBcm.UseDatabase(config) as cursor:
        cursor.execute(_DRIVER_DETAILS_SQL, (driver_id,))
        user_details = cursor.fetchall()
    d = []
    for item in data:
        for i in user_details:
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
    js_obj = json.dumps(d, default=converter)
    return js_obj


def register(f_name, l_name, email_addr, phone_n, passw, filename):
    js_obj = {}
    user_id = 0
    first_name = f_name.lower()
    last_name = l_name.lower()
    phone = str(phone_n)
    email_address = email_addr.lower()
    hashed_password = hashlib.sha256(bytes(passw, encoding='utf-8')).hexdigest()
    email_exists = check_if_exists(email_address)
    if email_exists is True:
        js_obj = json.dumps({"status": "email exists"})
        return js_obj
    else:
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
                cursor.execute(_USER_REGISTER_SQL, (first_name, last_name, email_address, phone, hashed_password, filename))
                user_id = cursor.lastrowid
            except Exception as e:
                print('Error registering user to User table:', e )
        with DBcm.UseDatabase(config) as cursor:
            try:
                cursor.execute(_PASSENGER_REGISTRATION_SQL, (user_id,))
            except Exception as e:
                print('Error adding user to Passenger table', e)
        with DBcm.UseDatabase(config) as cursor:
            try:
                cursor.execute(USER_RATING_REGISTER_SQL, (user_id,))
            except Exception as e:
                print('Error registering user rating:', e)
        with DBcm.UseDatabase(config) as cursor4:
            try:
                cursor4.execute(_USER_EXPERIENCE_REGISTER_SQL, (user_id, ))
            except Exception as e:
                print('Error registering user experience:', e)
            else:
                js_obj = json.dumps({"status": "registered"})
                return js_obj


def process_login(email, password):
    _EMAIL_SQL = """SELECT UserID, Email FROM User WHERE Email= %s"""
    _PASSWORD_SQL = """SELECT Password FROM User WHERE Password= %s"""
    _GET_USER_DETAILS_SQL = """SELECT u.UserID, u.First_Name, u.Last_Name,p.PassengerID
                                           FROM User u , Passenger p
                                           WHERE u.UserID = p.UserID
                                           AND u.UserID = %s"""
    _GET_DRIVER_ID_SQL = """SELECT DriverID FROM Driver WHERE UserID = %s"""
    _UPDATE_LOGIN_SQL = """UPDATE User SET Logged_In=1 WHERE UserID= %s"""
    emaildata, passworddata, driver_data = [], [], []
    js_obj = {}
    user_id, passenger_id, driver_id = 0, 0, 0
    u_name, u_l_name = "", ""
    hashed_password = hashlib.sha256(bytes(password, encoding='utf-8')).hexdigest()
    with DBcm.UseDatabase(config) as cursor:
        try:
            cursor.execute(_EMAIL_SQL, (email,))
            emaildata = cursor.fetchall()
            user_id = emaildata[0][0]
        except Exception as e:
            print('Error looking up email:', e)
    with DBcm.UseDatabase(config) as cursor1:
        try:
            cursor1.execute(_PASSWORD_SQL, (hashed_password,))
            passworddata = cursor1.fetchall()
        except Exception as e:
            print('error looking up password: ', e)
    if emaildata == [] or passworddata == []:
        js_obj = json.dumps({"status": "wrongemail/password"})
    elif email == emaildata[0][1] and hashed_password == passworddata[0][0]:
        with DBcm.UseDatabase(config) as cursor2:
            try:
                cursor2.execute(_GET_DRIVER_ID_SQL, (user_id,))
                driver_data = cursor2.fetchall()
            except Exception as e:
                print('Error getting driver id:', e)
        with DBcm.UseDatabase(config) as cursor3:
            try:
                cursor3.execute(_GET_USER_DETAILS_SQL, (user_id,))
                data = cursor3.fetchall()
                if driver_data != []:
                    for i in data:
                        for it in driver_data:
                            user_id = i[0]
                            u_name = i[1]
                            u_l_name = i[2]
                            passenger_id = i[3]
                            driver_id = it[0]
                        js_obj = json.dumps(
                            {"status": "match", "email": email, "user_id": user_id, "first_name": u_name.capitalize(),
                             "last_name": u_l_name.capitalize(), "passengerID": passenger_id, "myDriverID": driver_id})
                else:
                    for i in data:
                        user_id = i[0]
                        u_name = i[1]
                        u_l_name = i[2]
                        passenger_id = i[3]
                        driver_id = 0
                        js_obj = json.dumps(
                            {"status": "match", "email": email, "user_id": user_id, "first_name": u_name.capitalize(),
                             "last_name": u_l_name.capitalize(), "passengerID": passenger_id, "myDriverID": driver_id})
            except Exception as e:
                print('error with getting login information: ', e)
            else:
                with DBcm.UseDatabase(config) as cursor4:
                    try:
                        cursor4.execute(_UPDATE_LOGIN_SQL, (user_id,))
                    except Exception as e:
                        print('error executing update:', e)
                    else:
                        return js_obj
    else:
        js_obj = json.dumps({"status": "nomatch"})
    return js_obj


def process_logout(user_id):
    with DBcm.UseDatabase(config) as cursor:
        try:
            _SQL = """UPDATE User SET Logged_In=0 WHERE UserID=%s   """
            cursor.execute(_SQL, (user_id,))
            js_obj = json.dumps({"status": "logout successful"})
            return js_obj
        except Exception as err:
            print('sql error:', err)


def check_if_exists(email: str):
    exists = False
    with DBcm.UseDatabase(config) as cursor:
        _SQL = """SELECT Email FROM User WHERE Email= %s"""
        cursor.execute(_SQL, (email,))
        data = list(cursor.fetchall())
        emaildata = [i[0] for i in data]
    if emaildata == []:
        return exists
    else:
        exists = True
        return exists


def register_offer_lift(user_id, start_lat, start_long, start_county, destination_lat, destination_long, destination_county,
                        distance, departing, seats):
    _GETDRIVER_SQL = """SELECT DriverID FROM Driver WHERE UserID= %s """
    _User_Register_SQL = """INSERT INTO Lift
                       (DriverID, Start_Lat, Start_Long, Start_County, Destination_Lat, Destination_Long,
                       Destination_County, Distance, Depart_Date, Available_Spaces,
                       Created_At)
                       VALUES
                       (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,CURRENT_TIMESTAMP )"""
    with DBcm.UseDatabase(config) as cursor:
        cursor.execute(_GETDRIVER_SQL, (user_id,))
        data = cursor.fetchall()
        driver_id = data[0][0]
        cursor.execute(_User_Register_SQL, (driver_id, start_lat, start_long, start_county, destination_lat,
                                            destination_long, destination_county, distance, departing, seats))
    js_obj = json.dumps({"status": "registered"})
    return js_obj


# CHECK IF USER HAS A CAR REGISTERED BEFORE OFFERING A LIFT
def is_car_registered(user_id):
    if check_if_car_exists(user_id):
        js_obj = json.dumps({"status": "car registered"})
    else:
        js_obj = json.dumps({"status": "car not registered"})
    return js_obj


def check_if_car_exists(user_id):
    with DBcm.UseDatabase(config) as cursor:
        _SQL = """SELECT * FROM CarDetails WHERE UserID= %s"""
        cursor.execute(_SQL, (user_id,))
        data = list(cursor.fetchall())
    if data == []:
        js_obj = json.dumps({"status": "car not registered"})
    else:
        js_obj = json.dumps({"status": "car registered"})
    return js_obj


def register_car_and_driver(user_id, car_make, car_model, reg_num):
    carmake_lower = car_make.lower()
    carmodel_lower = car_model.lower()
    reg_lower = reg_num.lower()
    car_id, driver_id = 0, 0
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
            cursor.execute(_CAR_SQL, (carmake_lower, carmodel_lower, reg_lower, user_id))
            car_id = cursor.lastrowid
        except Exception as e:
            print('Error registering car:', e)
    with DBcm.UseDatabase(config) as cursor1:
        try:
            cursor1.execute(_DRIVER_SQL, (user_id, car_id))
        except Exception as e:
            print('Error registering user as driver:', e)
    with DBcm.UseDatabase(config) as cursor2:
        try:
            cursor2.execute(_GET_DRIVER_ID_SQL, (user_id, ))
            driver_data = cursor2.fetchall()
            driver_id = driver_data[0]
        except Exception as e:
            print('Error getting driver ID:', e)
        else:
            js_obj = json.dumps({"status": "registered", "driverID": driver_id})
            return js_obj


# REQUESTS


def process_request(lift_id, passenger_id):
    driver_id, request_id = 0, 0
    _GETDRIVER_SQL = """SELECT DriverID FROM Lift
                        WHERE LiftID = %s"""
    _REQUEST_SQL = """INSERT INTO Request
                      (DriverID, LiftID, PassengerID)
                      VALUES
                      (%s, %s, %s)"""
    try:
        with DBcm.UseDatabase(config)as cursor:
            try:
                cursor.execute(_GETDRIVER_SQL, (lift_id,))
                data = cursor.fetchall()
                driver_id = data[0][0]
            except Exception as e:
                print('error executing get driver SELECT query:', e)
        with DBcm.UseDatabase(config) as cursor:
            try:
                cursor.execute(_REQUEST_SQL, (driver_id, lift_id, passenger_id))
                request_id = cursor.lastrowid
            except Exception as e:
                print('error executing insert request:', e)
    except Exception as e:
        print('error executing process request queries:', e)
    else:
        return json.dumps({"status": "request completed", "requestID": request_id})


def list_user_requests(user_id):
    driver_id = 0
    _GETDRIVER_SQL = """SELECT DriverID FROM Driver WHERE UserID = %s"""
    _GETREQUESTS_SQL = """SELECT r.RequestID, r.DriverID, r.LiftID, r.PassengerID, r.Status, u.First_Name, u.Last_Name
                          FROM Request r, Passenger p, User u
                          WHERE r.PassengerID = p.PassengerID
                          AND u.UserID = p.UserID
                          AND r.DriverID = %s"""
    with DBcm.UseDatabase(config) as cursor:
        try:
            cursor.execute(_GETDRIVER_SQL, (user_id, ))
            data = cursor.fetchall()
            driver_id = data[0][0]
        except Exception as e:
            print('Error with get driver select query:', e)
    with DBcm.UseDatabase(config) as cursor:
        try:
            cursor.execute(_GETREQUESTS_SQL, (driver_id, ))
            request_data = cursor.fetchall()
            d = []
            for item in request_data:
                d.append({
                    'requestID': item[0],
                    'driverID': item[1],
                    'liftID': item[2],
                    'passengerID': item[3],
                    'status': item[4],
                    'passengerName': item[5] + ' ' + item[6]
                })
            js_obj = json.dumps(d)
        except Exception as e:
            print('Error with get requests select query:', e)
        else:
            return js_obj


def get_request_details(request_id):
    d, data, lift_data = [], [], []
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
            cursor.execute(_GETPASSENGERDETAILS_SQL, (request_id,))
            data = cursor.fetchall()
        except Exception as e:
            print('Error with get passenger details query: ', e)
    with DBcm.UseDatabase(config) as cursor:
        try:
            cursor.execute(_GETLIFTDETAILS_SQL, (request_id,))
            lift_data = cursor.fetchall()
        except Exception as e:
            print('Error with get lift details query: ', e)
        else:
            for item in data:
                for i in lift_data:
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
                    js_obj = json.dumps(d, default=converter)
                    return js_obj


def get_my_requests(user_id):
    passenger_id = 0
    _GETPASSENGER_SQL = """SELECT PassengerID FROM Passenger WHERE UserID = %s"""
    _GETREQUESTS_SQL = """SELECT r.RequestID, r.DriverID, r.LiftID, r.PassengerID, r.Status, u.First_Name, u.Last_Name
                          FROM Request r, Driver d, User u WHERE r.DriverID = d.DriverID
                          AND u.UserID = d.UserID
                          AND r.PassengerID = %s"""
    with DBcm.UseDatabase(config) as cursor:
        try:
            cursor.execute(_GETPASSENGER_SQL, (user_id,))
            data = cursor.fetchall()
            passenger_id = data[0][0]
        except Exception as e:
            print('Error with get passenger select query:', e)
    with DBcm.UseDatabase(config) as cursor:
        try:
            cursor.execute(_GETREQUESTS_SQL, (passenger_id, ))
            request_data = cursor.fetchall()
            d = []
            for item in request_data:
                d.append({
                    'requestID': item[0],
                    'driverID': item[1],
                    'liftID': item[2],
                    'passengerID': item[3],
                    'status': item[4],
                    'driverFName': item[5],
                    'driverLName': item[6]
                })
            js_obj = json.dumps(d)
        except Exception as e:
            print('Error with get requests select query:', e)
        else:
            return js_obj


def accept_request(request_id):
    driver_id, passenger_id, lift_id = 0, 0, 0
    _GETDRIVERPASSENGER_SQL = """SELECT DriverID, PassengerID, LiftID FROM Request WHERE RequestID = %s"""
    _UPDATELIFT_SQL = """UPDATE Lift SET Available_Spaces = Available_Spaces - 1 WHERE LiftID = %s"""
    _ADDTOCARGROUP_SQL = """INSERT INTO CarGroup (LiftID, DriverID, PassengerID) VALUES ( %s, %s, %s)"""
    _UPDATEREQUESTSTATUS_SQL = """UPDATE Request SET Status = 'Accepted' WHERE RequestID = %s"""
    with DBcm.UseDatabase(config) as cursor:
        try:
            cursor.execute(_GETDRIVERPASSENGER_SQL, (request_id,))
            data = cursor.fetchall()
            driver_id = data[0][0]
            passenger_id = data[0][1]
            lift_id = data[0][2]
        except Exception as e:
            print('Error with getting passengerID and liftID: ', e)
        try:
            cursor.execute(_UPDATELIFT_SQL, (lift_id,))
        except Exception as e:
            print('Error updating lift with accepted passenger:', e)
        try:
            cursor.execute(_ADDTOCARGROUP_SQL, (lift_id, driver_id, passenger_id))
        except Exception as e:
            print('Error inserting into car group table:', e)
        try:
            cursor.execute(_UPDATEREQUESTSTATUS_SQL, (request_id, ))
        except Exception as e:
            print('Error updating request status:', e)
    js_obj = json.dumps({'status': 'complete'})
    return js_obj


def deny_request(request_id):
    _UPDATEREQUESTSTATUS_SQL = """UPDATE Request SET Status = 'Denied' WHERE RequestID = %s"""
    with DBcm.UseDatabase(config) as cursor:
        try:
            cursor.execute(_UPDATEREQUESTSTATUS_SQL, (request_id,))
            js_obj = json.dumps({"status": "complete"})
        except Exception as e:
            print('Error with updating request status: ', e)
        else:
            return js_obj


# MY GROUPS

def get_my_groups(user_id):
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
            cursor.execute(_GROUPDETAIL_SQL, (user_id,))
            data = cursor.fetchall()
            d = []
            for item in data:
                d.append({
                    'groupID': item[0],
                    'driverName': item[1] + ' ' + item[2],
                    'liftID': item[3],
                    'departing': item[4],
                })
            js_obj = json.dumps(d, default=converter)
        except Exception as e:
            print('Error getting group details:', e)
        else:
            return js_obj


def get_group_details(lift_id, group_id):
    data, driver_data = [], []
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
            cursor1.execute(_GETGROUPDETAILS_SQL, (group_id, ))
            data = cursor1.fetchall()
        except Exception as e:
            print('Error getting group details: ', e)
    with DBcm.UseDatabase(config) as cursor2:
        try:
            cursor2.execute(_GETDRIVERDETAILS_SQL, (group_id,))
            driver_data = cursor2.fetchall()
        except Exception as e:
            print('Error getting driver details: ', e)
    with DBcm.UseDatabase(config) as cursor3:
        try:
            cursor3.execute(_GETPASSENGERS_SQL, (lift_id,))
            passenger_data = cursor3.fetchall()
            d = []
            for item in data:
                for i in driver_data:
                    for it in passenger_data:
                        d.append({
                            'groupID': group_id,
                            'liftID': lift_id,
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
            js_obj = json.dumps(d, default=converter)
        except Exception as e:
            print('Error getting passenger details: ', e)
        else:
            return js_obj


def get_my_completed_groups(user_id):
    d = []
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
            cursor.execute(_MY_COMPLETED_GROUPS_LIST_SQL, (user_id,))
            completed_group_data = cursor.fetchall()
            for item in completed_group_data:
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


def get_my_completed_lifts(user_id):
    d, lift_data = [], []
    _MY_COMPLETED_LIFT_LIST_SQL = """SELECT l.LiftID, l.Start_County, l.Destination_County, l.Depart_Date
                             FROM Lift l, Driver d, CompletedLifts c
                             WHERE c.DriverID = d.DriverID
                             AND c.LiftID = l.LiftID
                             AND d.UserID = %s
                             """
    with DBcm.UseDatabase(config) as cursor:
        try:
            cursor.execute(_MY_COMPLETED_LIFT_LIST_SQL, (user_id, ))
            lift_data = cursor.fetchall()
        except Exception as e:
            print('Error getting completed lifts:', e)
        else:
            for item in lift_data:
                d.append({
                    'liftID': item[0],
                    'route': item[1] + ' to ' + item[2],
                    'departing': item[3],
                })
            return json.dumps(d, default=converter)


def get_my_lifts(user_id):
    now = datetime.datetime.now()
    day = now.strftime("%Y-%m-%d")
    _LIFTDETAIL_SQL = """SELECT l.LiftID, l.Start_County, l.Destination_County, l.Depart_Date
                             FROM Lift l, Driver d
                             WHERE l.DriverID = d.DriverID
                             AND l.Depart_Date > %s
                             AND d.UserID = %s
                             AND l.LiftID NOT IN
                             (SELECT LiftID FROM CompletedLifts cl WHERE cl.LiftID = l.LiftID)"""
    with DBcm.UseDatabase(config) as cursor:
        try:
            cursor.execute(_LIFTDETAIL_SQL, (day, user_id,))
            data = cursor.fetchall()
            d = []
            for item in data:
                d.append({
                    'userID': user_id,
                    'liftID': item[0],
                    'route': item[1] + ' to ' + item[2],
                    'departing': item[3],
                })
            js_obj = json.dumps(d, default=converter)
        except Exception as e:
            print('Error getting lift list details:', e)
        else:
            return js_obj


def get_my_lift_details(lift_id):
    d, passenger_data, lift_data = [], [], []
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
            cursor.execute(_GETPASSENGERS_SQL, (lift_id,))
            passenger_data = cursor.fetchall()
            d = []
        except Exception as e:
            print('Error getting passenger details query: ', e)
    with DBcm.UseDatabase(config) as cursor:
        try:
            cursor.execute(_GETMYLIFTDETAILS_SQL, (lift_id, ))
            lift_data = cursor.fetchall()
            num_of_passengers = len(passenger_data)
            if passenger_data != []:
                for item in lift_data:
                    for i in passenger_data:
                        d.append({
                            'liftID': lift_id,
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
                            'numOfPassengers': num_of_passengers
                        })
            else:
                for item in lift_data:
                    d.append({
                        'liftID': lift_id,
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
            js_obj = json.dumps(d, default=converter)
        except Exception as e:
            print('Error getting my lift details:', e)
        else:
            return js_obj


def check_can_delete(lift_id):
    group_data = []
    _CHECK_IF_ACTIVE_SQL = """SELECT * FROM CarGroup WHERE LiftID = %s"""
    with DBcm.UseDatabase(config) as cursor:
        try:
            cursor.execute(_CHECK_IF_ACTIVE_SQL, (lift_id,))
            group_data = cursor.fetchall()
        except Exception as e:
            print('Error checking if lift is active:', e)
        else:
            if group_data == []:
                return json.dumps({'active': 'false'})
            else:
                return json.dumps({'active': 'true'})


def delete_lift(lift_id):
    _DELETE_LIFT_SQL= """DELETE FROM Lift WHERE LiftID = %s"""
    with DBcm.UseDatabase(config) as cursor:
        try:
            cursor.execute(_DELETE_LIFT_SQL, (lift_id,))
        except Exception as e:
            print('Error deleting lift:', e)
        else:
            return json.dumps({'status': 'deleted'})


def complete_lift(lift_id):
    d, passenger_ids, driver_id_data, distance_data = [], [], [], []
    driver_id, driver_id_for_completed_lift = 0, 0
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
            cursor1.execute(_GET_DRIVER_ID_SQL, (lift_id, ))
            driver_id_data = cursor1.fetchall()
            driver_id_for_completed_lift = driver_id_data[0][0]
        except Exception as e:
            print('Error getting driver user ID for insert:', e)
    with DBcm.UseDatabase(config) as cursor2:
        try:
            cursor2.execute(_GET_DISTANCE_SQL, (lift_id, ))
            distance_data = cursor2.fetchall()
            distance = distance_data[0][0]
        except Exception as e:
            print('Error getting distance information:', e)
    if driver_id_data:
        with DBcm.UseDatabase(config) as cursor3:
            try:
                cursor3.execute(_INSERT_COMPLETED_LIFT_DRIVER_SQL, (lift_id, driver_id_for_completed_lift, distance))
            except Exception as e:
                print('Error inserting driver to completed Lifts:', e)
    with DBcm.UseDatabase(config) as cursor4:
        try:
            cursor4.execute(_GET_PASSENGER_IDS_SQL, (lift_id, ))
            passenger_ids_data = cursor4.fetchall()
            for item in passenger_ids_data:
                passenger_ids.append(item[0])
        except Exception as e:
            print('Error getting passenger IDs:', e)
    with DBcm.UseDatabase(config) as cursor5:
        try:
            for item in passenger_ids:
                cursor5.execute(_INSERT_COMPLETED_LIFT_PASSENGERS_SQL, (lift_id, item, distance))
        except Exception as e:
            print('Error inserting passengers to completed Lifts:', e)
        else:
            return json.dumps({'completed lift registering': 'complete'})


def pop_ratings_table(lift_id, user_id):
    group_data, driverdata, d = [], [], []
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
            cursor.execute(_GET_CAR_GROUP_SQL, (lift_id, user_id, lift_id))
            group_data = cursor.fetchall()
        except Exception as e:
            print('Error getting car group details:', e)
    with DBcm.UseDatabase(config) as cursor2:
            try:
                cursor2.execute(_GET_DRIVER_SQL, (lift_id, user_id, lift_id))
                driverdata = cursor2.fetchall()
                if driverdata != []:
                    if group_data != []:
                        for item in group_data:
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
                    for item in group_data:
                            d.append({
                                'passengerID': item[0],
                                'passengerName': item[1] + ' ' + item[2],
                                'driverID': 'None',
                                'driverName': 'None',
                            })
                return json.dumps(d, default=converter)
            except Exception as e:
                print('Error getting car group driver:', e)



def rate_group(driver_id, driver_rating, passenger_data):
    # driverStar, passengerStar = '', ''
    star = ''
    driver_star_count, passenger_star_count = 0, 0
    driver_user_id, passenger_user_id, passenger_rating = 0, 0, 0
    driver_stars = {}
    if driver_rating != 0:
        star = str(driver_rating)
    passenger_star = str(3)
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
        if driver_id != 0:
            with DBcm.UseDatabase(config) as cursor:
                try:
                    cursor.execute(_GET_DRIVER_USERID_SQL, (driver_id, ))
                    driver_data = cursor.fetchall()
                    driver_user_id = driver_data[0][0]
                except Exception as e:
                    print('Error getting drivers UserID:', e)
            with DBcm.UseDatabase(config) as cursor:
                try:
                    cursor.execute(_UPDATE_DRIVER_STAR_COUNT_SQL, (driver_user_id, ))
                except Exception as e:
                    print('Error updating driver star count:', e)
            with DBcm.UseDatabase(config) as cursor:
                try:
                    cursor.execute(_GET_STAR_COUNT_SQL, (driver_user_id,))
                    driver_star_count_data = cursor.fetchall()
                    for item in driver_star_count_data:
                        driver_stars = {
                            '1': item[0],
                            '2': item[1],
                            '3': item[2],
                            '4': item[3],
                            '5': item[4]
                        }
                    driver_rating = data_utils.calculate_rating(driver_stars)
                except Exception as e:
                    print('Error getting driver star count:', e)
            with DBcm.UseDatabase(config) as cursor:
                try:
                    cursor.execute(_UPDATE_RATING_SQL, (driver_rating, driver_user_id))
                except Exception as e:
                    print('Error updating driver rating:', e)
        for item in passenger_data:
            star = str(item[1])
            _UPDATE_PASSENGER_STAR_COUNT_SQL = """UPDATE UserRating
                                             SET """ + star + """_Star =  """ + star + """_Star + 1,
                                             Number_of_Ratings = Number_of_Ratings +1
                                             WHERE UserID = %s"""
            with DBcm.UseDatabase(config) as cursor:
                try:
                    cursor.execute(_GET_PASSENGERS_USERID_SQL, (item[0],))
                    passenger_data = cursor.fetchall()
                    passenger_user_id = passenger_data[0][0]
                except Exception as e:
                    print('Error getting passengers UserID:', e)
            with DBcm.UseDatabase(config) as cursor:
                try:
                    cursor.execute(_UPDATE_PASSENGER_STAR_COUNT_SQL, (passenger_user_id, ))
                except Exception as e:
                    print('Error updating passenger star count:', e)
            with DBcm.UseDatabase(config) as cursor:
                try:
                    cursor.execute(_GET_STAR_COUNT_SQL, (passenger_user_id,))
                    passenger_star_count_data = cursor.fetchall()
                    for i in passenger_star_count_data:
                        passenger_stars = {
                            '1': i[0],
                            '2': i[1],
                            '3': i[2],
                            '4': i[3],
                            '5': i[4]
                        }
                    passenger_rating = data_utils.calculate_rating(passenger_stars)
                except Exception as e:
                    print('Error getting passenger star count:', e)
            with DBcm.UseDatabase(config) as cursor:
                try:
                    cursor.execute(_UPDATE_RATING_SQL, (passenger_rating, passenger_user_id))
                except Exception as e:
                    print('Error updating passenger rating:', e)
    except Exception as e:
        print('Error with rating function:', e)
    else:
        return json.dumps({'ratings': 'complete'})



def check_if_user_is_driver(lift_id, driver_id):
    driver_data, distance_data = [], []
    # see if user was the driver
    _SEE_IF_USER_IS_DRIVER_SQL = """SELECT DriverID FROM CarGroup
                                    WHERE LiftID = %s
                                    AND DriverID = %s"""
    _GET_DISTANCE_SQL = """SELECT Distance FROM Lift WHERE LiftID = %s"""
    with DBcm.UseDatabase(config) as cursor:
        try:
            cursor.execute(_GET_DISTANCE_SQL, (lift_id, ))
            distance_data = cursor.fetchall()
        except Exception as e:
            print('Error checking if user is the driver:', e)
    with DBcm.UseDatabase(config) as cursor1:
        try:
            cursor1.execute(_SEE_IF_USER_IS_DRIVER_SQL, (lift_id, driver_id))
            driver_data = cursor1.fetchall()
        except Exception as e:
            print('Error checking if user is the driver:', e)
        else:
            if driver_data != []:
                for item in distance_data:
                    return json.dumps({'is driver': 'true', 'distance': str(item[0])})
            else:
                for i in distance_data:
                    return json.dumps({'is driver': 'false', 'distance': str(i[0])})


def get_user_experience(user_id, new_exp, distance, num_of_passengers):
    experience_data, d = [], []
    _UPDATE_EXPERIENCE_SQL = """UPDATE Experience
                                SET Experience = Experience + %s, Overall_Distance_kilo = Overall_Distance_kilo + %s, Overall_Passengers = Overall_Passengers + %s
                                WHERE UserID = %s"""
    _GET_NEW_EXPERIENCE_SQL = """SELECT Overall_Distance_kilo, Overall_Passengers, Experience
                                 FROM Experience
                                 WHERE UserID = %s"""
    with DBcm.UseDatabase(config) as cursor:
        try:
            cursor.execute(_UPDATE_EXPERIENCE_SQL, (new_exp, distance, num_of_passengers, user_id))
        except Exception as e:
            print('Error updating users experience:', e)
    with DBcm.UseDatabase(config) as cursor1:
        try:
            cursor1.execute(_GET_NEW_EXPERIENCE_SQL, (user_id, ))
            experience_data = cursor1.fetchall()
        except Exception as e:
            print('Error getting users experience: ', e)
        else:
            for item in experience_data:
                d.append({
                    'overall distance': item[0],
                    'overallpassengers': item[1],
                    'experience': item[2]
                })
            return json.dumps(d, default=converter)


# ACTIVE LIFT


def get_driver_id(lift_id):
    _GET_DRIVER_ID_SQL ="""SELECT DriverID FROM Lift WHERE LiftID = %s"""
    with DBcm.UseDatabase(config) as cursor:
        try:
            cursor.execute(_GET_DRIVER_ID_SQL, (lift_id,))
            data = cursor.fetchall()
        except Exception as e:
            print('Error getting driver ID for lift:', e)
        else:
            return json.dumps({'driverID': data[0][0]})


def check_if_lift_finished(lift_id):
    _CHECK_IF_LIFTID_IN_COMPLETED_SQL = """SELECT  * FROM CompletedLifts WHERE LiftID = %s"""
    with DBcm.UseDatabase(config) as cursor:
        try:
            cursor.execute(_CHECK_IF_LIFTID_IN_COMPLETED_SQL, (lift_id,))
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
        except Exception as e:
            print('Error updating user information:', e)
    with DBcm.UseDatabase(config) as cursor1:
        try:
            cursor1.execute(_CHECK_IF_CAR_REGISTERED_SQL, (user_id, ))
            car_data = cursor1.fetchall()
        except Exception as e:
            print('Error check if car exists:', e)
    if car_make != "" and car_data != []:
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
        except Exception as e:
            print('Error checking if a driver:', e)
    if driver_data != []:
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
    d = []
    _GET_USERS_SQL_ = """SELECT u.First_Name, u.Last_Name, p.PassengerID, e.Experience
                         FROM User u, Passenger p, Experience e
                         WHERE u.UserID = p.UserID
                         AND u.UserID = e.UserID
                         ORDER BY e.Experience DESC"""
    with DBcm.UseDatabase(config) as cursor:
        try:
            cursor.execute(_GET_USERS_SQL_)
            data = cursor.fetchall()
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


function login(){
    console.log("LOGIN FUNCTION");
    event.preventDefault(); // prevents form submitting normally
    $.ajax({
        url:'http://looprac.pythonanywhere.com/loginuser',
        type:'post',
        async: false,
        data: $("#login_form").serialize()})
        .fail(function (jqXHR, textStatus, errorThrown) {
            console.log('AJAX ERROR\njqXHR: ' + jqXHR +'\ntext status: ' + textStatus + '\nError thrown: ' + errorThrown);
        })
        .done(function(data){
            var result = JSON.parse(data);
            if (result["status"] == "match")
            {
                console.log("match logged in ");
                window.sessionStorage.setItem('userID', result['user_id']);
                window.sessionStorage.setItem('firstName', result['first_name']);
                window.sessionStorage.setItem('lastName', result['last_name']);
                window.sessionStorage.setItem('passengerID', result['passengerID']);
                window.sessionStorage.setItem('myDriverID', result['myDriverID']);
                window.sessionStorage.setItem('loggedIn', true);
                window.location.replace("main_page.html");
            }
            else if (result["status"] == "wrongemail/password")
            {

                alert("Wrong email or password entered");
            }
            else if(result["status"] == "noMatch") {
                alert("Sorry, no match was found for email or password");
            }
        });
}

function checkLoginStatus(){
    var userID = sessionStorage.getItem('userID');
    var fname = sessionStorage.getItem('firstName');
    var lname = sessionStorage.getItem('lastName');
    var passID = sessionStorage.getItem('passengerID');
    var driveID = sessionStorage.getItem('myDriverID');
    var loggedin = sessionStorage.getItem('loggedIn');
    console.log('session data: ' + 'user id ' + userID + ' fname ' + fname + ' lname ' + lname + ' passengerID ' + passID + ' driverID ' + driveID + ' loggedin  ' + loggedin);
    var status = sessionStorage.getItem('loggedIn');
    console.log('status: ' + status);
    if(status){
        console.log('in if statement');
        window.location = "main_page.html";
    }
}

function logout(){
    console.log('logout funct ' );
    var form = $("#hiddenMainPageForm");
    // event.preventDefault(); // prevents form submitting normally
    // form.submit();
    // console.log
    $.ajax({
        url:'http://looprac.pythonanywhere.com/logoutuser',
        type:'post',
        async: false,
        data:form.serialize()})
        .fail(function (jqXHR, textStatus, errorThrown) {
            console.log('AJAX ERROR\njqXHR: ' + jqXHR +'\ntext status: ' + textStatus + '\nError thrown: ' + errorThrown);
        })
        .done(function(data){
            var result = JSON.parse(data);
            if (result["status"] == "logout successful")
            {
                sessionStorage.clear();
                alert('You have successfully logged out.');
                window.location = "login.html";
            }


        })
}


function RegisterUser(){
    event.preventDefault(); // prevents form submitting normally
    $.ajax({
        url:'http://looprac.pythonanywhere.com/registeruser',
        type:'post',
        async: false,
        data:  $("#form").serialize()})
        .fail(function (jqXHR, textStatus, errorThrown) {
            console.log('AJAX ERROR\njqXHR: ' + jqXHR +'\ntext status: ' + textStatus + '\nError thrown: ' + errorThrown);
        })
        .done(function(data){
            var result = JSON.parse(data);
            if (result["status"] == "registered")
            {
                alert("You are now a registered Looper :)");
                window.location.replace("login.html");
            }
            else if (result["status"] == "Not all required elements are entered")
            {
                alert("ERROR: not all fields were filled in");
            }
            else if (result["status"] == "email exists")
            {
                document.getElementById("emailError").innerHTML = "This email address already exists";
                setTimeout(function () {
                    window.location = document.URL;
                },5000);
            }
        });
    console.log("after subform ajax")
}

/******************************
 * OFFER LIFT
 */

function subOfferLift(){
    event.preventDefault(); // prevents form submitting normally
    var date = document.getElementById('departDateInput').value;
    console.log(date);
    var formattedDate = new Date(date).toMysqlFormat();
    console.log('formatted date '  + formattedDate);
    var d = JSON.stringify({
        'userID' : document.getElementById('userID').value,
        'start_lat': document.getElementById('lat').value,
        'start_long': document.getElementById('lng').value,
        'start_county': document.getElementById('start_county').value,
        'destination_lat': document.getElementById('destinationLat').value,
        'destination_long': document.getElementById('destinationLng').value,
        'destination_county': document.getElementById('destination_county').value,
        'depart_date' : formattedDate,
        'depart_time' : document.getElementById('departTimeInput').value,
        'seats' : document.getElementById('seatsInput').value
    });
    console.log(d);
    $.ajax({
        url:'http://looprac.pythonanywhere.com/offerLift',
        type:'post',
        async: false,
        contentType: 'application/json',
        dataType: 'json',
        data: d })
        .fail(function (jqXHR, textStatus, errorThrown) {
            console.log('AJAX ERROR\njqXHR: ' + jqXHR +'\ntext status: ' + textStatus + '\nError thrown: ' + errorThrown);
        })
        .done(function(data){
            // var result = JSON.parse(data);
            if (data["status"] == "registered")
            {
                alert("Your lift offer has been submitted" );
                window.location.replace("main_page.html");
            }
            else if (data["status"] == "Not all required elements are entered")
            {
                alert("ERROR: not all fields were filled in");
            }

        });
}

function twoDigits(d) {
    if(0 <= d && d < 10) return "0" + d.toString();
    if(-10 < d && d < 0) return "-0" + (-1*d).toString();
    return d.toString();
}

Date.prototype.toMysqlFormat = function() {
    return this.getUTCFullYear() + "-" + twoDigits(1 + this.getUTCMonth()) + "-" + twoDigits(this.getUTCDate()) ;
};


/***********************************
 CHECK IF USER HAS REGISTERED CAR BEFORE OFFERING A LIFT
 /**********************************/

function checkHasCarRegistered() {
    console.log('check car has registerd');
    event.preventDefault(); // prevents form submitting normally
    var user_id = sessionStorage.getItem('userID');
    var j = JSON.stringify({'userid': user_id});
    console.log('before ajax');
    $.ajax({
        url:'http://looprac.pythonanywhere.com/checkcarregistered',
        type:'post',
        async: false,
        contentType: 'application/json',
        dataType: 'json',
        data:  j})
        .fail(function (jqXHR, textStatus, errorThrown) {
            console.log('AJAX ERROR\njqXHR: ' + jqXHR +'\ntext status: ' + textStatus + '\nError thrown: ' + errorThrown);
        })
        .done(function(data){
            if (data["status"] == "car registered"){
                console.log('car reg branch');
                window.location.replace("offerLift.html");
            }
            else if (data["status"] == "car not registered"){
                console.log('car not registered branch');
                alert("Please register your car before you offer a lift");
                window.location.replace("carDetails.html");
            }

        });
    console.log('after ajax');
}

function registerCar() {
    event.preventDefault(); // prevents form submitting normally
    $.ajax({
        url:'http://looprac.pythonanywhere.com/registercar',
        type:'post',
        async: false,
        data: $("#carRegForm").serialize() })
        .fail(function (jqXHR, textStatus, errorThrown) {
            console.log('AJAX ERROR\njqXHR: ' + jqXHR +'\ntext status: ' + textStatus + '\nError thrown: ' + errorThrown);
        })
        .done(function(data){
            var result = JSON.parse(data);
            if (result["status"] == "registered"){
                window.sessionStorage.setItem("driverID", result["driverID"]);
                window.location.replace("offerLift.html");
            }
            else if (result["status" == "Not all required elements are entered"]){
                alert("ERROR: not all fields were filled in");
            }

        });
}



function updateAvailableLifts(){
    $.ajax({
        url:'http://looprac.pythonanywhere.com/availableLifts',
        type:'post',
        data: JSON.stringify({'passengerID': sessionStorage.getItem('passengerID')})
        })
        .fail(function (jqXHR, textStatus, errorThrown) {
            console.log('AJAX ERROR\njqXHR: ' + jqXHR +'\ntext status: ' + textStatus + '\nError thrown: ' + errorThrown);
        })
        .done(function(data){
            var result = JSON.parse(data);
            console.log(data);
            var table = $('#availableLiftsTbl');
            var tr = '';
            var liftID =0;
            var driverID = 0;
            var sCounty = '';
            var dCounty = '';
            var departDate = '';
            var departTime = '';
            var trID = '';
            var tdID = '';
            var btnID = '';
            var displayingDateTime = '';

            for (var i = 0; i < result.length ; i ++ ) {
                liftID = result[i]["liftID"];
                driverID = result[i]['driverID'];
                sCounty =  result[i]['startCounty'];
                dCounty = result[i]['destinationCounty'];
                departDate = result[i]['departDate'];
                departTime = result[i]['departTime'];
                displayingDateTime = departTime + ' ' + departDate;
                trID = 'trID' + i.toString();
                tdID = 'tdID' + i.toString();
                btnID = 'btnID' + i.toString();
                console.log(trID);
                console.log(tdID);
                tr = '<tr onclick="expandLift('+liftID +','+ driverID +')" id=' +trID + ' ><td class="hidden" id=' + tdID + '>' + liftID + '</td><td class="hidden">' + driverID + '</td><td>' + sCounty + '</td><td>' + dCounty
                    + '</td><td>' +  displayingDateTime + '</td></tr>';
                    // '<td><input type="button" id="'+ btnID +' " value=">" class="btn btn-primary" onclick="expandLift('+i+')" /></td></tr>';
                table.append(tr);
            }
        });
}

function expandLift(liftID, driverID){
    console.log(liftID);
    window.sessionStorage.setItem('expandLiftID', liftID);
    window.sessionStorage.setItem('driverID', driverID);
    window.location.replace('LiftDetails.html');
}

function getLiftDetails(){
    console.log('get lift details func');
    var liftID = sessionStorage.getItem('expandLiftID');
    var driverID = sessionStorage.getItem('driverID');
    console.log('lift and driver id ' + liftID + ' ' + driverID);
    var j = JSON.stringify({'liftID': liftID, 'driverID': driverID});
    console.log(typeof j);
    $.ajax({
        url:'http://looprac.pythonanywhere.com/liftDetails',
        type:'post',
        data:j})
        .fail(function (jqXHR, textStatus, errorThrown) {
            console.log('AJAX ERROR\njqXHR: ' + jqXHR +'\ntext status: ' + textStatus + '\nError thrown: ' + errorThrown);
        })
        .done(function (data) {
            var result = JSON.parse(data);
            console.log('result: ' + result[0]);
            var startLat = result[0]['startLat'];
            var startLng = result[0]['startLng'];
            var destLat = result[0]['destinationLat'];
            var destLng = result[0]['destinationLng'];
            var driver = result[0]['DriverFName'] + ' ' + result[0]['DriverLName'];
            var rating = result[0]['rating'];
            var departDate = result[0]['departDate'];
            var departTime = result[0]['departTime'];
            var returnDate = result[0]['returnDate'];
            var returnTime = result[0]['returnTime'];
            var seats = result[0]['seats'];

            console.log('return date and time ' + returnDate + ' ' + returnTime);
            showLift(startLat, startLng, destLat, destLng, "lift-map-canvas");
            geocodeCoords(startLat, startLng, 'startRdOnly');
            geocodeCoords(destLat, destLng, 'destinationRdOnly');
            document.getElementById('liftIDRdOnly').value = liftID;
            document.getElementById('driverRdOnly').value = driver;
            document.getElementById('driverRatingRdOnly').value = rating + ' / 5.0';
            document.getElementById('departTimeRdOnly').value = departTime;
            document.getElementById('departDateRdOnly').value = departDate;
            document.getElementById('seatsRdOnly').value = seats;

        });
    console.log('after ajax request');
}


/*********************************
 REQUESTS
 **************************************/

function sendLiftReq() {
    event.preventDefault();
    console.log('user id: ' + sessionStorage.getItem('userID'));
    $.ajax({
        url:'http://looprac.pythonanywhere.com/requestLift',
        type:'post',
        async: false,
        data: $('#liftReqForm').serialize()})
        .fail(function (jqXHR, textStatus, errorThrown) {
            console.log('AJAX ERROR\njqXHR: ' + jqXHR +'\ntext status: ' + textStatus + '\nError thrown: ' + errorThrown);
        })
        .done(function (data) {
            var result = JSON.parse(data);
            if(result["status"] == "request completed"){
                alert('Your request has been submitted.  You will be notified of the drivers response.');
                window.location = "availableLifts.html";
            }
        });
    console.log('after ajax');
}


function updateUserLiftRequests(){
    // var d = ;
    // console.log('d: ' + d + 'type: ' + typeof  d);
    $.ajax({
        url:'http://looprac.pythonanywhere.com/availableRequests',
        type:'post',
        data: $('#availableReqHiddenForm').serialize()
         })
        .fail(function (jqXHR, textStatus, errorThrown) {
            console.log('AJAX ERROR\njqXHR: ' + jqXHR +'\ntext status: ' + textStatus + '\nError thrown: ' + errorThrown);
        })
        .done(function(data){
            var result = JSON.parse(data);
            console.log('data ' + data + ' ' + data.length);
            var table = $('#availableRequestsTbl');
            var tr = '';
            var liftID =0;
            var passengerID = 0;
            var requestID = 0;
            var driverID = 0;
            var trID = '';
            var tdID = '';
            var btnID = '';
            var passengerName = '';
            var status = "";
            for (var i = 0; i < result.length ; i ++ ) {
                liftID = result[i]["liftID"];
                driverID = result[i]["driverID"];
                requestID = result[i]["requestID"];
                passengerID = result[i]["passengerID"];
                passengerName = result[i]["passengerName"];
                status = result[i]["status"];
                trID = 'trID' + i.toString();
                tdID = 'tdID' + i.toString();
                btnID = 'btnID' + i.toString();
                console.log('request ' + requestID + ' lift ' + liftID + ' driver ' + driverID + ' passenger ' + passengerID);
                if (status != "Pending"){
                    tr = '<tr style="color: #ff8800;"  id=' +trID
                        + ' ><td class="hidden" id=' + tdID + '>' + requestID + '</td><td class="hidden">' + liftID + '</td><td class="hidden">' + driverID
                        + '</td><td class="hidden">' + passengerID + '</td><td>' + passengerName + '</td><td>' + status
                        + '</td></tr>';
                }
                else{
                    tr = '<tr onclick="expandRequest('+ requestID + ',' + driverID +')" style="color: #ff8800;"  id=' +trID
                        + ' ><td class="hidden" id=' + tdID + '>' + requestID + '</td><td class="hidden">' + liftID + '</td><td class="hidden">' + driverID
                        + '</td><td class="hidden">' + passengerID + '</td><td>' + passengerName + '</td><td>' + status
                        + '</td></tr>';
                }

                table.append(tr);
            }
        });
}


function expandRequest(requestID, driverID){
    console.log(requestID);
    window.sessionStorage.setItem('requestID', requestID);
    window.sessionStorage.setItem('driverID', driverID);
    window.location.replace('requestDetails.html');
}

function getRequestDetails(){
    console.log('get request details func');
    var requestID = sessionStorage.getItem('requestID');
    var driverID = sessionStorage.getItem('driverID');
    console.log('lift and driver id ' + requestID + ' ' + driverID);
    var j = JSON.stringify({'requestID': requestID, 'driverID': driverID});
    $.ajax({
        url:'http://looprac.pythonanywhere.com/requestDetails',
        type:'post',
        data:j})
        .fail(function (jqXHR, textStatus, errorThrown) {
            console.log('AJAX ERROR\njqXHR: ' + jqXHR +'\ntext status: ' + textStatus + '\nError thrown: ' + errorThrown);
        })
        .done(function (data) {
            var result = JSON.parse(data);
            var startLat = result[0]["startLat"];
            var startLng = result[0]["startLng"];
            var destLat = result[0]["destLat"];
            var destLng = result[0]["destLng"];
            console.log('result: ' + data);
            document.getElementById('passengerNameRdOnly').value = result[0]["name"];
            document.getElementById('departTimeRdOnly').value = result[0]["time"];
            document.getElementById('departDateRdOnly').value = result[0]["date"];
            document.getElementById('passengerRatingRdOnly').value = result[0]["rating"] + ' / 5.0';
            window.onload = showLift(startLat, startLng, destLat, destLng, "myRequestMap-Canvas");

        });
    console.log('after ajax request');
}

function updateMyRequests(){
    $.ajax({
        url:'http://looprac.pythonanywhere.com/myRequests',
        type:'post',
        data: $('#myReqHiddenForm').serialize()
    })
        .fail(function (jqXHR, textStatus, errorThrown) {
            console.log('AJAX ERROR\njqXHR: ' + jqXHR +'\ntext status: ' + textStatus + '\nError thrown: ' + errorThrown);
        })
        .done(function(data){
            var result = JSON.parse(data);
            console.log('data ' + data + ' ' + data.length);
            var table = $('#myRequestsTbl');
            var tr = '';
            var liftID =0;
            var passengerID = 0;
            var requestID = 0;
            var driverID = 0;
            var driverName = '';
            var trID = '';
            var tdID = '';
            var btnID = '';
            var status = '';
            for (var i = 0; i < result.length ; i ++ ) {
                liftID = result[i]["liftID"];
                driverID = result[i]["driverID"];
                requestID = result[i]["requestID"];
                passengerID = result[i]["passengerID"];
                status = result[i]["status"];
                driverName = result[i]["driverFName"] + " " + result[i]["driverLName"];
                trID = 'trID' + i.toString();
                tdID = 'tdID' + i.toString();
                btnID = 'btnID' + i.toString();
                console.log('request ' + requestID + ' lift ' + liftID + ' driver ' + driverID + ' passenger ' + passengerID);
                tr = '<tr style="color: #ff8800;"  id='
                    +trID + ' ><td class="hidden" id=' + tdID + '>' + requestID + '</td><td class="hidden">' + liftID + '</td><td class="hidden">'
                    + driverID + '</td><td class="hidden">' + passengerID
                    + '</td><td>' + driverName + '</td><td style="color:#eae8ff;">' + status + '</td></tr>';
                table.append(tr);
            }

        });
}


function acceptRequest() {
    console.log('accept request func');
    $.ajax({
        url: 'http://looprac.pythonanywhere.com/acceptRequest',
        type: 'post',
        data: $('#liftReqForm').serialize()
    })
        .fail(function (jqXHR, textStatus, errorThrown) {
            console.log('AJAX ERROR\njqXHR: ' + jqXHR + '\ntext status: ' + textStatus + '\nError thrown: ' + errorThrown);
        })
        .done(function (data) {
            console.log('data ' + data);
            var result = JSON.parse(data);
            if (result["status"] == "complete"){
                console.log('inside if statement');
                alert('Request accepted.  The passenger will be notified.');
                window.location = "main_page.html";
            }
        });
    console.log('after ajax');
}


function denyRequest(){
    console.log('deny request func');
    $.ajax({
        url: 'http://looprac.pythonanywhere.com/denyRequest',
        type: 'post',
        data: $('#liftReqForm').serialize()
    })
        .fail(function (jqXHR, textStatus, errorThrown) {
            console.log('AJAX ERROR\njqXHR: ' + jqXHR + '\ntext status: ' + textStatus + '\nError thrown: ' + errorThrown);
        })
        .done(function (data) {
            console.log('data ' + data);
            var result = JSON.parse(data);
            if (result["status"] == "complete"){
                console.log('inside if statement');
                alert('Request has been denied.  The passenger will be notified.');
                window.location = "main_page.html";
            }
        });
    console.log('after ajax');
}


function updateMyGroups(){
    console.log('my lifts func');
    $.ajax({
        url: 'http://looprac.pythonanywhere.com/myGroups',
        type: 'post',
        data: $('#myReqHiddenForm').serialize()
    })
        .fail(function (jqXHR, textStatus, errorThrown) {
            console.log('AJAX ERROR\njqXHR: ' + jqXHR + '\ntext status: ' + textStatus + '\nError thrown: ' + errorThrown);
        })
        .done(function (data) {
            console.log('data ' + data);
            var result = JSON.parse(data);
            var table = $('#myGroupsTbl');
            var tr = '';
            var groupID = 0;
            var driverName = '';
            var departTime = '';
            var departDate = '';
            var liftID = '';
            var trID = '';
            var tdID = '';
            var btnID = '';
            for (var i = 0; i < result.length ; i ++ ) {
                groupID = result[i]["groupID"];
                driverName = result[i]["driverName"];
                liftID = result[i]["liftID"];
                departTime = result[i]["departTime"];
                departDate = result[i]["departDate"];
                trID = 'trID' + i.toString();
                tdID = 'tdID' + i.toString();
                btnID = 'btnID' + i.toString();
                console.log('LIFT id ' + liftID);
                tr = '<tr onclick="expandGroup(' + liftID + ',' + groupID +')" style="color: #ff8800;" id=' +trID + '><td class="hidden" id=' + tdID + '>' + liftID+ '</td><td>' + driverName + '</td><td>' + departTime + ' ' + departDate +  '</td></tr>';
                table.append(tr);
                // $('#trID').on("click", showGroupDetails(groupID, departTime, departDate, driverName, i));
            }
        });
    console.log('after ajax');
}

function expandGroup(liftID, groupID){
    window.sessionStorage.setItem('myLiftID', liftID);
    window.sessionStorage.setItem('groupID', groupID);

    window.location.replace('groupDetails.html');
}

function showGroupDetails(liftID, groupID )
{
    $.ajax({
        url: 'http://looprac.pythonanywhere.com/groupDetails',
        type: 'post',
        data: JSON.stringify({"liftID": liftID, "groupID": groupID})
    })
        .fail(function (jqXHR, textStatus, errorThrown) {
            console.log('AJAX ERROR\njqXHR: ' + jqXHR + '\ntext status: ' + textStatus + '\nError thrown: ' + errorThrown);
        })
        .done(function (data) {
            var result = JSON.parse(data);
            console.log('data ' + data + ' ' + result.length);
            var numOfPassengers = result.length;
            console.log('NUMBER of passengers: ' + numOfPassengers);
            window.sessionStorage.setItem('numOfPassengers', numOfPassengers);
            document.getElementById('hiddenNumOfPassengers').value = numOfPassengers;
            document.getElementById('driverNameRdOnly').value =  result[0]["driverName"];
            document.getElementById('carRegRdOnly').value =  result[0]["carReg"];
            document.getElementById('driverPhoneRdOnly').value =  result[0]["driverPhone"];
            document.getElementById('driverDetailsRdOnly').value = result[0]["driverRating"];
            document.getElementById('routeRdOnly').value = result[0]["startCounty"] + ' To ' + result[0]["destCounty"];
            document.getElementById('departTimeRdOnly').value = result[0]["departTime"];
            document.getElementById('departDateRdOnly').value = result[0]["departDate"];
            document.getElementById('hiddenDriverID').value = result[0]["driverID"];
            document.getElementById('numOfPassengersHeader').innerHTML ='Passengers: ' + numOfPassengers;
            var startLat = result[0]["startLat"];
            var startLng = result[0]["startLng"];
            var destinationLat = result[0]["destLat"];
            var destinationLng= result[0]["destLng"];
            window.sessionStorage.setItem('myLiftStartLat', startLat);
            window.sessionStorage.setItem('myLiftStartLng', startLng);
            window.sessionStorage.setItem('myLiftDestinationLat', destinationLat);
            window.sessionStorage.setItem('myLiftDestinationLng', destinationLng);
            var paragraph = '';
            var passengerName = '';
            var passengerRating = '';
            var table = $('#passengersTbl');
            var phone = '';
            var trID ='';
            var tdID = '';
            var btnID = '';
            for (var index = 0; index < result.length; index++)
            {
                trID = 'trID' + index.toString();
                tdID = 'tdID' + index.toString();
                btnID = 'btnID' + index.toString();
                passengerName = result[index]["passengerName"];
                phone = result[index]["passengerPhone"];
                passengerRating = result[index]["passengerRating"];
                paragraph = '<tr style="color:#ff8800;"><td>'+ passengerName + '</td><td>' + passengerRating + '</td><td>' + phone + '</td></tr>';
                console.log('name: ' + passengerName + ' ' + 'phone: ' + phone);
                table.append(paragraph);
            }
            window.onload = showLift(startLat, startLng, destinationLat, destinationLng, "myLift-map-canvas");

        });


}

//MY LIFTS: where driver see's the lifts they have created and who the passengers are

function updateMyLifts(){
    console.log('my lifts func');
    $.ajax({
        url: 'http://looprac.pythonanywhere.com/myLifts',
        type: 'post',
        data: $('#myLiftsHiddenForm').serialize()
    })
        .fail(function (jqXHR, textStatus, errorThrown) {
            console.log('AJAX ERROR\njqXHR: ' + jqXHR + '\ntext status: ' + textStatus + '\nError thrown: ' + errorThrown);
        })
        .done(function (data) {
            console.log('data ' + data);
            var result = JSON.parse(data);
            var table = $('#myLiftsTbl');
            var tr = '';
            var liftID = 0;
            var route = '';
            var departingInfo= '';
            var trID = '';
            var tdID = '';
            var btnID = '';
            for (var i = 0; i < result.length ; i ++ ) {
                liftID = result[i]["liftID"];
                route = result[i]["route"];
                departingInfo = result[i]["departTime"] + ' ' + result[i]["departDate"];
                trID = 'trID' + i.toString();
                tdID = 'tdID' + i.toString();
                btnID = 'btnID' + i.toString();
                console.log('LIFT id ' + liftID);
                tr = '<tr onclick="expandMyLift(' + liftID +')" style="color: #ff8800;" id=' +trID + '><td>' + route + '</td><td>' + departingInfo +  '</td></tr>';
                table.append(tr);
                // $('#trID').on("click", showGroupDetails(groupID, departTime, departDate, driverName, i));
            }
        });
    console.log('after ajax');
}

function expandMyLift(liftID){
    window.sessionStorage.setItem('myLiftID', liftID);
    window.location.replace("myLiftDetails.html");
}

function showMyLiftDetails(liftID )
{
    $.ajax({
        url: 'http://looprac.pythonanywhere.com/myLiftDetails',
        type: 'post',
        data: JSON.stringify({"liftID": liftID})
    })
        .fail(function (jqXHR, textStatus, errorThrown) {
            console.log('AJAX ERROR\njqXHR: ' + jqXHR + '\ntext status: ' + textStatus + '\nError thrown: ' + errorThrown);
        })
        .done(function (data) {
            var result = JSON.parse(data);
            console.log('data ' + data + ' ' + result.length);

            document.getElementById('spacesAvailableRdOnly').value =  result[0]['spaces'];
            document.getElementById('routeRdOnly').value = result[0]["startCounty"] + ' To ' + result[0]["destCounty"];
            document.getElementById('departTimeRdOnly').value = result[0]["departTime"];
            document.getElementById('departDateRdOnly').value = result[0]["departDate"];
            document.getElementById('carRegRdOnly').value = result[0]["car reg"];
            document.getElementById('hiddenDriverID').value = sessionStorage.getItem('myDriverID');

            var startLat = result[0]["startLat"];
            var startLng = result[0]["startLng"];
            var destinationLat = result[0]["destLat"];
            var destinationLng= result[0]["destLng"];
            window.sessionStorage.setItem('myLiftStartLat', startLat);
            window.sessionStorage.setItem('myLiftStartLng', startLng);
            window.sessionStorage.setItem('myLiftDestinationLat', destinationLat);
            window.sessionStorage.setItem('myLiftDestinationLng', destinationLng);
            var passengerRating = '';
            var paragraph = '';
            var passengerName = '';
            var table = $('#passengersTbl');
            var phone = '';
            var trID ='';
            var tdID = '';
            var btnID = '';
            for (var index = 0; index < result.length; index++)
            {
                trID = 'trID' + index.toString();
                tdID = 'tdID' + index.toString();
                btnID = 'btnID' + index.toString();
                passengerName = result[index]["passengerName"];
                phone = result[index]["passengerPhone"];
                window.sessionStorage.setItem('numOfPassengers', result[index]["numOfPassengers"]);
                console.log(result[index]["numOfPassengers"]);
                if (result[index]["numOfPassengers"] == undefined){
                    document.getElementById('numOfPassengersHeader').innerHTML ='Passengers: 0';
                }
                else{
                    document.getElementById('numOfPassengersHeader').innerHTML ='Passengers: ' + result[index]["numOfPassengers"];
                }
                document.getElementById('hiddenNumOfPassengers').value = result[index]["numOfPassengers"];
                passengerRating = result[index]["passengerRating"];
                if (passengerName == "None")
                {
                    passengerName = "";
                    passengerRating = "";
                    phone = "";
                }
                paragraph = '<tr style="color:#ff8800;"><td>'+ passengerName + '</td><td>' + passengerRating + '</td><td>' + phone + '</td></tr>';
                console.log('name: ' + passengerName + ' ' + 'phone: ' + phone);
                table.append(paragraph);
            }
            window.onload = showLift(startLat, startLng, destinationLat, destinationLng, "myLift-map-canvas");

        });


}

/*************************************
 * COMPLETED LIFTS
 */

function updateMyCompletedGroups(){
    $.ajax({
        url: 'http://looprac.pythonanywhere.com/myCompletedGroups',
        type: 'post',
        data: $('#myCompletedGroupHiddenForm').serialize()
    })
        .fail(function (jqXHR, textStatus, errorThrown) {
            console.log('AJAX ERROR\njqXHR: ' + jqXHR + '\ntext status: ' + textStatus + '\nError thrown: ' + errorThrown);
        })
        .done(function (data) {
            console.log('data ' + data);
            var result = JSON.parse(data);
            var table = $('#myCompletedGroupsTbl');
            var tr = '';
            var driverName = '';
            var departed = '';
            var liftID = '';
            var trID = '';
            var tdID = '';
            for (var i = 0; i < result.length ; i ++ ) {
                driverName = result[i]["driverName"];
                liftID = result[i]["liftID"];
                departed = result[i]["time"] + ' ' + result[i]["date"];
                trID = 'trID' + i.toString();
                tdID = 'tdID' + i.toString();
                tr = '<tr onclick="expandMyCompletedLift(' + liftID + ')" style="color: #ff8800;" id=' + trID + '><td class="hidden" id=' + tdID + '>' + liftID+ '</td><td>' + driverName + '</td><td>' + departed +  '</td></tr>';
                table.append(tr);
            }
        });
}
function updateMyCompletedLifts(){
    $.ajax({
        url: 'http://looprac.pythonanywhere.com/myCompletedLifts',
        type: 'post',
        data: $('#myCompletedLiftsHiddenForm').serialize()
    })
        .fail(function (jqXHR, textStatus, errorThrown) {
            console.log('AJAX ERROR\njqXHR: ' + jqXHR + '\ntext status: ' + textStatus + '\nError thrown: ' + errorThrown);
        })
        .done(function (data) {
            console.log('data ' + data);
            var result = JSON.parse(data);
            var table = $('#myCompletedLiftsTbl');
            var tr = '';
            var liftID = 0;
            var route = '';
            var departedInfo= '';
            var trID = '';
            var tdID = '';
            var btnID = '';
            for (var i = 0; i < result.length ; i ++ ) {
                liftID = result[i]["liftID"];
                route = result[i]["route"];
                departedInfo = result[i]["departTime"] + ' ' + result[i]["departDate"];
                trID = 'trID' + i.toString();
                tdID = 'tdID' + i.toString();
                btnID = 'btnID' + i.toString();
                tr = '<tr onclick="expandMyCompletedLift(' + liftID +')" style="color: #ff8800;" id=' +trID + '><td>' + route + '</td><td>' + departedInfo +  '</td></tr>';
                table.append(tr);
                // $('#trID').on("click", showGroupDetails(groupID, departTime, departDate, driverName, i));
            }
        });
}

function expandMyCompletedLift(liftID){
    window.sessionStorage.setItem('myCompletedLiftID', liftID);
    window.location.replace("myCompletedLiftDetails.html");
}

function showMyCompletedLiftDetails(liftID) {
    $.ajax({
        url: 'http://looprac.pythonanywhere.com/myLiftDetails',
        type: 'post',
        data: JSON.stringify({"liftID": liftID})
    })
        .fail(function (jqXHR, textStatus, errorThrown) {
            console.log('AJAX ERROR\njqXHR: ' + jqXHR + '\ntext status: ' + textStatus + '\nError thrown: ' + errorThrown);
        })
        .done(function (data) {
            var result = JSON.parse(data);
            console.log('data ' + data + ' ' + result.length);
            document.getElementById('routeRdOnly').value = result[0]["startCounty"] + ' To ' + result[0]["destCounty"];
            document.getElementById('departTimeRdOnly').value = result[0]["departTime"];
            document.getElementById('departDateRdOnly').value = result[0]["departDate"];
            document.getElementById('driverNameRdOnly').value = result[0]["driverName"];
            document.getElementById('driverRatingRdOnly').value = result[0]["driverRating"];

            var startLat = result[0]["startLat"];
            var startLng = result[0]["startLng"];
            var destinationLat = result[0]["destLat"];
            var destinationLng = result[0]["destLng"];
            var paragraph = '';
            var passengerName = '';
            var passengerRating = '';
            var table = $('#passengersTbl');
            var phone = '';
            var trID = '';
            var tdID = '';
            for (var index = 0; index < result.length; index++) {
                trID = 'trID' + index.toString();
                tdID = 'tdID' + index.toString();
                passengerName = result[index]["passengerName"];
                passengerRating = result[index]["passengerRating"];
                phone = result[index]["passengerPhone"];
                document.getElementById('numOfPassengersHeader').innerHTML = 'Passengers: ' + result[index]["numOfPassengers"];
                document.getElementById('hiddenNumOfPassengers').value = result[index]["numOfPassengers"];
                document.getElementById('carRegRdOnly').value = result[index]["car reg"];
                if (passengerName == "None") {
                    passengerName = "";
                    passengerRating = "";
                    phone = "";
                }
                paragraph = '<tr style="color:#ff8800;"><td>' + passengerName + '</td><td>' + passengerRating + '</td><td>' + phone + '</td></tr>';
                table.append(paragraph);
            }
            window.onload = showLift(startLat, startLng, destinationLat, destinationLng, "myLift-map-canvas");
        })
}

function completeLiftAndFilterRatingList(liftID, distance){
    console.log('distance ' + distance);
    $.ajax({
        url: 'http://looprac.pythonanywhere.com/completeLift',
        type: 'post',
        data: JSON.stringify({"liftID": liftID, "distance": distance})
    })
        .fail(function (jqXHR, textStatus, errorThrown) {
            console.log('AJAX ERROR\njqXHR: ' + jqXHR + '\ntext status: ' + textStatus + '\nError thrown: ' + errorThrown);
        })
        .done(function (data) {
            var result = JSON.parse(data);
            if (result["completed lift registering"] == "complete")
            {
                window.location = "liftComplete.html";
            }
            else{
                console.log('Registering users to completed lift failed');
            }
        })

}

function displayRatingTables(){
    $.ajax({
        url: 'http://looprac.pythonanywhere.com/populateRatingTables',
        type: 'post',
        data: JSON.stringify({"liftID": sessionStorage.getItem('myLiftID'), "userID": sessionStorage.getItem('userID')})
    })
        .fail(function (jqXHR, textStatus, errorThrown) {
            console.log('AJAX ERROR\njqXHR: ' + jqXHR + '\ntext status: ' + textStatus + '\nError thrown: ' + errorThrown);
        })
        .done(function (data) {
            console.log('returned data: ' + data);
            var result= JSON.parse(data);
            var table = $('#ratingTbl');
            var tr = '';
            var trID ='';
            var tdID = '';
            var btnID = '';
            var starID ='';
            var driverName = '';
            var driverID = 0;
            var passengerName = '';
            var passengerID = 0;
            var driverTable = $('#driverRatingTbl'); //document.getElementById('driverRatingTbl');
            driverID = result[0]["driverID"];
            driverName = result[0]["driverName"];
            console.log('driverID ' + driverID + ' ret driver ' + result[0]["driverID"]);
            if (result[0]["driverID"] == "None") {
                driverTable.hide();
                // driverTable.setAttribute('class', 'hidden');
                document.getElementById('driverHeader').setAttribute('class', 'hidden');
            }
            else {
                console.log('in driver conditional');
                for (var i = 0; i < 1; i++) {
                    trID = 'trID' + i.toString();
                    tdID = 'tdID' + i.toString();
                    btnID = 'btnID' + i.toString();
                    starID = 'input-id' + i.toString();
                    tr = '<tr style="color:#ff8800;"><td>' + driverName + '</td><td id="driverID" class="hidden">' + driverID + '</td><td><input id="input-id" value="3" type="text" class="rating" data-step="1.0" data-show-clear="false" data-size="xs" /></td></tr>';
                    driverTable.append(tr);
                }
            }
            if (result[0]["passengerID"] == "None") {
                table.hide();
                // driverTable.setAttribute('class', 'hidden');
                document.getElementById('passengerHeader').setAttribute('class', 'hidden');
            }
            else{
                for (var index = 0; index < result.length; index++)
                {
                    trID = 'trID' + index.toString();
                    tdID = 'tdID' + index.toString();
                    btnID = 'btnID' + index.toString();
                    starID = 'input-id' + index.toString();
                    passengerName = result[index]["passengerName"];
                    passengerID = result[index]["passengerID"];
                    if (passengerID != sessionStorage["passengerID"]) {
                        tr = '<tr style="color:#ff8800;"><td>' + passengerName + '</td><td id="passengerID' + index.toString() + '" class="hidden">' + passengerID + '</td><td><input id="input-id' + index.toString() + '" data-step="1.0" type="text" value="3" class="rating" data-show-clear="false" data-size="xs" /></td></tr>';
                        console.log('name: ' + passengerName);
                        table.append(tr);
                    }
                }
            }

            var driverStar = $('#input-id');
            var star1 =  $('#input-id0');
            var star2 =  $('#input-id1');
            var star3 =  $('#input-id2');
            var star4 =  $('#input-id3');
            var star5 =  $('#input-id4');
            var star6=  $('#input-id5');

            //display the stars
            driverStar.rating({showCaption:false});
            star1.rating({showCaption: false});
            star2.rating({showCaption: false});
            star3.rating({showCaption: false});
            star4.rating({showCaption: false});
            star5.rating({showCaption: false});
            star6.rating({showCaption: false});
        })

}

function checkAllRated(){
    var driverID = 0;
    var driverRating = 0;
    if ($("#driverID").html()){
        driverID = document.getElementById('driverID').innerHTML;
        console.log('driver id ' + driverID);
        driverRating = document.getElementById('input-id').value;
        console.log('driver rating ' + driverRating);
    }
    var length = document.getElementById('ratingTbl').rows.length -1;
    console.log('number of rows: ' + length + ' ' + typeof length);
    var ratingid = '';
    var passengersIDandRating = [];
    var passengerID = '';
    for (var index = 0; index < length; index++){
        ratingid = 'input-id' + index.toString();
        passengerID = 'passengerID' +index.toString();
        console.log('index value: ' + index + ' passengerID ' + passengerID + ' rating: ' +  ratingid);
        passengersIDandRating.push([document.getElementById(passengerID).innerHTML, document.getElementById(ratingid).value]);
    }

    console.log('rating: ' + passengersIDandRating);
    $.ajax({
        url: 'http://looprac.pythonanywhere.com/rateUsers',
        type: 'post',
        data: JSON.stringify({'driverID': driverID, 'driverRating': driverRating, 'passengerData': passengersIDandRating})
    })
        .fail(function (jqXHR, textStatus, errorThrown) {
            console.log('AJAX ERROR\njqXHR: ' + jqXHR + '\ntext status: ' + textStatus + '\nError thrown: ' + errorThrown);
        })
        .done(function (data) {
            var result = JSON.parse(data);
            if (result['ratings'] == 'complete'){
                alert('Thank you for rating the other passengers.  You will now be shown what experience you got from this journey');
                window.location = "experience.html";
            }
        })

}

function calculateExperience(userID, distance, liftID, driverID){
    console.log('driver ID ' + sessionStorage.getItem('myDriverID'));
    $.ajax({
        url: 'http://looprac.pythonanywhere.com/checkIfDriver',
        type: 'post',
        data: JSON.stringify({'liftID': liftID, 'driverID': driverID})
    })
        .fail(function (jqXHR, textStatus, errorThrown) {
            console.log('AJAX ERROR\njqXHR: ' + jqXHR + '\ntext status: ' + textStatus + '\nError thrown: ' + errorThrown);
        })
        .done(function (data) {
                var result = JSON.parse(data);
                if (result["is driver"] == 'true'){
                    console.log('is driver');
                    calculateDriverExperience(userID, distance, sessionStorage.getItem('numOfPassengers'));
                }
                else {
                    console.log('is a passenger');
                    calculatePassengerExperience(userID, distance);
                }
        })
}

function calculateDriverExperience(userID, distance, numOfPassengers){
    //driver experience is calculated by getting (10 + number of passengers) % of the distance of the journey
    var driverMultiplier = (10 + numOfPassengers) * 1/100;
    var newExperience = parseFloat(distance) * driverMultiplier;
    document.getElementById('newExpHeader').innerHTML = newExperience.toString() + ' XP';
    document.getElementById('distance').value = distance;
    document.getElementById('numOfPassengers').value = numOfPassengers;
    $.ajax({
        url: 'http://looprac.pythonanywhere.com/getExperience',
        type: 'post',
        data: JSON.stringify({'userID': userID, 'newExp': newExperience, 'distance': parseFloat(distance), 'numOfPassengers': numOfPassengers})
    })
        .fail(function (jqXHR, textStatus, errorThrown) {
            console.log('AJAX ERROR\njqXHR: ' + jqXHR + '\ntext status: ' + textStatus + '\nError thrown: ' + errorThrown);
        })
        .done(function (data) {
            var result = JSON.parse(data);
            console.log(data);
            document.getElementById('overallExpHeader').innerHTML = result[0]["experience"] + ' XP';
            document.getElementById('overallDistance').value = result[0]["overall distance"] + ' km';
            document.getElementById('overallNumOfPassengers').value = result[0]["overall passengers"];
        })

}

function calculatePassengerExperience(userID, distance){
    document.getElementById('overallnumOfPassengers').setAttribute('class', 'hidden');
    document.getElementById('numOfPassengers').setAttribute('class','hidden');
    document.getElementById('overallnumOfPassengersLbl').setAttribute('class', 'hidden');
    document.getElementById('numOfPassengersLbl').setAttribute('class','hidden');
    //passenger experience is calculated by getting 10% of the distance of the journey
    var newExperience = parseFloat(distance) * .1;
    document.getElementById('newExpHeader').innerHTML = newExperience.toString() + ' XP';
    document.getElementById('distance').value = distance;
    $.ajax({
        url: 'http://looprac.pythonanywhere.com/getExperience',
        type: 'post',
        data: JSON.stringify({'userID': userID, 'newExp': newExperience, 'distance': parseFloat(distance), 'numOfPassengers': 0})
    })
        .fail(function (jqXHR, textStatus, errorThrown) {
            console.log('AJAX ERROR\njqXHR: ' + jqXHR + '\ntext status: ' + textStatus + '\nError thrown: ' + errorThrown);
        })
        .done(function (data) {
            var result = JSON.parse(data);
            console.log(data);
            document.getElementById('overallExpHeader').innerHTML = result[0]["experience"] + ' XP';
            document.getElementById('overallDistance').value = result[0]["overall distance"] + ' km';
        })
}

function passengerActiveLift() {
    document.getElementById('startLiftBtn').setAttribute('class', 'liftActiveBtn col-xs-12');
    document.getElementById('startLiftBtn').value = "Active!";
    document.getElementById('liftDetailsBtnDiv').setAttribute('class', 'hidden');
    checkIfLiftFinished();

}


function checkIfCanDepart() {
    console.log('in');
    navigator.geolocation.getCurrentPosition(onSuccess, onError, { timeout: 7000 , enableHighAccuracy: true});
    function onSuccess(position){
        var currentDateTime = new Date();
        var now = new Date().toLocaleTimeString();
        var departTime = document.getElementById('departTimeRdOnly').value;
        var departDate = document.getElementById('departDateRdOnly').value;
        var formattedDepartDate = new Date(departDate).toLocaleDateString();
        var formattedDepartTime = toDate(departTime,"h:m");
        var combinedDepartInfo = new Date(formattedDepartDate + ' ' + formattedDepartTime);
        var today = formattedDepartDate;
        var myLocation = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
        console.log('my local ' + myLocation);
        // var myLatLng = new google.maps.LatLng()
        var startLocation = new google.maps.LatLng(sessionStorage.getItem('myLiftStartLat'), sessionStorage.getItem('myLiftStartLng'));
        var distance = calcDistance(startLocation, myLocation);
        var numOfPassengers = document.getElementById('hiddenNumOfPassengers').value;
        if (numOfPassengers > 0)
        {
            console.log('date: ' + today + ' time: ' + now + ' d: ' + formattedDepartDate + ' formatted time: ' + formattedDepartTime
                + ' combined: ' + combinedDepartInfo + ' currentDateTime ' + currentDateTime.getTime());
            if (formattedDepartDate === today){
                console.log('Dates Match');
                var timeDifferenceMilliseconds = combinedDepartInfo.getTime() - currentDateTime.getTime();
                var x = timeDifferenceMilliseconds /1000;
                var seconds = Math.floor(x % 60);
                x /= 60;
                var minutes =Math.floor(x % 60);
                x /= 60;
                var hours = Math.floor(x % 24);
                x /= 24;
                var days = Math.floor(x);
                console.log('time difference, day: ' + days + ' hours: ' + hours + ' minutes: ' + minutes );
                //FOR TESTING
                hours = 0;
                minutes =4;
                if (hours == 0 && minutes < 5){
                    //for the driver
                    if(sessionStorage.getItem('myDriverID') == document.getElementById('hiddenDriverID').value){
                        window.location = "groupJourneyDisplay.html";
                    }
                    else{
                        passengerActiveLift();
                    }
                }
                else{
                    alert('Sorry, it is to early to start this lift from the agreed time');
                }
            }
            else{
                alert('Sorry, but it is too early to begin this trip.  It is not scheduled to depart until ' + formattedDepartDate);
            }
        }
        else{
            alert('Sorry, but to begin this lift you need at least one passenger.  Try "My Requests" to see if anyone' +
                ' has requested to join this trip')
        }
    }
    function onError (error) {
        console.log('in ERROR ' + error);
        switch (error.code) {
            case error.TIMEOUT:
                refresh();
                break;
            case error.PERMISSION_DENIED:
                if(error.message.indexOf("Only secure origins are allowed") == 0) {
                    tryAPIGeolocation();

                }
                break;
            case error.POSITION_UNAVAILABLE:
                alert("Please ensure your GPS is turned on !\n\nPosition unavailable.");
                break;
            case error.code == 1:
                alert("You have decided not to share your location.");
                break;
            case error.code == 2:
                alert("The positioning service cannot be reached at this time.");
                break;
            case error.code == 3:
                alert("The attempt timed out before it could get the location data.");
                break;
        }
    }
    var tryAPIGeolocation = function() {
        jQuery.post( "https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyAXN5xs4epnIsoBhsQnTHBKN5bGiPdbPUc", function(success) {
            apiGeolocationSuccess(
                {
                    coords:
                        {
                            latitude: success.location.lat,
                            longitude: success.location.lng
                        }
                });
        })
            .fail(function(err) {
                alert("API Geolocation error! \n\n"+err);
            });
    };
    var apiGeolocationSuccess = function(position) {
        // var today = new Date().toLocaleDateString();
        var currentDateTime = new Date();
        var now = new Date().toLocaleTimeString();
        // console.log('Time: ' + time + ' Date: ' + date);
        var departTime = document.getElementById('departTimeRdOnly').value;
        var departDate = document.getElementById('departDateRdOnly').value;
        var formattedDepartDate = new Date(departDate).toLocaleDateString();
        var formattedDepartTime = toDate(departTime,"h:m");
        var combinedDepartInfo = new Date(formattedDepartDate + ' ' + formattedDepartTime);
        var today = formattedDepartDate;
        var myLocation = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
        console.log('my local ' + myLocation);
        // var myLatLng = new google.maps.LatLng()
        var startLocation = new google.maps.LatLng(sessionStorage.getItem('myLiftStartLat'), sessionStorage.getItem('myLiftStartLng'));
        console.log('my local type ' + typeof  myLocation);
        calcDistance(startLocation, myLocation);
        var d = sessionStorage.getItem('distance');
        var distance = d.substring(0, d.indexOf(' '));

        //FOR TESTING
        distance = .5;

        console.log('distance : ' + distance);
        var numOfPassengers = document.getElementById('hiddenNumOfPassengers').value;
        if (numOfPassengers > 0)
        {
            console.log('date: ' + today + ' time: ' + now + ' d: ' + formattedDepartDate + ' formatted time: ' + formattedDepartTime
                + ' combined: ' + combinedDepartInfo + ' currentDateTime ' + currentDateTime.getTime());
            if (formattedDepartDate === today){
                console.log('Dates Match');
                var timeDifferenceMilliseconds = combinedDepartInfo.getTime() - currentDateTime.getTime();
                var x = timeDifferenceMilliseconds /1000;
                var seconds = Math.floor(x % 60);
                x /= 60;
                var minutes =Math.floor(x % 60);
                x /= 60;
                var hours = Math.floor(x % 24);
                x /= 24;
                var days = Math.floor(x);
                console.log('time difference, day: ' + days + ' hours: ' + hours + ' minutes: ' + minutes );
                //FOR TESTING
                hours = 0;
                minutes =4;
                if (hours == 0 && minutes < 5){
                    console.log('time is within 5 mins');
                    if (distance <= .5 ){
                        //for the driver
                        if(sessionStorage.getItem('myDriverID') == document.getElementById('hiddenDriverID').value){
                            window.location = "groupJourneyDisplay.html";
                        }
                        else{
                            passengerActiveLift();
                        }
                    }
                    else{
                        alert('Sorry, but your current location is too far from start location. Please move closer to the area shown on map as A');
                    }
                }
                else{
                    alert('Sorry, it is too early to start this lift from the agreed time');
                }
            }
            else{
                alert('Sorry, but it is too early to begin this trip.  It is not scheduled to depart until ' + formattedDepartDate);
            }
        }
        else{
            alert('Sorry, but to begin this lift you need at least one passenger.  Try "My Requests" to see if anyone' +
                ' has requested to join this trip')
        }
    };
    google.maps.event.addDomListener(window, 'load', onSuccess);
}

//convert str time from MySQL into valid datetime format
function toDate(str, format){
    console.log('toDate function, str: ' + str + ' format: ' + format);
    var trimmed = str.substring(0, str.length -3);
    console.log('trimmed: ' + trimmed);
    var converted = new Date();
    if (format == "h:m"){
        converted.setHours(trimmed.substr(0, trimmed.indexOf(":")));
        converted.setMinutes(trimmed.substr(trimmed.indexOf(":")+1));
        converted.setSeconds(0);
        console.log('now: ', converted);
        return converted.toLocaleTimeString();
    }
    else{
        console.log('wrong format');
        return 'Invalid Format';
    }
}

function displayActiveLift(liftID){
    navigator.geolocation.getCurrentPosition(onSuccess, onError, { timeout: 7000 , enableHighAccuracy: true});
    function onSuccess(position){
        console.log('liftID ' +  liftID);
        document.getElementById('liftID').value = liftID;
        var startLat = sessionStorage.getItem('myLiftStartLat');
        var startLng = sessionStorage.getItem('myLiftStartLng');
        var destLat = sessionStorage.getItem('myLiftDestinationLat');
        var destLng = sessionStorage.getItem('myLiftDestinationLng');
        console.log('start ' + startLat + ' ' + startLng + ' destination ' + destLat + ' ' + destLng);

        var startLatlng = new google.maps.LatLng(startLat,startLng);
        var destLatLng = new google.maps.LatLng(destLat, destLng);
        var myLat = position.coords.latitude;
        var myLng = position.coords.longitude;
        var myLatlng = new google.maps.LatLng(myLat, myLng);
        var mapOptions = {zoom: 17,center: myLatlng};
        var map = new google.maps.Map(document.getElementById('map'), mapOptions);
        // calcRoute(startLatlng, destLatLng, map );
        var start =  new google.maps.Marker({position: startLatlng, map: map, label: ' A '});
        var end =  new google.maps.Marker({position: destLatLng, map: map, label: ' B '});
        var myLocation = new google.maps.Marker({position: myLatlng, map: map, label: ' Me '});
        var finishCircle = new google.maps.Circle({
            strokeColor: '#FF0000',
            strokeOpacity: 0.8,
            strokeWeight: 2,
            fillColor: '#FF0000',
            fillOpacity: 0.35,
            map: map,
            center: destLatLng,
            radius: 500
        });
    }
    function onError (error) {
        console.log('in ERROR ' + error);
        switch (error.code) {
            case error.TIMEOUT:
                refresh();
                break;
            case error.PERMISSION_DENIED:
                if(error.message.indexOf("Only secure origins are allowed") == 0) {
                    tryAPIGeolocation();

                }
                break;
            case error.POSITION_UNAVAILABLE:
                alert("Please ensure your GPS is turned on !\n\nPosition unavailable.");
                break;
            case error.code == 1:
                alert("You have decided not to share your location.");
                break;
            case error.code == 2:
                alert("The positioning service cannot be reached at this time.");
                break;
            case error.code == 3:
                alert("The attempt timed out before it could get the location data.");
                break;
        }
    }
    var tryAPIGeolocation = function() {
        jQuery.post( "https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyAXN5xs4epnIsoBhsQnTHBKN5bGiPdbPUc", function(success) {
            apiGeolocationSuccess(
                {
                    coords:
                        {
                            latitude: success.location.lat,
                            longitude: success.location.lng
                        }
                });
        })
            .fail(function(err) {
                alert("API Geolocation error! \n\n"+err);
            });
    };
    var apiGeolocationSuccess = function(position) {
            console.log('liftID ' + liftID);
            document.getElementById('liftID').value = liftID;
            var startLat = sessionStorage.getItem('myLiftStartLat');
            var startLng = sessionStorage.getItem('myLiftStartLng');
            var destLat = sessionStorage.getItem('myLiftDestinationLat');
            var destLng = sessionStorage.getItem('myLiftDestinationLng');
            console.log('start ' + startLat + ' ' + startLng + ' destination ' + destLat + ' ' + destLng);

            var startLatlng = new google.maps.LatLng(startLat, startLng);
            var destLatLng = new google.maps.LatLng(destLat, destLng);
            window.sessionStorage.setItem('destinationLat', destLat);
            window.sessionStorage.setItem('destinationLng', destLng);
            var driverLat = position.coords.latitude;
            var driverLng = position.coords.longitude;
            var driverLatlng = new google.maps.LatLng(driverLat, driverLng);
            var mapOptions = {zoom: 11, center: driverLatlng};
            var map = new google.maps.Map(document.getElementById('map'), mapOptions);
            var start = new google.maps.Marker({position: startLatlng, map: map, label: ' A '});
            var end = new google.maps.Marker({position: destLatLng, map: map, label: ' B '});
            var driverLocation = new google.maps.Marker({position: driverLatlng, map: map, label: ' Me '});
            //creates a red circle on map at destination with a raidus of 500m to show where they can complete journey
            var finishCircle = new google.maps.Circle({
                strokeColor: '#FF0000',
                strokeOpacity: 0.8,
                strokeWeight: 2,
                fillColor: '#FF0000',
                fillOpacity: 0.35,
                map: map,
                center: destLatLng,
                radius: 500
            });
        };

    google.maps.event.addDomListener(window, 'load', onSuccess);
}

function checkIfLiftFinished() {
    var liftID = sessionStorage.getItem('myLiftID');
    $.ajax({
        url: 'http://looprac.pythonanywhere.com/checkIfLiftFinished',
        type: 'post',
        data: JSON.stringify({'liftID': liftID})
    })
        .fail(function (jqXHR, textStatus, errorThrown) {
            console.log('AJAX ERROR\njqXHR: ' + jqXHR + '\ntext status: ' + textStatus + '\nError thrown: ' + errorThrown);
        })
        .done(function (data) {
            var result = JSON.parse(data);
            if (result["status"] == "lift finished" ){
                alert('lift finished! You will be brought to the ratings page next.');
                window.location = "liftComplete.html";
            }
            else{
                //runs function every 15 seconds to see if lift has been completed by driver
                window.setInterval(checkIfLiftFinished, 15000);
                console.log('Not yet finished. Check again in 15 seconds.')
            }
        })
}
function checkIfCanFinish(){
    navigator.geolocation.watchPosition(onSuccess, onError, { timeout: 7000 , enableHighAccuracy: true});
    function onSuccess(position){
        var driverLocation = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
        var destLat = sessionStorage.getItem('myLiftDestinationLat');
        var destLng = sessionStorage.getItem('myLiftDestinationLng');
        var startLat = sessionStorage.getItem('myLiftStartLat');
        var startLng = sessionStorage.getItem('myLiftStartLng');
        var startLatLng = new google.maps.LatLng(startLat, startLng);
        var destLatLng = new google.maps.LatLng(destLat, destLng);
        console.log('destlat ' + destLat + ' destlng ' + destLng);
        calcDistance(destLatLng, driverLocation);
        var d = sessionStorage.getItem('distance');
        var distance = d.substring(0, d.indexOf(' '));
        var mapOptions = {zoom: 11,center: driverLocation};
        var map = new google.maps.Map(document.getElementById('map'), mapOptions);
        var marker;
        //FOR TESTING

        distance = .3;

        if (distance <= .5){
            console.log('COMPLETE');
            calcDistance(startLatLng, destLatLng);
            d = sessionStorage.getItem('distance');
            distance = d.substring(0, d.indexOf(' '));
            window.sessionStorage.setItem('liftDistance', distance);
            console.log('distance ' + sessionStorage.getItem('distance') + ' lift distance ' + sessionStorage.getItem('liftDistance'));
            marker = new google.maps.Marker({position: driverLocation, map: map, label: ' Me '});
            completeLiftAndFilterRatingList(sessionStorage.getItem('myLiftID'), sessionStorage.getItem('liftDistance'));
            window.location = "liftComplete.html";
        }
        else{
            marker = new google.maps.Marker({position: driverLocation, map: map, label: ' Me '});
            alert('Sorry, you are too far from the destination to complete it.  Get within 500 meters to complete journey');
        }
    }
    function onError (error) {
        console.log('in ERROR ' + error);
        switch (error.code) {
            case error.TIMEOUT:
                refresh();
                break;
            case error.PERMISSION_DENIED:
                if(error.message.indexOf("Only secure origins are allowed") == 0) {
                    tryAPIGeolocation();

                }
                break;
            case error.POSITION_UNAVAILABLE:
                alert("Please ensure your GPS is turned on !\n\nPosition unavailable.");
                break;
            case error.code == 1:
                alert("You have decided not to share your location.");
                break;
            case error.code == 2:
                alert("The positioning service cannot be reached at this time.");
                break;
            case error.code == 3:
                alert("The attempt timed out before it could get the location data.");
                break;
        }
    }
    var tryAPIGeolocation = function() {
        jQuery.post( "https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyAXN5xs4epnIsoBhsQnTHBKN5bGiPdbPUc", function(success) {
            apiGeolocationSuccess(
                {
                    coords:
                        {
                            latitude: success.location.lat,
                            longitude: success.location.lng
                        }
                });
        })
            .fail(function(err) {
                alert("API Geolocation error! \n\n"+err);
            });
    };
    var apiGeolocationSuccess = function(position) {
        var driverLocation = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
        var destLat = sessionStorage.getItem('myLiftDestinationLat');
        var destLng = sessionStorage.getItem('myLiftDestinationLng');
        var startLat = sessionStorage.getItem('myLiftStartLat');
        var startLng = sessionStorage.getItem('myLiftStartLng');
        var startLatLng = new google.maps.LatLng(startLat, startLng);
        var destLatLng = new google.maps.LatLng(destLat, destLng);
        console.log('destlat ' + destLat + ' destlng ' + destLng);
        calcDistance(destLatLng, driverLocation);
        var d = sessionStorage.getItem('distance');
        var distance = d.substring(0, d.indexOf(' '));
        var mapOptions = {zoom: 11,center: driverLocation};
        var map = new google.maps.Map(document.getElementById('map'), mapOptions);
        var marker;
        //FOR TESTING

        distance = .3;

        if (distance <= .5){
            console.log('COMPLETE');
            calcDistance(startLatLng, destLatLng);
            d = sessionStorage.getItem('distance');
            distance = d.substring(0, d.indexOf(' '));
            window.sessionStorage.setItem('liftDistance', distance);
            console.log('distance ' + sessionStorage.getItem('distance') + ' lift distance ' + sessionStorage.getItem('liftDistance'));
            marker = new google.maps.Marker({position: driverLocation, map: map, label: ' Me '});
            completeLiftAndFilterRatingList(sessionStorage.getItem('myLiftID'), sessionStorage.getItem('liftDistance'));
            window.location = "liftComplete.html";
        }
        else{
            marker = new google.maps.Marker({position: driverLocation, map: map, label: ' Me '});
            alert('Sorry, you are too far from the destination to complete it.  Get within 500 meters to complete journey');
        }
    };
    google.maps.event.addDomListener(window, 'load', onSuccess);
}

/***********************************************
 *      PROFILE PAGE
 */

function populateProfile(userID){
    $.ajax({
        url: 'http://looprac.pythonanywhere.com/profile',
        type: 'post',
        data: JSON.stringify({'userID': userID})
    })
        .fail(function (jqXHR, textStatus, errorThrown) {
            console.log('AJAX ERROR\njqXHR: ' + jqXHR + '\ntext status: ' + textStatus + '\nError thrown: ' + errorThrown);
        })
        .done(function (data) {
            console.log(data);
            var result = JSON.parse(data);
            document.getElementById('profileCreated').value = result["created"];
            document.getElementById('profileName').innerHTML= result["name"];
            document.getElementById('profileEmail').value = result["email"];
            document.getElementById('profilePhone').value = result["phone"];
            document.getElementById('profileRating').value = result["rating"];
            document.getElementById('profileRatingAmt').value = '( ' +  result["numOfRatings"] + ' )';
            document.getElementById('profileExp').value = result["experience"];
            document.getElementById('profileDistance').value = result["overallDistance"];
            if(result["carMake"] == "None"){
                document.getElementById('profileCarDetailsDiv').setAttribute('class', 'hidden');
            }
            else{
                document.getElementById('profileCarMake').value = result["carMake"];
                document.getElementById('profileCarModel').value = result["carModel"];
                document.getElementById('profileCarReg').value = result["carReg"];
            }
            $('#profileRating').rating({showCaption:false});
        })
}

/*********************************************
  GOOGLE API FUNCTION CALLS FOR OFFER LIFT FORM
 */



// api call that displays the route between start and destination on map
function calcRoute(startLatLng, destLatLng, map){
    console.log('in calcRoute');
    var directionsService = new google.maps.DirectionsService;
    var directionsDisplay = new google.maps.DirectionsRenderer;
    directionsDisplay.setMap(map);
    var request ={
        origin: startLatLng,
        destination: destLatLng,
        travelMode: 'DRIVING',
        unitSystem: google.maps.UnitSystem.METRIC
    };
    directionsService.route(request, function(result, status){
        if (status == 'OK'){
            console.log('in success ');
            directionsDisplay.setDirections(result);
        }
        else{
            console.log('not successful');
            console.log('Directions request failed due to ' + status);
        }
    });
    console.log('end of calc route');
}

//api call for getting distance between points on google maps
function calcDistance(startLatLng, destLatLng){
    console.log('calc distance func');
    var service = new google.maps.DistanceMatrixService;
    service.getDistanceMatrix({
        origins: [startLatLng],
        destinations: [destLatLng],
        travelMode: 'DRIVING',
        unitSystem: google.maps.UnitSystem.Metric
    }, function (response, status) {
        if (status != google.maps.DistanceMatrixStatus.OK){
            console.log('Error was: ' + status);
        }
        else{
            var originList = response.originAddresses;
            var destinationList = response.destinationAddresses;
            var distance = response.rows[0].elements[0].distance.text;
            window.sessionStorage.setItem('distance', distance);
            // var outputDiv = document.getElementById('output');
            // outputDiv.innerHTML = '';
           console.log('origin list: ' + originList + '\n' + 'destination list: ' + destinationList + '\n' + 'distance: ' + distance);
           return distance;
        }
    })
}

function showLift(startLat, startLng, destinationLat, destinationLng, mapID){
    navigator.geolocation.getCurrentPosition(onSuccess, onError, { timeout: 7000 , enableHighAccuracy: true});
    console.log('in show lift func');
    function onSuccess(position) {
        //Google Maps
        var startLatlng = new google.maps.LatLng(startLat,startLng);
        var destLatLng = new google.maps.LatLng(destinationLat, destinationLng);
        var mapOptions = {zoom: 7,center: startLatlng};
        var map = new google.maps.Map(document.getElementById(mapID), mapOptions);

        console.log('in success, before calcRoute call');
        calcRoute(startLatlng, destLatLng, map);
        var distance = calcDistance(startLatlng, destLatLng);
        console.log('distance ' + distance);
        var markers = [startLatlng, destLatLng];
        for (var i = 0; i <= markers.length; i ++)
        {
            var marker = new google.maps.Marker({position: markers[i],map: map});
        }

    }
    function onError (error) {
        console.log('in ERROR ' + error);
        switch (error.code) {
            case error.TIMEOUT:
                refresh();
                break;
            case error.PERMISSION_DENIED:
                if(error.message.indexOf("Only secure origins are allowed") == 0) {
                    tryAPIGeolocation();

                }
                break;
            case error.POSITION_UNAVAILABLE:
                alert("Please ensure your GPS is turned on !\n\nPosition unavailable.");
                break;
            case error.code == 1:
                alert("You have decided not to share your location.");
                break;
            case error.code == 2:
                alert("The positioning service cannot be reached at this time.");
                break;
            case error.code == 3:
                alert("The attempt timed out before it could get the location data.");
                break;
        }
    }
    var tryAPIGeolocation = function() {
        jQuery.post( "https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyAXN5xs4epnIsoBhsQnTHBKN5bGiPdbPUc", function(success) {
            apiGeolocationSuccess(
                {
                    coords:
                        {
                            latitude: success.location.lat,
                            longitude: success.location.lng
                        }
                });
        })
            .fail(function(err) {
                alert("API Geolocation error! \n\n"+err);
            });
    };
    var apiGeolocationSuccess = function(position) {
        var startLatlng = new google.maps.LatLng(startLat,startLng);
        var destLatLng = new google.maps.LatLng(destinationLat, destinationLng);
        var mapOptions = {zoom: 7,center: startLatlng};
        var map = new google.maps.Map(document.getElementById(mapID), mapOptions);
        var markers = [startLatlng, destLatLng];
        for (var i = 0; i <= markers.length; i ++)
        {
            var marker = new google.maps.Marker({position: markers[i],map: map});

        }
    };
    google.maps.event.addDomListener(window, 'load', onSuccess);
}





function geocodeCoords(lat, lng, elementID){
    var geocoder = new google.maps.Geocoder;
    var latLng = new google.maps.LatLng(lat, lng);
    var address = "";
   geocoder.geocode({'latLng': latLng}, function check(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            console.log('IN IF STATEMENT');
            if (results[0]) {
                var address = "";
                address = results[0].formatted_address;

                // console.log('IN SECOND IF STATEMENT ' +  dfd.state());

            }
        }
       console.log('address: ' + address);

       document.getElementById(elementID).value = address;

   });

}

function mainPageMap(){
    console.log('main map function');
    $.ajax({
        url: 'http://looprac.pythonanywhere.com/getLifts',
        type: 'post',
        data: JSON.stringify({"passengerID": sessionStorage.getItem("passengerID")})
    })
        .fail(function (jqXHR, textStatus, errorThrown) {
            console.log('AJAX ERROR\njqXHR: ' + jqXHR + '\ntext status: ' + textStatus + '\nError thrown: ' + errorThrown);
        })
        .done(function (data) {
            var result = JSON.parse(data);
            var customIcon = {
                url: 'https://www.pythonanywhere.com/user/Looprac/files/home/Looprac/LoopracAPI/icons/icon.png',
                scaledSize: new google.maps.Size(60, 60), // scaled size
                origin: new google.maps.Point(0,0), // origin
                anchor: new google.maps.Point(30, 60) // anchor
            };
            console.log('result: ' + data);
            navigator.geolocation.getCurrentPosition(onSuccess, onError, {timeout: 7000, enableHighAccuracy: true});
            function onSuccess(position) {

                var infoWindow = new google.maps.InfoWindow;
                var lat = position.coords.latitude;
                var lang = position.coords.longitude;
                var  i;
                var myLatlng = new google.maps.LatLng(lat, lang);
                var mapOptions = {zoom: 20, center: myLatlng};
                var map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
                var locationStartLat;
                var locationStartLng;
                var locationLatLng;
                var mylocation = new google.maps.Marker({position: myLatlng, map: map, label: ' Me '});
                if (result["available lifts"] == "yes") {
                    for (i = 0; i < result.length; i++) {
                        console.log('marker creation ' + result[i]["startLat"] + ' ' + result[i]["startLng"]);
                        locationStartLat = result[i]["startLat"];
                        locationStartLng = result[i]["startLng"];
                        locationLatLng = new google.maps.LatLng(locationStartLat, locationStartLng);
                        var marker = new google.maps.Marker({
                            position: locationLatLng,
                            map: map,
                            label: i.toString(),
                            animation: google.maps.Animation.DROP
                        });
                        google.maps.event.addListener(marker, 'click', (function (marker, i) {
                            return function () {
                                infoWindow.setContent('Start Point');
                                infoWindow.open(map, marker);
                                expandLift(result[i]["liftID"], result[i]["driverID"]);
                            }
                        })(marker, i));
                    }
                }



            }

            function onError(error) {
                switch (error.code) {
                    case error.TIMEOUT:
                        refresh();
                        break;
                    case error.PERMISSION_DENIED:
                        if (error.message.indexOf("Only secure origins are allowed") == 0) {
                            tryAPIGeolocation();

                        }
                        break;
                    case error.POSITION_UNAVAILABLE:
                        alert("Please ensure your GPS is turned on !\n\nPosition unavailable.");
                        break;
                }
            }

            var tryAPIGeolocation = function () {
                jQuery.post("https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyAXN5xs4epnIsoBhsQnTHBKN5bGiPdbPUc", function (success) {
                    apiGeolocationSuccess(
                        {
                            coords: {
                                latitude: success.location.lat,
                                longitude: success.location.lng
                            }
                        });
                })
                    .fail(function (err) {
                        alert("API Geolocation error! \n\n" + err);
                    });
            };
            var apiGeolocationSuccess = function (position) {
                var infoWindow = new google.maps.InfoWindow;
                var lat = position.coords.latitude;
                var lang = position.coords.longitude;
                var  i;
                var myLatlng = new google.maps.LatLng(lat, lang);
                var mapOptions = {zoom: 20, center: myLatlng};
                var map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
                var locationStartLat;
                var locationStartLng;
                var locationLatLng;
                var mylocation = new google.maps.Marker({position: myLatlng, map: map, label: ' Me '});
                if (result["available lifts"] == "yes") {
                    for (i = 0; i < result.length; i++) {
                        console.log('marker creation ' + result[i]["startLat"] + ' ' + result[i]["startLng"]);
                        locationStartLat = result[i]["startLat"];
                        locationStartLng = result[i]["startLng"];
                        locationLatLng = new google.maps.LatLng(locationStartLat, locationStartLng);
                        var marker = new google.maps.Marker({
                            position: locationLatLng,
                            map: map,
                            label: i.toString(),
                            animation: google.maps.Animation.DROP
                        });
                        google.maps.event.addListener(marker, 'click', (function (marker, i) {
                            return function () {
                                infoWindow.setContent('Start Point');
                                infoWindow.open(map, marker);
                                expandLift(result[i]["liftID"], result[i]["driverID"]);
                            }
                        })(marker, i));
                    }
                }
            };
            google.maps.event.addDomListener(window, 'load', onSuccess);
            //       if gps timesout prompts user to turn on GPS and it will refresh and try again
            function refresh() {
                if (confirm("Timed out\nPlease turn your GPS is turned on\n\nClick OK to try agian") == true) {
                    location.reload();
                }
            }
        })
}


function initMap(){
    navigator.geolocation.getCurrentPosition(onSuccess, onError, { timeout: 7000 , enableHighAccuracy: true});
    function onSuccess(position) {
        var lat = position.coords.latitude;
        var lang = position.coords.longitude;
        //Google Maps
        var myLatlng = new google.maps.LatLng(lat,lang);
        var mapOptions = {zoom: 20,center: myLatlng};
        var map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
        var marker = new google.maps.Marker({position: myLatlng,map: map, draggable: true, animation: google.maps.Animation.DROP});
        choseLocation(marker, map);
    }
    function onError (error) {
        switch (error.code) {
            case error.TIMEOUT:
                refresh();
                break;
            case error.PERMISSION_DENIED:
                if(error.message.indexOf("Only secure origins are allowed") == 0) {
                    tryAPIGeolocation();

                }
                break;
            case error.POSITION_UNAVAILABLE:
                alert("Please ensure your GPS is turned on !\n\nPosition unavailable.");
                break;
        }
    }
    var tryAPIGeolocation = function() {
        jQuery.post( "https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyAXN5xs4epnIsoBhsQnTHBKN5bGiPdbPUc", function(success) {
            apiGeolocationSuccess(
                {
                    coords:
                        {
                            latitude: success.location.lat,
                            longitude: success.location.lng
                        }
                });
        })
            .fail(function(err) {
                alert("API Geolocation error! \n\n"+err);
            });
    };
    var apiGeolocationSuccess = function(position) {
        var lat = position.coords.latitude;
        var long = position.coords.longitude;
        var myLatlng = new google.maps.LatLng(lat,long);
        var mapOptions = {zoom: 20,center: myLatlng};
        var map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
        var marker = new google.maps.Marker({position: myLatlng,map: map, draggable: true, animation: google.maps.Animation.DROP});
        choseLocation(marker, map);

    };
    google.maps.event.addDomListener(window, 'load', onSuccess);

    //       if gps timesout prompts user to turn on GPS and it will refresh and try again
    function refresh(){
        if(confirm("Timed out\nPlease turn your GPS is turned on\n\nClick OK to try agian") == true){
            location.reload();
        }
    }
}



function choseLocation(marker, map){
    var geocoder = new google.maps.Geocoder;
    var infowindow = new google.maps.InfoWindow;
    google.maps.event.addListener(marker, 'dragend', function (event)
    {
        var lat = this.getPosition().lat();
        var lng =this.getPosition().lng();
        var latLng = new google.maps.LatLng(lat,lng);
        document.getElementById('chosen_lat').value = lat;
        document.getElementById('chosen_long').value = lng;
        geocoder.geocode({'latLng': latLng}, function (results, status) {
            if(status == google.maps.GeocoderStatus.OK){
                if(results[0]){
                    var address = "";
                    var county = "";
                    // document.getElementById('location').value = results[0].formatted_address;
                    for(var i in results[0].address_components){
                        if(results[0].address_components[i].types.toString() == "administrative_area_level_2,political")
                        {
                            county = results[0].address_components[i].short_name;
                            console.log('county ' + county);
                        }
                        address += results[0].address_components[i].long_name;
                    }
                    document.getElementById('location').value = results[0].formatted_address;
                    document.getElementById('chosen_county').value = county;
                    infowindow.setContent(address);
                    infowindow.open(map, marker);
                }
            }
        });
    });
}

function locationChoice() {
    var startLocation = document.getElementById('location').value;
    var lat = document.getElementById('chosen_lat').value;
    var lng = document.getElementById('chosen_long').value;
    var county = document.getElementById('chosen_county').value;
    window.sessionStorage.setItem('start_local', startLocation);
    window.sessionStorage.setItem('start_local_lat', lat );
    window.sessionStorage.setItem('start_local_lng', lng);
    window.sessionStorage.setItem('start_county', county);

    window.history.back();
}



function initDestinationMap(){
    navigator.geolocation.getCurrentPosition(onSuccess, onError, { timeout: 7000 , enableHighAccuracy: true});
    function onSuccess(position) {
        var lat = position.coords.latitude;
        var lang = position.coords.longitude;
        var accuracy = position.coords.accuracy;
//            alert("coords: " + lat + '\n' + lang);

        //Google Maps
        var myLatlng = new google.maps.LatLng(lat,lang);
        var mapOptions = {zoom: 20,center: myLatlng};
        var map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
        var marker = new google.maps.Marker({position: myLatlng,map: map, draggable: true});
        chooseDestination(marker, map);
    }
    function onError (error) {
        switch (error.code) {
            case error.TIMEOUT:
                refresh();
                break;
            case error.PERMISSION_DENIED:
                if(error.message.indexOf("Only secure origins are allowed") == 0) {
                    tryAPIGeolocation();

                }
                break;
            case error.POSITION_UNAVAILABLE:
                alert("Please ensure your GPS is turned on !\n\nPosition unavailable.");
                break;
        }
    }
    var tryAPIGeolocation = function() {
        jQuery.post( "https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyAXN5xs4epnIsoBhsQnTHBKN5bGiPdbPUc", function(success) {
            apiGeolocationSuccess(
                {
                    coords:
                        {
                            latitude: success.location.lat,
                            longitude: success.location.lng
                        }
                });
        })
            .fail(function(err) {
                alert("API Geolocation error! \n\n"+err);
            });
    };
    var apiGeolocationSuccess = function(position) {
        var lat = position.coords.latitude;

        var long = position.coords.longitude;
        var myLatlng = new google.maps.LatLng(lat,long);
        var mapOptions = {zoom: 20,center: myLatlng};
        var map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
        var marker = new google.maps.Marker({position: myLatlng,map: map, draggable: true});
        chooseDestination(marker, map);

    };
    google.maps.event.addDomListener(window, 'load', onSuccess);

    //       if gps timesout prompts user to turn on GPS and it will refresh and try again
    function refresh(){
        if(confirm("Timed out\nPlease turn your GPS is turned on\n\nClick OK to try agian") == true){
            location.reload();
        }
    }
}

function chooseDestination(marker, map){
    var geocoder = new google.maps.Geocoder;
    var infowindow = new google.maps.InfoWindow;
    google.maps.event.addListener(marker, 'dragend', function (event)
    {
        var lat = this.getPosition().lat();
        var lng =this.getPosition().lng();
        var latLng = new google.maps.LatLng(lat,lng);
        document.getElementById('chosen_lat').value = lat;
        document.getElementById('chosen_long').value = lng;
        geocoder.geocode({'latLng': latLng}, function (results, status) {
            if(status == google.maps.GeocoderStatus.OK){
                if(results[0]){
                    var address = "";
                    var county = "";
                    for(var i in results[0].address_components){
                        if(results[0].address_components[i].types.toString() == "administrative_area_level_2,political")
                        {
                            county = results[0].address_components[i].short_name;
                            console.log('county ' + county);
                        }

                        address += ' ' + results[0].address_components[i].long_name;
                    }
                    document.getElementById('destination').value = results[0].formatted_address;
                    document.getElementById('chosen_county').value = county;
                    infowindow.setContent(address);
                    infowindow.open(map, marker);
                }
            }
        });
    });
}

function destinationChoice() {
    var destinationLocation = document.getElementById('destination').value;
    var lat = document.getElementById('chosen_lat').value;
    var lng = document.getElementById('chosen_long').value;
    var county = document.getElementById('chosen_county').value;

    window.sessionStorage.setItem('destination_local', destinationLocation);
    window.sessionStorage.setItem('destination_local_lat', lat );
    window.sessionStorage.setItem('destination_local_lng', lng);
    window.sessionStorage.setItem('destination_county', county);

    window.history.back();
}

function showHideModal(){
    // Get the modal
    var modal = document.getElementById('routeModal');

// Get the button that opens the modal
    var btn = document.getElementById("displayLiftBtn");

// Get the <span> element that closes the modal
    var span = document.getElementsByClassName("close")[0];

// When the user clicks on the button, open the modal
    btn.onclick = function() {
        modal.style.display = "block";
    };

// When the user clicks on <span> (x), close the modal
    span.onclick = function() {
        modal.style.display = "none";
    };

// When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    };
}



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
                window.sessionStorage.setItem('driverID', result['driverID']);
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
    console.log("LOGIN FUNCTION: after ajax");
}

function checkLoginStatus(){
    var userID = sessionStorage.getItem('userID');
    var fname = sessionStorage.getItem('firstName');
    var lname = sessionStorage.getItem('lastName');
    var passID = sessionStorage.getItem('passengerID');
    var driveID = sessionStorage.getItem('driverID');
    var loggedin = sessionStorage.getItem('loggedIn');
    console.log('session data: ' + userID + ' ' + fname + ' ' + lname + ' ' + passID + ' ' + driveID + ' ' + loggedin);


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


function SubForm(){
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
    var returnDate = document.getElementById('returnDateInput').value;
    console.log(date);
    var formattedDate = new Date(date).toMysqlFormat();
    var formattedReturnDate = new Date(returnDate).toMysqlFormat();
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
        'return_date' : formattedReturnDate,
        'return_time' : document.getElementById('returnTimeInput').value,
        'type' : document.getElementById('liftTypeInput').value,
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

function checkType(){
    var type = document.getElementById('liftTypeInput').value;
    console.log('type: ' + type);
    if (type == 'single'){
        document.getElementById('returnDateLbl').setAttribute('class','hidden');
        document.getElementById('returnTimeLbl').setAttribute('class','hidden');
        document.getElementById('returnDateInput').setAttribute('class','hidden');
        document.getElementById('returnTimeInput').setAttribute('class','hidden');
    }
    else if (type == 'return'){
        document.getElementById('returnDateLbl').classList.remove('hidden');
        document.getElementById('returnTimeLbl').classList.remove('hidden');
        document.getElementById('returnDateInput').classList.remove('hidden');
        document.getElementById('returnTimeInput').classList.remove('hidden');
    }
}

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
            console.log(result);
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
            var departDate = result[0]['departDate'];
            var departTime = result[0]['departTime'];
            var returnDate = result[0]['returnDate'];
            var returnTime = result[0]['returnTime'];
            var seats = result[0]['seats'];
            var liftType = result[0]['liftType'];
            console.log('return date and time ' + returnDate + ' ' + returnTime);
            showLift(startLat, startLng, destLat, destLng, "lift-map-canvas");
            geocodeCoords(startLat, startLng, 'startRdOnly');
            geocodeCoords(destLat, destLng, 'destinationRdOnly');
            document.getElementById('liftIDRdOnly').value = liftID;
            document.getElementById('driverRdOnly').value = driver;
            document.getElementById('departTimeRdOnly').value = departTime;
            document.getElementById('departDateRdOnly').value = departDate;
            if(returnDate != null && returnTime != null)
            {
                document.getElementById('returnDateRdOnly').value = returnDate;
                document.getElementById('returnTimeRdOnly').value = returnTime;
            }
            else
            {
                document.getElementById('returnDateLbl').setAttribute('class','hidden');
                document.getElementById('returnTimeLbl').setAttribute('class','hidden');
                document.getElementById('returnDateRdOnly').setAttribute('class','hidden');
                document.getElementById('returnTimeRdOnly').setAttribute('class','hidden');
            }
            document.getElementById('seatsRdOnly').value = seats;
            document.getElementById('typeRdOnly').value = liftType;
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
            console.log('result: ' + data);
            document.getElementById('passengerNameRdOnly').value = result["name"];
            document.getElementById('departTimeRdOnly').value = result["time"];
            document.getElementById('departDateRdOnly').value = result["date"];

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
    window.sessionStorage.setItem('groupLiftID', liftID);
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

            document.getElementById('driverNameRdOnly').value =  result[0]['driverName'];
            document.getElementById('carRegRdOnly').value =  result[0]['carReg'];
            document.getElementById('driverPhoneRdOnly').value =  result[0]['driverPhone'];
            document.getElementById('routeRdOnly').value = result[0]["startCounty"] + ' To ' + result[0]["destCounty"];
            document.getElementById('departTimeRdOnly').value = result[0]["departTime"];
            document.getElementById('departDateRdOnly').value = result[0]["departDate"];
            var startLat = result[0]["startLat"];
            var startLng = result[0]["startLng"];
            var destinationLat = result[0]["destLat"];
            var destinationLng= result[0]["destLng"];
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
                paragraph = '<tr style="color:#ff8800;"><td>'+ passengerName + '</td><td>' + phone + '</td></tr>';
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
            var userID = 0;
            var route = '';
            var departingInfo= '';
            var trID = '';
            var tdID = '';
            var btnID = '';
            for (var i = 0; i < result.length ; i ++ ) {
                liftID = result[i]["liftID"];
                userID = result[i]["userID"];
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
            document.getElementById('liftTypeTitle').value =result[0]["type"];
            var startLat = result[0]["startLat"];
            var startLng = result[0]["startLng"];
            var destinationLat = result[0]["destLat"];
            var destinationLng= result[0]["destLng"];

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
                if (passengerName == "None")
                {
                    passengerName = "";
                    phone = "";
                }
                paragraph = '<tr style="color:#ff8800;"><td>'+ passengerName + '</td><td>' + phone + '</td></tr>';
                console.log('name: ' + passengerName + ' ' + 'phone: ' + phone);
                table.append(paragraph);
            }
            window.onload = showLift(startLat, startLng, destinationLat, destinationLng, "myLift-map-canvas");

        });


}

/*********************************************
  GOOGLE API FOR OFFER LIFT FORM
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
        if (status != 'OK'){
            console.log('Error was: ' + status);
        }
        else{
            var originList = response.originAddresses;
            var destinationList = response.destinationAddresses;
            var distance = response.rows[0].elements[0].distance.text;
            // var outputDiv = document.getElementById('output');
            // outputDiv.innerHTML = '';
           console.log('origin list: ' + originList + '\n' + 'destination list: ' + destinationList + '\n' + 'distance: ' + distance);
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

// Resize map to show on a Bootstrap's modal
        $('#routeModal').on('shown.bs.modal', function() {
            var currentCenter = map.getCenter();  // Get current center before resizing
            google.maps.event.trigger(map, "resize");
            map.setCenter(currentCenter); // Re-set previous center
        });
        console.log('in success, before calcRoute call');
        calcRoute(startLatlng, destLatLng, map);
        calcDistance(startLatlng, destLatLng);

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


function initMap(){
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
        var accuracy = position.coords.accuracy;
        var myLatlng = new google.maps.LatLng(lat,long);
        var mapOptions = {zoom: 20,center: myLatlng};
        var map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
        var marker = new google.maps.Marker({position: myLatlng,map: map, draggable: true});
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
        var accuracy = position.coords.accuracy;
//            alert("API geolocation success!\n\nlat = " + lat + "\nlng = " + long + '\nacc = ' + accuracy);

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

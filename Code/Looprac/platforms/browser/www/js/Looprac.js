function login(){
    console.log("LOGIN FUNCTION");
    event.preventDefault(); // prevents form submitting normally
    $.ajax({
        url:'http://looprac.pythonanywhere.com/loginuser',
        type:'post',
        async: false,
        data: $("#login_form").serialize()})
        .done(function(data){
            var result = JSON.parse(data);
            if (result["status"] == "match")
            {
                console.log("match logged in ");
                window.sessionStorage.setItem('userID', result['user_id']);
                window.sessionStorage.setItem('firstName', result['first_name']);
                window.sessionStorage.setItem('lastName', result['last_name']);
                window.sessionStorage.setItem('loggedIn', result['logged_in']);
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


function SubForm(){
    event.preventDefault(); // prevents form submitting normally
    $.ajax({
        url:'http://looprac.pythonanywhere.com/registeruser',
        type:'post',
        async: false,
        data:  $("#form").serialize()})
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
    console.log('inside func before ajax');

    $.ajax({
        url:'http://looprac.pythonanywhere.com/availableLifts',
        type:'get',
        // contentType: 'application/json',
        dataType: 'json'})
        .done(function(data){
            // var result = JSON.parse(data);
            // console.log(result);
            var table = $('#availableLiftsTbl');
            var tr = '';
            var liftID =0;
            var driverID = 0;
            var sCounty = '';
            var dCounty = '';
            var created = '';
            var trID = '';
            var tdID = '';
            var btnID = '';

            for (var i = 0; i <= data.length ; i ++ ) {
                liftID = data[i]["liftID"];
                driverID = data[i]['driverID'];
                sCounty =  data[i]['startCounty'];
                dCounty = data[i]['destinationCounty'];
                created = data[i]['created'];
                trID = 'trID' + i.toString();
                tdID = 'tdID' + i.toString();
                btnID = 'btnID' + i.toString();
                console.log(trID);
                console.log(tdID);
                tr = '<tr onclick="expandLift('+liftID +','+ driverID +')" id=' +trID + ' ><td class="hidden" id=' + tdID + '>' + liftID + '</td><td class="hidden">' + driverID + '</td><td>' + sCounty + '</td><td>' + dCounty
                    + '</td><td>' +  created + '</td></tr>';
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
        // async: false,
        // contentType: 'application/json',
        // dataType: 'json',
        data:j})
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
            var seats = result[0]['seats'];
            var liftType = result[0]['liftType'];

            showLift(startLat, startLng, destLat, destLng);
            geocodeCoords(startLat, startLng, 'startRdOnly');
            geocodeCoords(destLat, destLng, 'destinationRdOnly');
            document.getElementById('driverRdOnly').value = driver;
            document.getElementById('departTimeRdOnly').value = departTime;
            document.getElementById('departDateRdOnly').value = departDate;
            document.getElementById('seatsRdOnly').value = seats;
            document.getElementById('typeRdOnly').value = liftType;


        });
    console.log('after ajax request');
}

/*********************************************
  GOOGLE API FOR OFFER LIFT FORM
 */



function showLift(startLat, startLng, destinationLat, destinationLng){
    navigator.geolocation.getCurrentPosition(onSuccess, onError, { timeout: 5000 , enableHighAccuracy: true});
    function onSuccess(position) {
        //Google Maps
        var startLatlng = new google.maps.LatLng(startLat,startLng);
        var destLatLng = new google.maps.LatLng(destinationLat, destinationLng);
        var mapOptions = {zoom: 7,center: startLatlng};
        var map = new google.maps.Map(document.getElementById('lift-map-canvas'), mapOptions);
        var markers = [startLatlng, destLatLng];
        for (var i = 0; i <= markers.length; i ++)
        {
            var marker = new google.maps.Marker({position: markers[i],map: map});
        }

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
        var startLatlng = new google.maps.LatLng(startLat,startLng);
        var destLatLng = new google.maps.LatLng(destinationLat, destinationLng);
        var mapOptions = {zoom: 7,center: startLatlng};
        var map = new google.maps.Map(document.getElementById('lift-map-canvas'), mapOptions);
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
    navigator.geolocation.getCurrentPosition(onSuccess, onError, { timeout: 5000 , enableHighAccuracy: true});
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
//            alert("API geolocation success!\n\nlat = " + lat + "\nlng = " + long + '\nacc = ' + accuracy);

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
    navigator.geolocation.getCurrentPosition(onSuccess, onError, { timeout: 5000 , enableHighAccuracy: true});
    function onSuccess(position) {
        var lat = position.coords.latitude;
        var lang = position.coords.longitude;
        var accuracy = position.coords.accuracy;
//            alert("coords: " + lat + '\n' + lang);

        //Google Maps
        var myLatlng = new google.maps.LatLng(lat,lang);
        var mapOptions = {zoom: 10,center: myLatlng};
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


/*******************
 AVAILABLE LIFTS
 // /*****************************/


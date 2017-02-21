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

    $.ajax({
        url:'http://looprac.pythonanywhere.com/offerLift',
        type:'post',
        async: false,
        contentType: 'application/json',
        dataType: 'json',
        data:  d})
        .done(function(data){
            // var result = JSON.parse(data);
            if (data["status"] == "registered")
            {
                alert("Your lift offer has been submitted");
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
    $.get('http://looprac.pythonanywhere.com/availableLifts',function (data, status){
        var result = JSON.parse(data);
        for (var i = 0; i <= data.length; i ++ ){
            // console.log(result[i]['liftID']);
            // console.log(result[i]['userID']);
            // console.log(result[i]['startLat']);
            // console.log(result[i]['startLng']);
            // console.log(result[i]['destinationLat']);
            // console.log(result[i]['destinationLng']);
            // console.log(result[i]['departDate']);
            // console.log(result[i]['departTime']);
            // console.log(result[i]['seats']);
            // console.log(result[i]['type']);
            // console.log(result[i]['created']);
            // console.log('\n');
            var tr = '';
            //     console.log(typeof data);
            //
            //     $.each(data, function (i, item){
            //
            //         tr += '<tr><td>' + item + '</td><td>' + item + '</td><td>' + item + '</td></tr>';
            //     });
        }
    });
    // var d = JSON.stringify({'status':'get available lifts'});
    // $.ajax({
    //     url: 'http://looprac.pythonanywhere.com/availableLifts',
    //     async: false,
    //     // contentType: 'application/json',
    //     type: 'post',
    //     dataType: 'json',
    //     data: d
    // })
    // .done(function (data) {
    //     // // var result = JSON.parse(data);
    //     console.log(data[0]);
    //     // var d = $.parseJSON( data ).d;
    //     var tr = '';
    //     console.log(typeof data);
    //
    //     $.each(data, function (i, item){
    //
    //         tr += '<tr><td>' + item + '</td><td>' + item + '</td><td>' + item + '</td></tr>';
    //     });
    // })
}

/*********************************************
  GOOGLE API PLACES FOR OFFER LIFT FORM
 */

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
    // document.getElementById('pickup_location').innerHTML = x.latLng.lat()+' , '+x.latLng.lng();
    var geocoder = new google.maps.Geocoder;
    var infowindow = new google.maps.InfoWindow;
    // var long = position.coords.longitude;
    // var myLatlng = new google.maps.LatLng(lat,long);
    // var mapOptions = {zoom: 20,center: myLatlng};
    // var map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
    // var marker = new google.maps.Marker({position: myLatlng,map: map, draggable: true});
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
                        address += results[0].address_components[i].short_name;
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


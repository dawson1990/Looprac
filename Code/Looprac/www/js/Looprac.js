function carDetailsVisibility(){
    var target = $('#carDetails');
    if(target.hasClass("hiddenDiv")){
        target.removeClass("hiddenDiv");
    }
    else{
        target.addClass("hiddenDiv");
    }
}


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
    console.log("sub form");
    $.ajax({
        url:'http://looprac.pythonanywhere.com/registeruser',
        type:'post',
        async: false,
        data: $("#form").serialize()})
        .done(function(data){
            var result = JSON.parse(data);
            if (result["status"] == "Register Complete")
            {
                alert("You are now a registered Looper :)");
                window.location.replace("login.html");
            }
            else if (result["status"] == "Not all required elements are entered")
            {
                alert("ERROR: not all fields were filled in");
            }

        });
    console.log("after subform ajax")
}


//
// function validateRegister(){
//     // var fName = document.getElementById("firstNameInput");
//     // var lName = document.getElementById("lastNameInput");
//     // var email = document.getElementById("emailInput");
//     // var phone = document.getElementById("phoneInput");
//     // var password = document.getElementById("passwordInput");
//     // var nameReg = /\d/;
//     // if (nameReg.test(fName) == true)
//     // {
//     //     alert("First Name cannot include numbers");
//     // }
//     // if (nameReg.test(LName) == true)
//     // {
//     //     alert("Last Name cannot include numbers");
//     // }
//
//
//
//
// }

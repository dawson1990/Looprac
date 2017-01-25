/**
 * Created by Kevin on 29/12/2016.

 */

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
    console.log("there");
    event.preventDefault(); // prevents form submitting normally
    $.ajax({
        url:'http://looprac.pythonanywhere.com/registeruser',
        type:'post',
        async: false,
        data: $("#form").serialize()})
        .done(function(){
            alert("You are now a registered Looper :)");
            window.location.replace("login.html");
        });
}


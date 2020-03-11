var password = document.getElementById("password"), confirm_password = document.getElementById("confirm_password");
var current_tab = "home";
var email = "";

window.alert(email);

//saves the email of the one whos is browsed for access
var currentBrowsingEmail = "";

displayView=function(view){
  //thecoderequiredtodisplayaview
  document.getElementById('content').innerHTML = view.innerHTML;

};

/*On page load*/
window.onload=function(){
  //check if token exists
  var token = localStorage.getItem("token");
  var obj = {"name" : "hello"};

  if(token){ // if user is logged in
     displayView(document.getElementById('profileView')); // load profile
     displayAccountMessages();
     displayUserInfoOnLoad();
  }
  else{
    displayView(document.getElementById('welcomeview'));
  }
};

forgotPasswordView=function(){
	displayView(document.getElementById('forgotPasswordView'));
}

//Send request to server using XMLHttpRequest
sendRequest=function(type, url, request_body, callBack){  

  if(request_body){
  	request_body["HMAC"] = encryptJSON(request_body);
  } else {
  	request_body = {"HMAC" : encryptJSON("")};
  }

  request_body["API Key"]=email;
  
  try{
    var req = new XMLHttpRequest();
    req.open(type, url, true);
    req.setRequestHeader("Content-type", "application/json");
    req.onreadystatechange = function(){
      if (this.readyState == 4){
        response = JSON.parse(req.responseText);

        callBack(response)
      }
    };
    req.send(JSON.stringify(request_body));
  }
  catch(e){
    window.alert(e);
    console.error(e);
  }
}

encryptJSON=function(object){
	stringObj = JSON.stringify(object);
	var token = localStorage.getItem("token");
	var hmac = "";

	if(token){
		var shaObj = new jsSHA("SHA-256", "TEXT");
	
		shaObj.setHMACKey(token, "TEXT");
		shaObj.update(stringObj);
		hmac = shaObj.getHMAC("HEX");
	}
	
	return hmac;
}


displayUserInfoOnLoad=function(){
  sendRequest("GET", "/get_user_data_by_token", null, displayUserInfoOnLoad_Callback)
}

displayUserInfoOnLoad_Callback = function(response){
  displayAccountInfo(response["data"], false);
}


/*Called when input is given on signup */
validatePassword=function(){
  var password = document.getElementById("password");
  var confirm_password = document.getElementById("confirm_password");
  if (password.value.trim().length <= 9) {
    password.setCustomValidity("Password not long enough");
  }
  else if(password.value.trim() != confirm_password.value.trim()){
    password.setCustomValidity("");

    confirm_password.setCustomValidity("Passwords don't match");
  }
  else {
    confirm_password.setCustomValidity("");
    password.setCustomValidity("");

  }
}

forgotPassword=function(form){
  var email = form.email.value.trim();
  var request = {"email" : email}
  

  sendRequest("PUT", "/forgot_password", request, forgotPassword_Callback);
  
  return false;
};

forgotPassword_Callback=function(response){

	var errorMessage = document.getElementById('reset_password_message');
	
	errorMessage.innerHTML = response["message"];
}


resetPassword=function(form){
  var new_password = form.new_password.value.trim();
  var password = form.password.value.trim();
  if( new_password == password){
    var errorMessage = document.getElementById('reset_password_message');
    errorMessage.innerHTML = "cannot use same password";
    return false;
  }
  var request = {"newPassword" : new_password, "oldPassword" : password}
  sendRequest("PUT", "/change_password", request, resetPassword_Callback)
  form.password.value = "";
  form.new_password.value = "";
  form.repeat_new_password.value = "";

}

resetPassword_Callback=function(response){
  var errorMessage = document.getElementById('reset_password_message');  
  errorMessage.innerHTML = response["message"];
}

/* Creates validity on password input when password is reset */
validateNewPassword=function(){
  var password = document.getElementById("new_password");
  var confirm_password = document.getElementById("repeat_new_password");
  if (password.value.trim().length <= 9) {
    password.setCustomValidity("New password not long enough");
  }
  else if(password.value.trim() != confirm_password.value.trim()){
    password.setCustomValidity("");

    confirm_password.setCustomValidity("Passwords don't match");
  }
  else {
    confirm_password.setCustomValidity("");
    password.setCustomValidity("");

  }
}


signout = function() {
  sendRequest("POST", "/sign_out", {}, signout_callback);
  return false
}

signout_callback = function(response){
  localStorage.removeItem("token");
  displayView(document.getElementById('welcomeview'));
  current_tab = "home";
}


signup=function(form){
  var firstName = form.firstName.value.trim();
  var familyName = form.familyName.value.trim();
  var gender = form.gender.value.trim();
  var city = form.city.value.trim();
  var country = form.country.value.trim();
  var email = form.email.value.trim();
  var password = form.password.value.trim();
  var repPassword = form.repPassword.value.trim();
  var request = {"email" : email, "password" : password, "firstname" : firstName
                , "familyname" : familyName, "gender" : gender, "city" : city, "country" : country};

  sendRequest("PUT", "/signup", request, signup_Callback)

  return false;
};

signup_Callback=function(response){
  var errorMessage = document.getElementById('signupMessage');
  errorMessage.innerHTML = response["message"];
}

signin=function(form){
  var email = form.email.value.trim();
  var password = form.password.value.trim();
  var request = {"email" : email, "password" : password}
  window.email = email;
  
  sendRequest("PUT", "/signin", request, signin_Callback)
  
  return false;
};

signin_Callback=function(response){
  if(response["success"]){
    var token = response["data"]["token"]
    localStorage.setItem("token", token);
    displayView(document.getElementById('profileView'));
    displayUserInfoOnLoad();
    displayAccountMessages();
    socketConnection();
  }
  else{
    var errorMessage = document.getElementById('errorLabel');
    errorMessage.innerHTML = response["message"]
  }
}

/*Called when browse button is pressed*/
browseUser = function(form){
  var request = {"email" : form.email.value.trim()}
  sendRequest("GET", "/get_user_data_by_email?email=" + form.email.value, null, browseUser_Callback);
  
  return false;
}

browseUser_Callback=function(response){
  if(response["success"]){
    displayAccountInfo(response["data"], true);
    displayAccountMessages(response["data"]["email"]);
  }
  else{
    document.getElementById("browse_user_message").innerHTML = response["message"];
  }
}


displayAccountMessages = function(email = null){
  var posts;
  var wall;

  if(!email){
    sendRequest("GET", "/get_user_messages_by_token", null ,displayAccountMessages_Mine_CallBack )
  }
  else
  {
    sendRequest("GET", "/get_user_messages_by_email?email=" +  email, null, displayAccountMessages_Other_CallBack )
  }
}

displayAccountMessages_Mine_CallBack=function(response){
  wall = document.getElementById("myWall");
  if(response["success"]){
    wall.innerHTML = "";
    messages = response["data"]["messages"];
    for(var message in messages){
      wall.innerHTML += "<div> <span>" + messages[message][0]
        + ":</span>   <span class='align-r'>" + messages[message][1] + "</span> </div>";
    }
  }

}
displayAccountMessages_Other_CallBack=function(){
  wall = document.getElementById("browseWall");
  if(response["success"]){
    wall.innerHTML = "";
    messages = response["data"]["messages"];
    for(var message in messages){
      wall.innerHTML += "<div> <span>" + messages[message][0]
        + ":</span>   <span class='align-r'>" + messages[message][1] + "</span> </div>";
    }
  }
  else{

    wall.innerHTML = "";
  }
}

displayAccountInfo = function(data, browse) {
  var user;
  var personalInfo;
  if(!browse){
  
    personalInfo = document.getElementById("personalInfo");
  }
  else {
    personalInfo = document.getElementById("personalInfoForUser");

    currentBrowsingEmail = data["email"];

  }

  personalInfo.innerHTML = "";

  for(info in data){
    personalInfo.innerHTML += "<div> <span>" + info
      + ":</span> 	<span class='align-r'>" +data[info] + "</span> </div>";
  }
}

postMessageOnMyWall = function(form){
  try{

    var req = new XMLHttpRequest();
    req.open("GET", "/get_user_data_by_token", true);
    req.setRequestHeader("Content-type", "application/json");
    req.onreadystatechange = function(){
      if (this.readyState == 4){
        if (this.status == 200){
          response = JSON.parse(req.responseText);
          postMessage(form, response["data"]["email"]);
        }else if (this.status == 400){
                    
        }
      }
      
    };
    req.send(null);
  }
    catch(e){
      window.alert(e);
    console.error(e);
  }
  return false;
}

postMessage = function(form, email = null){
  var recipient;
  if(email != null){
    recipient = email;
  }
  else {
    recipient = currentBrowsingEmail;

  }
  var message = form.contents.value;

  var request = {"email" : recipient, "message" : message}
  
  sendRequest("POST", "/post_message", request, postMessage_Callback);
  form.contents.value = "";

  return false;
}

postMessage_Callback=function(response){

}

refreshMessages = function(myWall){
  if(myWall){
    displayAccountMessages();
  }
  else{
    displayAccountMessages(currentBrowsingEmail);
  }
  return false;
}


/*Called when switching tabs*/
select=function (tab) {
  var currentTab = document.getElementById(current_tab);
  currentTab.style.backgroundColor = "lightgrey";

  var currentContent = document.getElementById(current_tab + "tab");
  currentContent.style.display = "none";

  var content = document.getElementById(tab.id + "tab");
  content.style.display = "flex";
  current_tab = tab.id;
  tab.style.backgroundColor = "grey";

}

socketConnection=function(){
  if (window.location.protocol == "https:") {
    var ws_scheme = "wss://";
  } else {
    var ws_scheme = "ws://"
  };
  var socket = new WebSocket(ws_scheme + location.host + "/websocket");

  socket.onmessage = function (socket_event){
    var event_data = socket_event.data;

    if(event_data == "logout_req"){
      localStorage.removeItem("token");
      displayView(document.getElementById('welcomeview'));
      current_tab = "home";

    };
  };
}
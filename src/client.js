var password = document.getElementById("password"), confirm_password = document.getElementById("confirm_password");
var current_tab = "home";

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

  if(token){ // if user is logged in
     displayView(document.getElementById('profileView')); // load profile
     displayAccountInfo();
     displayAccountMessages();

  }
  else{
    displayView(document.getElementById('welcomeview'));
  }

};

/*Called when input is given on signup */
validatePassword=function(){
  var password = document.getElementById("password");
  var confirm_password = document.getElementById("confirm_password");
  if (password.value.trim().length <= 9) {
    password.setCustomValidity("Password nocurrentBrowsingt long enough");
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


resetPassword=function(form){
  var new_password = form.new_password.value.trim();
  var password = form.password.value.trim();
  if( new_password == password){
    var errorMessage = document.getElementById('reset_password_message');
    errorMessage.innerHTML = "cannot use same password";
    return false;
  }
  var token = localStorage.getItem("token");
  var message = serverstub.changePassword(token,password,new_password);
  var errorMessage = document.getElementById('reset_password_message');

  if(!message["success"]){
    errorMessage.style.color = "red";
  }
  else {
    errorMessage.style.color = "green";
    form.password.value = "";
    form.new_password.value = "";
    form.repeat_new_password.value = "";
  }

  errorMessage.innerHTML = message["message"];
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
  var token = localStorage.getItem("token");
  serverstub.signOut(token)
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
  var mess = serverstub.signUp(request);
  var errorMessage = document.getElementById('signupMessage');
  errorMessage.innerHTML = mess["message"]  ;
  document.getElementById("personalInfo")

  return false; //not to refresh page
  //var info = [];
  //info = JSON.stringify(form);
  //var obj = JSON.parse(info);
};

signin=function(form){

  var email = form.email.value.trim();
  var password = form.password.value.trim();
  var mess = serverstub.signIn(email,password);
  var token = mess["data"];
  if(token != null){
    localStorage.setItem("token", token);
    displayView(document.getElementById('profileView'));
    displayAccountInfo();
    displayAccountMessages();

  }
  else{
    var errorMessage = document.getElementById('errorLabel');
    errorMessage.innerHTML = mess["message"];
  }

  return false;

};

/*Called when browse button is pressed*/
browseUser = function(form){
  displayAccountInfo(form.email.value);
  displayAccountMessages(form.email.value);
  return false;
}


displayAccountMessages = function(email = null){
  var token = localStorage.getItem("token");
  var posts;
  var wall;

  if(!email){
    posts = serverstub.getUserMessagesByToken(token);
    wall = document.getElementById("myWall");
  }
  else {
    posts = serverstub.getUserMessagesByEmail(token,email);
    wall = document.getElementById("browseWall");

  }
  wall.innerHTML = "";
  for(message in posts["data"]){
    wall.innerHTML += "<div> <span>" + posts["data"][message]["writer"]
      + ":</span> 	<span class='align-r'>" +posts["data"][message]["content"] + "</span> </div>";
  //window.alert(JSON.stringify();
  }

}

displayAccountInfo = function(email = null) {
  var token = localStorage.getItem("token");
  var user;
  var personalInfo;

  if(!email){
    user = serverstub.getUserDataByToken(token);
    personalInfo = document.getElementById("personalInfo");
  }
  else {
    user = serverstub.getUserDataByEmail(token,email);
    personalInfo = document.getElementById("personalInfoForUser");
    currentBrowsingEmail = email;

  }
  //window.alert(JSON.stringify(user));
  personalInfo.innerHTML = "";
  for(info in user["data"]){
    personalInfo.innerHTML += "<div> <span>" + info
      + ":</span> 	<span class='align-r'>" +user["data"][info] + "</span> </div>";
  }


}


postMessage = function(form, mywall = true){
  var token = localStorage.getItem("token");
  var recipient;
  if(mywall){
    var user = serverstub.getUserDataByToken(token);
    recipient = user["data"]["email"];
  }
  else {
    recipient = currentBrowsingEmail;
  }
  var message = form.contents.value;
  serverstub.postMessage(token, message, recipient);
  form.contents.value = "";
  return false;
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
  content.style.display = "block";
  current_tab = tab.id;
  tab.style.backgroundColor = "grey";

}

var password = document.getElementById("password"), confirm_password = document.getElementById("confirm_password");

displayView=function(view){
  //thecoderequiredtodisplayaview
  document.getElementById('content').innerHTML = view.innerHTML;

};

window.onload=function(){
  var token = localStorage.getItem("token");
  var user = serverstub.getUserDataByToken(token);
  var mess = serverstub.signIn(user["email"],user["password"]);

  //window.alert(JSON.stringify(mess));
  if(mess["success"]){
     displayView(document.getElementById('profileView'));
  }
  else{
    displayView(document.getElementById('welcomeview'));
  }

};


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

signout = function() {
  var token = localStorage.getItem("token");
  serverstub.signOut(token)
  localStorage.removeItem("token");
  displayView(document.getElementById('welcomeview'));
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
  errorMessage.innerHTML = mess["message"];


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

  }
  else{
    var errorMessage = document.getElementById('errorLabel');
    errorMessage.innerHTML = mess["message"];
  }

  return false;

};

signinValidation=function(form){
};

/*  */

validateNewPassword=function(){
  var password = document.getElementById("new_password");
  var confirm_password = document.getElementById("confirm_new_password");
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
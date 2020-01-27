
displayView=function(view){
  //thecoderequiredtodisplayaview
  document.getElementById('content').innerHTML = view.innerHTML;

};

window.onload=function(){
  displayView(document.getElementById('welcomeview'));
};

signupValidation=function(form){
  var firstName = form.firstName.value.trim();
  var familyName = form.familyName.value.trim();
  var gender = form.gender.value.trim();
  var city = form.city.value.trim();
  var country = form.country.value.trim();
  var email = form.email.value.trim();
  var password = form.password.value.trim();
  var repPassword = form.repPassword.value.trim();


  window.alert(firstName);

  //var info = [];
  //info = JSON.stringify(form);
  //var obj = JSON.parse(info);
};

signinValidation=function(form){
};

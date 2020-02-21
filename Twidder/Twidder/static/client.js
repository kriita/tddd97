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
     displayAccountMessages();
     displayUserInfoOnLoad();
  }
  else{
    displayView(document.getElementById('welcomeview'));
  }

};

displayUserInfoOnLoad=function(){
  var token = localStorage.getItem("token");
  try{

    var req = new XMLHttpRequest();
    req.open("GET", "/get_user_data_by_token?token=" + token, true);
    req.setRequestHeader("Content-type", "application/json");
    req.onreadystatechange = function(){
      if (this.readyState == 4){
        if (this.status == 200){

          response = JSON.parse(req.responseText);
          displayAccountInfo(response["data"], false);
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


resetPassword=function(form){
  var new_password = form.new_password.value.trim();
  var password = form.password.value.trim();
  if( new_password == password){
    var errorMessage = document.getElementById('reset_password_message');
    errorMessage.innerHTML = "cannot use same password";
    return false;
  }
  var token = localStorage.getItem("token");
  var request = {"token" : token, "newPassword" : new_password, "oldPassword" : password}
  

  try{
    var req = new XMLHttpRequest();
    req.open("PUT", "/change_password", true);
    req.setRequestHeader("Content-type", "application/json");
    req.onreadystatechange = function(){
      if (this.readyState == 4){
        var response = JSON.parse(req.responseText);
        var errorMessage = document.getElementById('reset_password_message');

        if (this.status == 200){
          errorMessage.style.color = "green";
          form.password.value = "";
          form.new_password.value = "";
          form.repeat_new_password.value = "";
        }else if (this.status == 400){
           errorMessage.style.color = "red";

      }

      errorMessage.innerHTML = response["message"];
    } 

    };
    req.send(JSON.stringify(request));
  }
  catch(e){
    window.alert(e);
  console.error(e);
  }
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
  var request = {"token" : token}
  try{
    var req = new XMLHttpRequest();
    req.open("POST", "/sign_out", true);
    req.setRequestHeader("Content-type", "application/json");
    req.onreadystatechange = function(){
      if (this.readyState == 4){
        if (this.status == 200){
          response = JSON.parse(req.responseText);
          console.log(response);
          localStorage.removeItem("token");
          displayView(document.getElementById('welcomeview'));
          current_tab = "home";
        }else if (this.status == 400){

          response = JSON.parse(req.responseText)
          var response = JSON.parse(req.responseText);
        } else if (this.status == 400){
          var response = JSON.parse(req.responseText)
        }
      }


    };
    req.send(JSON.stringify(request));
  }
  catch(e){
    window.alert(e);
  console.error(e);
  }

  return false
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
  //var mess = serverstub.signUp(request);


  try{

    var req = new XMLHttpRequest();
    req.open("PUT", "/signup", true);
    req.setRequestHeader("Content-type", "application/json");
    req.onreadystatechange = function(){
      if (this.readyState == 4){
        if (this.status == 200){
        

          response = JSON.parse(req.responseText);
          console.log(response);
        }else if (this.status == 400){

          response = JSON.parse(req.responseText)
        }
      }
      var errorMessage = document.getElementById('signupMessage');
      errorMessage.innerHTML = response["message"]  ;
      document.getElementById("personalInfo")

    };
    req.send(JSON.stringify(request));
  }
    catch(e){
      window.alert(e);
    console.error(e);
  }

  return false; //not to refresh page
  //var info = [];
  //info = JSON.stringify(form);
  //var obj = JSON.parse(info);
};

signin=function(form){
  var email = form.email.value.trim();
  var password = form.password.value.trim();
  var request = {"email" : email, "password" : password}
  //var mess = serverstub.signIn(email,password);
 // var mess = send_req(request, "PUT", "/signin")
  try{

    var req = new XMLHttpRequest();
    req.open("PUT", "/signin", true);
    req.setRequestHeader("Content-type", "application/json");
    req.onreadystatechange = function(){
      if (this.readyState == 4){
        if (this.status == 200){
          response = JSON.parse(req.responseText);
          var token = response["data"]["token"]
          localStorage.setItem("token", token);
          displayView(document.getElementById('profileView'));
          displayUserInfoOnLoad();
          displayAccountMessages();
          console.log(response);
        }else if (this.status == 400){
          response = JSON.parse(req.responseText)
          var errorMessage = document.getElementById('errorLabel');
          errorMessage.innerHTML = response["message"];
        }
      }
      
    };
    req.send(JSON.stringify(request));
  }
    catch(e){
      window.alert(e);
    console.error(e);
  }
  return false;
};

/*Called when browse button is pressed*/
browseUser = function(form){
  var token = localStorage.getItem("token");
  var request = {"token" : token, "email" : form.email.value.trim()}
  //  var user_data = serverstub.getUserDataByEmail(token, form.email.value);
  try{

    var req = new XMLHttpRequest();
    req.open("GET", "/get_user_data_by_email?token=" + token + "&email=" + form.email.value, true);
    req.setRequestHeader("Content-type", "application/json");
    req.onreadystatechange = function(){
      if (this.readyState == 4){
        if (this.status == 200){
          response = JSON.parse(req.responseText);
          displayAccountInfo(response["data"], true);
          displayAccountMessages(response["data"]["email"]);
        }else if (this.status == 400){
          document.getElementById("browse_user_message").innerHTML = user_data["message"];
          
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


displayAccountMessages = function(email = null){
  var token = localStorage.getItem("token");
  var posts;
  var wall;

  if(!email){
    //posts = serverstub.getUserMessagesByToken(token);
    try{
      var req = new XMLHttpRequest();
      req.open("GET", "/get_user_messages_by_token?token=" + token, true);
      req.setRequestHeader("Content-type", "application/json");
      req.onreadystatechange = function(){
        if (this.readyState == 4){
          wall = document.getElementById("myWall");

          if (this.status == 200){
            response = JSON.parse(req.responseText);
            wall.innerHTML = "";
            messages = response["data"]["messages"];
            for(var message in messages){
              wall.innerHTML += "<div> <span>" + messages[message][0]
                + ":</span>   <span class='align-r'>" + messages[message][1] + "</span> </div>";
            }

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
  }

  else
  {
    try{
      var req = new XMLHttpRequest()
      req.open("GET", "/get_user_messages_by_email?token=" + token + "&email=" +  email, true)
      req.setRequestHeader("Content-type", "application/json");
      req.onreadystatechange = function(){
        if (this.readyState == 4){
          wall = document.getElementById("browseWall")

          if (this.status == 200){
            response = JSON.parse(req.responseText);
            wall.innerHTML = "";
            messages = response["data"]["messages"];
            for(var message in messages){
              wall.innerHTML += "<div> <span>" + messages[message][0]
                + ":</span>   <span class='align-r'>" + messages[message][1] + "</span> </div>";
            }

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
    //posts = serverstub.getUserMessagesByEmail(token,email);
  }
}

displayAccountInfo = function(data, browse) {
  var token = localStorage.getItem("token");
  var user;
  var personalInfo;
  if(!browse){
    //user = serverstub.getUserDataByToken(token);
  
    personalInfo = document.getElementById("personalInfo");
  }
  else {
    //user = serverstub.getUserDataByEmail(token,email);
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
  var token = localStorage.getItem("token");

  try{

    var req = new XMLHttpRequest();
    req.open("GET", "/get_user_data_by_token?token=" + token, true);
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
  var token = localStorage.getItem("token");
  var recipient;
  if(email != null){
    //var user = serverstub.getUserDataByToken(token);
    recipient = email;
  }
  else {
    recipient = currentBrowsingEmail;

  }
  var message = form.contents.value;
  //serverstub.postMessage(token, message, recipient);

  var request = {"token" : token, "email" : recipient, "message" : message}
  //  var user_data = serverstub.getUserDataByEmail(token, form.email.value);
  
  try{
    var req = new XMLHttpRequest();
    req.open("POST", "/post_message", true);
    req.setRequestHeader("Content-type", "application/json");
    req.onreadystatechange = function(){

      if (this.readyState == 4){
        response = JSON.parse(req.responseText);
        if (this.status == 200){
          form.contents.value = "";

        }else if (this.status == 400){
          
        }
      }
      
    };
    req.send(JSON.stringify(request));
  }
    catch(e){
      window.alert(e);
    console.error(e);
  }
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
  content.style.display = "flex";
  current_tab = tab.id;
  tab.style.backgroundColor = "grey";

}

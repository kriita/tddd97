
displayView=function(view){
  //thecoderequiredtodisplayaview
  document.getElementById('content').innerHTML = view.innerHTML;

};

window.onload=function(){
  displayView(document.getElementById('welcomeview'));
};

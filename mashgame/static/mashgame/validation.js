$("#js_user_name").keyup(function(){
  var user_name = $(this).val();

  $.ajax({
    url: "{% url 'mashgame:validate_username' %}",
    data: {
      'user_name': user_name
    },
    dataType: 'json',
    success: function(res_data) {
      if(res_data.is_taken) {
        document.getElementById("js_user_name").style.borderColor = "red";
        $("#js_password").hide();
        $("#js_confirm_password").hide();
        $("#js_signup_button").hide();

      }
      else{
        document.getElementById("js_user_name").style.borderColor = "green";
        $("#js_password").show();
        $("#js_confirm_password").show();
        $("#js_signup_button").show();
      }
    }
  });
});

var check = function(){
  if(document.getElementById('js_password').value==
     document.getElementById('js_confirm_password').value){
    document.getElementById("js_confirm_password").style.borderColor = "green";
    $("#js_signup_button").show();
  }
  else {
    document.getElementById("js_confirm_password").style.borderColor = "red";
    $("#js_signup_button").hide();
  }
}

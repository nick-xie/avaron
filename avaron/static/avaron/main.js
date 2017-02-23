//LOBBY JS
//For getting CSRF token
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
          	// Does this cookie string begin with the name we want?
          	if (cookie.substring(0, name.length + 1) == (name + '=')) {
            	cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              	break;
            }
        }
    }
 return cookieValue;
}
var scrollFunction = function(idstring) {
  $('html, body').animate({
      scrollTop: $(idstring).offset().top
  }, 400);
};
function fillOutGame(game_num){
  $('#JoinError').empty();
  $('#game_num').val(game_num);
  scrollFunction('.cardb');
  $('#player_name').focus();
}
//List available games
function listGames(){
  var csrftoken2 = getCookie('csrftoken');
  $.ajax({
      type : 'POST',
      data : { csrfmiddlewaretoken : csrftoken2 },
      ifModified: true,
      url : "GetGames/",
    success : function(json) {
      if(status!="notmodified"){
        //console.log(json);
        //alert("change");
        var cGames= $('#openGames').text();
        //Must do a manual check for changes since AJAX xhr statuses can only check for not notmodified (which isn't working) 
        var glist = json.games;
        var clist ="";
        for (var i = 0; i<glist.length; i++) {
          clist = clist + "" + glist[i];
        }
        //alert(cGames);
        //alert(clist);
        if(clist!=cGames){
          $('#openGames').empty();
          for (var i = 0; i < glist.length; i++) {
            var num=glist[i];
            buildListElementItem = $('<li>' + glist[i] + '</li>');
            buildListElementItem.bind('click', function (){
              fillOutGame($(this).text());
            });
            $("#openGames").append(buildListElementItem);
          }
        }
      }
      setTimeout(listGames(), 2000);
    },
    error : function(xhr,errmsg,err) {
      console.log(xhr.status + ": " + xhr.responseText);
    },
  });
}
// window.onload = function() {
//   listGames();
// }
 //For doing AJAX post
$(document).ready(function(){
  listGames();
  //Create game is clicked
  $("#red").click(function(e){
    $("#join").prop('disabled', true);
    e.preventDefault();
    var csrftoken = getCookie('csrftoken');
    var pname = $('#player_nameC').val();
    //Ajax post
    $.ajax({
        type: 'POST',
        data: { csrfmiddlewaretoken : csrftoken, pname : pname},
        url : 'make_game/',
        success : function(json){
          //console.log(json);
          window.location.href='/avaron/'+json.gameNumber;
        },
        error : function(xhr,errmsg,err){
          console.log(xhr.status + ": " + xhr.responseText);
        }
    });
  }); 
  //-------------------------------------------------------------/
  //When join is clicked
  $("#join").click(function(e) {
	 $("#join").prop('disabled', true);
    //Prevent default submit. Must for Ajax post.Beginner's pit.
	 e.preventDefault();
    //Prepare csrf token
	 var csrftoken = getCookie('csrftoken');
    //Collect data from fields
	 var pname = $('#player_name').val();
	 var num = $('#game_num').val();
    //This is the Ajax post.Observe carefully. It is nothing but details of where_to_post,what_to_post
    //Send data  
 	  $.ajax({
       type : 'POST', // http method
       data : { csrfmiddlewaretoken : csrftoken, pname : pname, num : num},
       url : 'make_player/',// data sent with the post request
 // handle a successful response
 		success : function(json) {
 			//console.log(json); // another sanity check
 //On success show the data posted to server as a message
 			// alert(json.gameNumber);
 			if (json.gameNumber == 0) {
 			    window.location.href='/avaron/GameClosed';
 			} else if (json.gameNumber == -1) {
          $('#JoinError').text("Sorry, that game doesn't exist.");
      }else {
 			    window.location.href='/avaron/' + json.gameNumber;
 			}
 		},
    // handle a non-successful response
 		 error : function(xhr,errmsg,err) {
 		   console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
 		 }
 	  });
  });
});

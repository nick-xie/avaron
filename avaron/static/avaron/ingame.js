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

function listPlayers(){
	var csrftoken = getCookie('csrftoken');
	var num = $('#gamenum').text();
	$.ajax({
	    type : 'POST',
	    data : { csrfmiddlewaretoken : csrftoken, num : num},
	    ifModified: true,
	    url : "GetPlayers/",
		success : function(json) {
			if(status!="notmodified"){
				var plist = json.players;
				$('#playerList').empty();
				for (var i = 0; i < plist.length; i++) {
					$('#playerList').append('<p>' + plist[i] + '</p>');
				}
			}
			setTimeout(listPlayers(), 2000);
		},
		error : function(xhr,errmsg,err) {
			console.log(xhr.status + ": " + xhr.responseText);
		},
	});
}

window.onload = function() {
	listPlayers();
}

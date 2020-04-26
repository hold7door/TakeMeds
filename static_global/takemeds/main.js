function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function setCookie(cname, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    var expires = "expires="+ d.toUTCString();
    document.cookie = 'lat' + "=" + cname['latitude'] + ";" + expires + ";path=/";
	document.cookie = 'lon' + "=" + cname['longitude'] + ";" + expires + ";path=/";
}


var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function geoFindMe(){
		/*
		if(!navigator.geolocation)
		{
			output.innerHTML = "Your browser does not support geolocation";
			return ;
		}
		function success(position){			//Send coordinates to Server
        la = position.coords.lattitude;
        ln = position.coords.longitude;
		*/
        la = 26.84;
        ln = 80.87;
	
		var loc = { latitude : la , longitude : ln };
        $.ajax({
            type : 'POST',
            url : "loc/",
            data : loc,
            datatype : "json",
            success: function(){
			setCookie(loc,365);
            console.log("Successfully Sent");
            }
        }
        );
/*		
       }
        	
		function error(error){
			console.log('Error occured: Error code: ' + error.code);
		}
		navigator.geolocation.getCurrentPosition(success , error);
		*/
}


var djrs = djrs || {};  

djrs.remaining = Math.round(timeoutPeriod * (1 + count / 3));
djrs.count = count;
djrs.maxcount = 5;

djrs.countdown = function() {  
        if (djrs.count > djrs.maxcount) {
        	document.getElementById("timer").innerHTML="Refresh paused (count too high)";
	}
	else if (djrs.remaining < 0) {
		djrs.reload();
	}
	else {
        	document.getElementById("timer").innerHTML="Countdown: " + djrs.remaining + " secs";
		djrs.remaining = djrs.remaining - 1;
		setTimeout("djrs.countdown();",1000);
	}
};	

djrs.reload = function() {  
	console.log("Refresh Url: " + url);
        // TODO make this check for existing parameters and merge in new refresh parameter.
	window.location.replace(url + "?refresh=1");
};	

djrs.countdown()


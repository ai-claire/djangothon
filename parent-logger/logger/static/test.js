window.onload = function() {
	document.getElementById("para").innerHTML = "my plugin is awesome";
	dimensionX = document.getElementById("dimensionX").innerHTML;
	dimensionY = document.getElementById("dimensionY").innerHTML;
	url = document.getElementById("url").innerHTML;
	timestamp = document.getElementById("timestamp").innerHTML;
	insights = document.getElementById("insights").innerHTML;
	var a = new XMLHttpRequest();
	a.open("POST", '/logger/');
	a.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	a.send("dimensionX="+dimensionX+"&dimensionY="+dimensionY+"&url="+url+"&timestamp="+timestamp+"&insights="+insights);
	a.onreadystatechange = function() {
		if (a.readyState == 4 && a.status == 200) {
			console.log(a.responseText);
		}
	}
}
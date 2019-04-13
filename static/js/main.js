function onVoteButtonClick(movieID) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            alert('voted successfully')
        }
    };
    xhttp.open("GET", "/api/1/vote/" + movieID, true);
    xhttp.send();
}


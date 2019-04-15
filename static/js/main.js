function onVoteButtonClick(movieID) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var btn = document.getElementById("btn-fav-" + movieID);
            var res = JSON.parse(this.response);
            if (res['vote']) {
                btn.classList.remove('btn-fav-false', 'btn-primary');
                btn.classList.add('btn-fav-true', 'btn-outline-danger');
            } else {
                btn.classList.remove('btn-fav-true', 'btn-outline-danger');
                btn.classList.add('btn-fav-false', 'btn-primary');
            }
        }
    };
    xhttp.open("GET", "/api/1/vote/" + movieID, true);
    xhttp.send();
}


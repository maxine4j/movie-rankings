function onFavouriteButtonClick(movieID) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var btn = document.getElementById("btn-fav-" + movieID);
            var favCounter = document.getElementById("fav-counter-" + movieID);
            var res = JSON.parse(this.response);
            if (res['favourite']) {
                btn.classList.remove('btn-fav-false', 'btn-primary');
                btn.classList.add('btn-fav-true', 'btn-outline-danger');
                favCounter.innerHTML = parseInt(favCounter.innerHTML) + 1
            } else {
                btn.classList.remove('btn-fav-true', 'btn-outline-danger');
                btn.classList.add('btn-fav-false', 'btn-primary');
                favCounter.innerHTML = parseInt(favCounter.innerHTML) - 1
            }
        }
    };
    xhttp.open("GET", "/api/1/favourite/" + movieID, true);
    xhttp.send();
}


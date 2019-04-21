function onFavouriteButtonClick(movieID) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var res = JSON.parse(this.response);
            if (res.success) {
                var btn = document.getElementById("btn-fav-" + movieID);
                var favCounter = document.getElementById("fav-counter-" + movieID);
                if (res['favourite']) {
                    btn.classList.remove('btn-fav-false', 'btn-primary');
                    btn.classList.add('btn-fav-true', 'btn-outline-danger');
                    favCounter.innerHTML = parseInt(favCounter.innerHTML) + 1
                } else {
                    btn.classList.remove('btn-fav-true', 'btn-outline-danger');
                    btn.classList.add('btn-fav-false', 'btn-primary');
                    favCounter.innerHTML = parseInt(favCounter.innerHTML) - 1
                }
            } else {
                alert(res['message']);
            }
        }
    };
    xhttp.open("GET", "/api/1/favourite/" + movieID, true);
    xhttp.send();
}

function onPollChoiceClick(pollID, choiceID) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var res = JSON.parse(this.response);
            if (res.success) {
                var new_vote_counter = document.getElementById("vote-count-" + choiceID);
                var prev_choice_field = document.getElementById("poll-prev-choice-" + pollID);
                var prev_choice_id = prev_choice_field.value;
                var prev_vote_counter = document.getElementById("vote-count-" + prev_choice_id);
                new_vote_counter.innerHTML = parseInt(new_vote_counter.innerHTML) + 1;
                prev_vote_counter.innerHTML = parseInt(prev_vote_counter.innerHTML) - 1;
                prev_choice_field.value = choiceID;
            } else {
                alert(res['message']);
            }
        }
    };
    xhttp.open("GET", "/api/1/vote/"+pollID+"/"+choiceID, true);
    xhttp.send();
}
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
                    favCounter.innerHTML = parseInt(favCounter.innerHTML) + 1;
                } else {
                    btn.classList.remove('btn-fav-true', 'btn-outline-danger');
                    btn.classList.add('btn-fav-false', 'btn-primary');
                    favCounter.innerHTML = parseInt(favCounter.innerHTML) - 1;
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
                var prev_choice_field = document.getElementById("poll-prev-choice-" + pollID);
                var prev_prog_bar = document.getElementById("poll-prog-" + prev_choice_field.value);
                var prog_bar = document.getElementById("poll-prog-" + choiceID);
                var max_counter = document.getElementById("poll-max-count-" + choiceID);
                var total_counter = document.getElementById("poll-total-count-" + pollID);

                if (prev_prog_bar) {
                    prev_prog_bar.value -= 1;
                }
                prog_bar.value += 1;

                if (prev_choice_field.value == -1) {
                    total_counter.innerHTML = parseInt(total_counter.innerHTML) + 1;
                }

                prev_choice_field.value = choiceID;
            } else {
                alert(res['message']);
            }
        }
    };
    xhttp.open("GET", "/api/1/vote/"+pollID+"/"+choiceID, true);
    xhttp.send();
}

function initNewPollChoice(elementID) {
    $(elementID).select2({
        placeholder: "Enter a movie title",
        ajax: {
            url: '/api/1/search',
            type: "GET",
            dataType: "json",
            delay: 250,
            data: function (params) {
                var query = {
                    q: params.term
                }
                return query;
            },
            processResults: function (data) {
                return data
            }
        }
    });
}

function addNewPollChoice() {
    var pollChoiceCounter = document.getElementById("new-poll-choice-counter");
    pollChoiceCounter.value = parseInt(pollChoiceCounter.value) + 1;
    var newPollChoiceDiv = document.getElementById("new-poll-choices");
    /*
    <div class="form-group">
        <select class="form-control new-poll-choice-select" id="new-poll-choice-1" name="choice1" ></select>
    </div>
    */
    var div_formGroup = document.createElement("div");
    newPollChoiceDiv.append(div_formGroup);
    div_formGroup.setAttribute("class", "form-group");

    var select_newChoice = document.createElement("select");
    div_formGroup.append(select_newChoice);
    select_newChoice.setAttribute("class", "form-control new-poll-choice-select");
    select_newChoice.setAttribute("id", "new-poll-choice-" + pollChoiceCounter.value);
    select_newChoice.setAttribute("name", "choice" + pollChoiceCounter.value);

    initNewPollChoice("#new-poll-choice-" + pollChoiceCounter.value);
}

$(document).ready(function() {
    //addNewPollChoice();
    //addNewPollChoice();
    //addNewPollChoice();
});

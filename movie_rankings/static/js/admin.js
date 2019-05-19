function ajaxReloadAction(url) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var res = JSON.parse(this.response);
            if (res.success) {
                window.location.reload(true);
            } else {
                alert(res['message']);
            }
        }
    };
    xhttp.open("GET", url, true);
    xhttp.send();
}

function admin_grantAdmin() {
    ajaxReloadAction("/api/1/admin/grant/")
}

function admin_removePoll(pollID) {
    ajaxReloadAction("/api/1/poll/remove/"+pollID)
}

function admin_removeComment(commentID) {
    ajaxReloadAction("/api/1/comment/remove/"+commentID)
}
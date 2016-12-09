// Scroll down to see last messages at the botton of the page
function autoscroll() {
    $(document).ready(function () {
        $('#msg_list').animate({
            scrollTop: $('#msg_list').get(0).scrollHeight
        }, 1);
    });
}

// Live tracking for new messages
function getNewMessages() {
    $.get('/get_new_messages/', function (json) {
        $('#msg_list').html(json['messages']);
        autoscroll();
    })
}

// Getting cookies
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

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

// Send new message and save it to the Django model
$('#chat-form').on('submit', function (event) {
    event.preventDefault();

    $.ajax({
        url: '/save_new_msg/',
        type: 'POST',
        data: {'new_msg': $('#new_msg').val()},

        success: function (json) {
            autoscroll();
            //location.reload();
            $('#new_msg').val('');
            $('#msg_list').val('').html(json['messages']);
            autoscroll();
        }
    })
});

// Ajax setup
$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

var csrftoken = getCookie('csrftoken');
refreshTimer = setInterval(getNewMessages, 1500); // Timer for chat's live updating
autoscroll();

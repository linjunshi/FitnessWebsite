$('.form').find('input, textarea').on('keyup blur focus', function (e) {

  var $this = $(this),
      label = $this.prev('label');

	  if (e.type === 'keyup') {
		if ($this.val() === '') {
            label.removeClass('active highlight');
        } else {
            label.addClass('active highlight');
        }
    } else if (e.type === 'blur') {
    	if( $this.val() === '' ) {
    		label.removeClass('active highlight');
		} else {
		    label.removeClass('highlight');
		}
    } else if (e.type === 'focus') {

        if( $this.val() === '' ) {
    		label.removeClass('highlight');
		}else if( $this.val() !== '' ) {
		    label.addClass('highlight');
		}
    }

});

$('.tab a').on('click', function (e) {

  e.preventDefault();

  $(this).parent().addClass('active');
  $(this).parent().siblings().removeClass('active');

  target = $(this).attr('href');

  $('.tab-content > div').not(target).hide();

  $(target).fadeIn(600);

});

function check_login_info () {
    var data = $("#signin_form").serialize();
    $.ajax({
        type: "post",
        async: false,
        url: "signin/",
        data: data,
        timeout: 9999,
        success: function (ret_data) {
            console.log(ret_data);
            if (ret_data === "not verified") {
                $("#login_error").hide();
                $("#verified_error").show();
            } else if (ret_data !== "confirmed"){
                // console.log("HI!");
                $("#verified_error").hide();
                $("#login_error").show();
            } else {
                // redirect
                window.location="../";
            }
        }
    });
    // console.log(data);
    return false;
}

// forgot password, done by John
function send_password_link () {
    var data = $("#password_form").serialize();
    $.ajax({
        type: "post",
        async: false,
        url: "/register/forgotPassword/",
        data: data,
        timeout: 9999,
        success: function (ret_data) {
            console.log(ret_data);
            if (ret_data === "sent") {
                $("#password_link").show();
            }
        }
    });
    //console.log(data);
    return false;
}


function check_sign_up () {
    var data = $("#signup_form").serialize();
    $.ajax({
        type: "post",
        async: false,
        url: "signup/",
        data: data,
        timeout: 9999,
        success: function (ret_data) {
            console.log(ret_data);
            if (ret_data !== "ok"){
                // console.log("HI!");
                $("#signup_error").show();
            } else {
                // redirect
                alert("Please confirm registration in your email")
            }
        }
    });
    return false;
}

function like(e) {
    // alert("here");
    var data = e.target.getAttribute("id");
    // alert(data);
    $.ajax({
        type: "get",
        async: false,
        url: "/like/",
        data: {"video_id": data},
        timeout: 9999,
        success: function (ret_data) {
            if (ret_data === "not log in") {
                alert("Please log in first.");
                window.location="/register/";
            } else if (ret_data == "evaluated") {
                alert("You are evaluated");
            } else {
                e.target.innerHTML = ret_data;
            }
        }
    });
    return false;
}
$('.like').on('click',like);

function dislike(e) {
    var data = e.target.getAttribute("id");
    $.ajax({
        type: "get",
        async: false,
        url: "/dislike/",
        data: {"video_id": data},
        timeout: 9999,
        success: function (ret_data) {
            if (ret_data === "not log in") {
                alert("Please log in first.");
                window.location="/register/";
            } else if (ret_data == "evaluated") {
                alert("You are evaluated");
            } else {
                e.target.innerHTML = ret_data;
            }
        }
    });
    return false;
}
$('.dislike').on('click',dislike);
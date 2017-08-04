/**
 * Created by mugbya on 2017/5/9.
 */

// 获取 csrftoken
jQuery(document).ajaxSend(function (event, xhr, settings) {
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

    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});


$(function () {
    // 重置密码处理发送短信
    $(".reset-code-btn").on("click", function () {

        var url = '/audience/get_verification_code/';
        var phone = $('.reset-phone').val();

        $.ajax({
            url: url,
            method: 'get', // or another (GET), whatever you need
            dataType: 'json',
            data: {
                'phone': phone,
                'operate': 4
            },
            success: function (data) {
               alert('验证码发送成功');
            },
            error: function (data, error) {
                alert(data.responseText);
            }
        });
    })
});



$(function () {
    // 验证码登录 处理发送短信
    $(".login-code-btn").on("click", function () {

        var url = '/audience/get_verification_code/';
        var phone = $('.login-phone').val();

        $.ajax({
            url: url,
            method: 'get', // or another (GET), whatever you need
            dataType: 'json',
            data: {
                'phone': phone,
                'operate': 2
            },
            success: function (data) {
                alert('验证码发送成功');
            },
            error: function (data, error) {
                alert(data.responseText);
            }
        });
    })
});

$(function () {
    // 注册 处理发送短信
    $(".register-code-btn").on("click", function () {

        var url = '/audience/get_verification_code/';
        var phone = $('.register-phone').val();

        $.ajax({
            url: url,
            method: 'get', // or another (GET), whatever you need
            dataType: 'json',
            data: {
                'phone': phone,
                'operate': 1
            },
            success: function (data) {
                alert('验证码发送成功');
            },
            error: function (data, error) {
                alert(data.responseText);
            }
        });
    })
});




// -------------- 弹窗

$(function () {

    $(".navs-slider-btn").on("click", function () {
        getCode = 0;
        bar_s = $(this).attr("data-i");
        $(this).addClass("active").siblings().removeClass("active");
        $(this).css("color", "#48995b").siblings().css("color", "#666");
        if (bar_s == 1) {
            $(".navs-slider-bar").css("left", (0 + "px"));
            $(".loginIn").addClass("active");
            $(".loginUp").removeClass("active");
        } else {
            $(".navs-slider-bar").css("left", (72 + "px"));
            $(".loginIn").removeClass("active");
            $(".loginUp").addClass("active");
        }

    });

    $(".unable-login").on("click", function () {
        $(".md_backdrop").css("display", "block");
        $(".unable_Login").css("display", "block");
    });
    $(".unable_login_resetPw_btn").on("click", function () {
        getCode = 0;
        $(this).parent().css("display", "none");
        $(".unable_Login_resetPw").css("display", "block");
    });
    $(".unable_login_useVcode_btn").on("click", function () {
        getCode = 0;
        $(this).parent().css("display", "none");
        $(".unable_Login_useVcode").css("display", "block");
    });
    $(".unable_Login_close").on("click", function () {
        $(this).parent().parent().css("display", "none");
        $(".md_backdrop").css("display", "none");
    });
    $(".unable_Login_useVcode_back").on("click", function () {
        $(this).parent().parent().css("display", "none");
        $(".unable_Login").css("display", "block");
    });
    $(".unable_Login_useVcode_close").on("click", function () {
        $(this).parent().parent().css("display", "none");
        $(".md_backdrop").css("display", "none");
    });
    $(".unable_Login_resetPw_back").on("click", function () {
        $(this).parent().parent().css("display", "none");
        $(".unable_Login").css("display", "block");
    });
    $(".unable_Login_resetPw_close").on("click", function () {
        $(this).parent().parent().css("display", "none");
        $(".md_backdrop").css("display", "none");
    });
});
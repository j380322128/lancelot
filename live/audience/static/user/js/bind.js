/**
 * Created by mugbya on 2017/5/10.
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

    // 微信绑定 处理发送短信
    $(".weui-vcode-btn").on("click", function () {
        var phone = $('.phone').val();
        if (!(/^1[3|4|5|7|8]\d{9}$/.test(phone))) {
            $('.phone').val("手机号不正确");
            setTimeout(function () {
                $('.phone').val("");
            }, 1000);
            return false;
        }

        var url = '/user/get_verification_code/';

        $.ajax({
            url: url,
            method: 'get', // or another (GET), whatever you need
            dataType: 'json',
            data: {
                'phone': phone,
                'operate': 3
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
    // 处理 跳过绑定手机
    $(".jump_btn").on("click", function () {
        $('.jump_form').submit();
    })
});
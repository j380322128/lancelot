/**
 * Created by mugbya on 2017/5/2.
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
    var status = $("#status").val()
    if(status != 3){
        $("#live_start").hide();
        $("#live_over").show();

    }
    else{
        $("#live_start").show();
        $("#live_over").hide();
    }
    $('.charge_btn').click(function () {
            var id = $(this).attr('data'); // 触发行 id
            var audit = $(this).attr('data_value')
            
            $.ajax({
                url: '/course/course_audit/',
                method: 'POST', // or another (GET), whatever you need
                dataType: 'json',
                data: {
                    'id': id,
                    'audit': audit
                    //'csrfmiddlewaretoken': '{{ csrf_token }}',
                },
                success: function (data) {
                    console.log(data);
                    if (data['result'] == 'success') {
                        location.reload();
                    } else {
                        $('.body-message').html(data['message']);
                        $('#message').modal({show: true});
                    }
                }
            });
        })

    $('#live_start').click(function () {
        var id = $("#id").val(); // 触发行 id  
        $.ajax({
            url: '/courses/forbidden_or_resume_pulish_stream/',
            method: 'POST', // or another (GET), whatever you need
            dataType: 'json',
            data: {
                'id': id,
                'option': 'resume'
               
                //'csrfmiddlewaretoken': '{{ csrf_token }}',
            },
            success: function (data) {
                console.log(data);
                // video 的src 赋值
                document.getElementById("live_video").src=data['pull_rtmp']
                $('#push_url1').text(data['publish_url']);

                alert('开始成功')
                $("#live_start").hide();
                $("#live_over").show();
            },
            error: function(data){
                alert('error')            }
        });
    })
    $('#live_over').click(function () {
        var id = $("#id").val(); // 触发行 id  
        $.ajax({
            url: '/courses/forbidden_or_resume_pulish_stream/',
            method: 'POST', // or another (GET), whatever you need
            dataType: 'json',
            data: {
                'id': id,
                'option': 'forbidden'
               
                //'csrfmiddlewaretoken': '{{ csrf_token }}',
            },
            success: function (data) {
                console.log(data);
                alert('结束成功');
                $("#live_start").show();
                $("#live_over").hide();
              
            },
            error: function(data){
                alert('结束error');
            }
        });
    })
})
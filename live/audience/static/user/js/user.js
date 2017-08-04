/**
 * Created by mugbya on 16-10-9.
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
    // 用户状态联动
    $('.user-statue').click(function () {
        if ($(".userStatus").find("select").val() == "2") {
            $(".GagTime").css("display", "block");
        } else {
            $(".GagTime").css("display", "none");
        }
    });

    // 充值modal
    $(".charge_btn").click(function(){
        // 得到当前用户账户id
        var owner_id = $(this).attr("data");
        $.get("/users/account/"+owner_id+"/", function(data, status){
            if (data){
                $("input[name='account_id']").attr("value", data.account_id);
            }
        })
        // 得到所有资金流转账户
        var system_account = $("#YH_PRIMARY_ACCOUNT_TYPE").val();
        $("select[name='source']").empty();
        $.get("/account/accounts/?accountType__name="+ system_account, function(data, status){
             $.each(data.results, function(i, n){
                console.info(n);
                // 排除旧账户主账号
                if (n.name != "旧账户主账号"){ 
                    // 添加select option
                    var option = $("<option></option>");
                    option.attr("value", n.id);
                    option.html(n.description);
                    $("select[name='source']").append(option);
                }
             });
             $('#entering').modal({show: true});
        });
    });

    var isString = function(str){
        return (typeof str=='string')&&str.constructor==String;
    }

    // 确认充值
    $(".charge-success-btn").click(function(){
        var amount = $("input[name='charge_amount']").val();
        var source_id = $("select[name='source']").find("option:selected").val();
        var account_id = $("input[name='account_id']").val();

        $.post("/account/transfers/charge/", {amount:amount, source:source_id, description: "系统充值", merchant: "系统充值", account_id: account_id, channel:'system'}, function(data, status){
            if (isString(data)){
                alert(data);
            } else {
                alert("充值成功!");
            }
        });
    });
});


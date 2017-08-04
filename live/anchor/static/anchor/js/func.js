$('.charge_btn').click(function () {
        var id = $(this).attr('data'); // 触发行 id
        var audit = $(this).attr('data_value')
        
        $.ajax({
            url: '/anchor/anchor_audit/',
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

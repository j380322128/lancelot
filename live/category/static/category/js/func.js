$(function () {
    $(".js_add_cat").click(function(){
        $('.js_add_form').show();
        $('.js_cat_list').hide();
    })

    $(".btn_verify").on("click", function(){
        var category_id = $(this).attr("data-value");
        $(".verify").attr("data-value", category_id)
        $("#check").show()
    });

      $(".verify").on("click", function(){
        var category_id = $(this).attr("data-value");

        $.ajax({
            url: '/categories/'+ category_id+'/',
            type: 'DELETE',
            success: function(result) {
                alert('删除成功');
                window.location.href ='/category/category_list/';
            },
            error: function(s){
                alert(s.responseJSON.detail)
            }
        });
    });

    $(".btn-category").on("click", function () {

        var url = '/category/index/';
        var name = $('#category_name').val();
        var img_url = $('.dz-details > img').attr('alt');

        $.ajax({
            url: url,
            method: 'POST', // or another (GET), whatever you need
            dataType: 'json',
            data: {
                'name': name,
                'img_url': img_url,
                //'csrfmiddlewaretoken': '{{ csrf_token }}',
            },
            success: function (data) {
                console.log(data);
                if(data['result'] == 'success'){
                    location.reload();
                }
            }
        });
    })
});


$(".upload").on("click", function(){
        var upimage = $(this).prev();
        upimage.click();
    });
    // 封面图，限制大小
    $(".up").on("change", function(){
        var size_num = 10
        var file = $(this).prop('files')[0];
        //检查是否上传为图片
        if(!/image\/\w+/.test(file.type)){
            alert("这个需要图片！");
            return false;
        }

        var reader = new FileReader();//新建一个FileReader
        var d = $(this).next();
        d.empty();
        reader.readAsDataURL(file, "UTF-8");//读取文件
        reader.onload = function(evt){ //读取完文件之后会回来这里
            var fileString = evt.target.result;
            d.append($("<img width='120' height='120' src='"+fileString+"'/>"));
        }
    });

//
    $(".submit").on("click", function(){
        var f = $("form");
        var image = $("input[name='color_image']").prop("files")[0]
        if (image){
            //检查是否上传为图片
            if(!/image\/\w+/.test(image.type)){
                alert("封面必须为图片!");

                return false;
            }
            var size_num = 10

        } else {
                var no_change_image = $("#categ_image").val()
                if (no_change_image){return true;}
                alert("图片不能为空");
                return false;

        }
        var name = $("#category_name").val()
        if (name == '' || name == null){
            alert('分类名称不能为空');
            return false;
        }
    });
// $(function () {
//     Dropzone.autoDiscover = false;
//
//     var myDropzone = new Dropzone("#myDropzone", {
//         url: "/category/index/",
//         addRemoveLinks: false,
//         method: 'post',
//         filesizeBase: 1024,
//         sending: function (file, xhr, formData) {
//             formData.append("filesize", file.size);
//         },
//         success: function (file, response, e) {
//             location.reload();
//         //     var res = JSON.parse(response);
//         //     if (res.error) {
//         //         $(file.previewTemplate).children('.dz-error-mark').css('opacity', '1')
//         //     }
//         }
//     });
//
// });


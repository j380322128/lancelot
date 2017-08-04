

//申请大咖
//姓名
    function check_name(){
      var textVal = $("#name").val();
        newTextVal = textVal.replace(/[^\a-\z\A-\Z0-9\u4E00-\u9FA5\ \_]/g, '');
       return newTextVal;
    }
//手机
    function check_phone_num(){
      console.log("aaaaa");
        var phone_num = $("#tel").val();
        if(!(/^1[3|4|5|7|8]\d{9}$/.test(phone_num))){ $("#tel").attr("placeholder","请输入正确的手机号");$("#tel").css("border-color","red"); }else{
          $("#tel").css("border-color","#ccc");
        }
     }
//身份证/(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)/
    function check_identity_num(){
        var identity_num = $("#card_id").val();
        if(!/(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)/.test(identity_num)){ $("#card_id").attr("placeholder","请输入正确的身份证号码");$("#card_id").css("border-color","red"); }else{
          $("#card_id").css("border-color","#ccc");
        }
     }

     //添加直播
     function check_limit_num(g){
        var limit_num = $(g).val();
        limit_num = limit_num.replace(/[^\.0-9]/g, '');
        return limit_num;
     }
(function() {
    $("#tel").blur(function(){
      console.log("check_phone_num");
      check_phone_num();
    })
    $("#card_id").blur(function(){
      check_identity_num();
    })






    "use strict";

    // custom scrollbar

    $("html").niceScroll({styler:"fb",cursorcolor:"#65cea7", cursorwidth: '6', cursorborderradius: '0px', background: '#424f63', spacebarenabled:false, cursorborder: '0',  zindex: '1000'});

    $(".left-side").niceScroll({styler:"fb",cursorcolor:"#65cea7", cursorwidth: '3', cursorborderradius: '0px', background: '#424f63', spacebarenabled:false, cursorborder: '0'});


    $(".left-side").getNiceScroll();
    if ($('body').hasClass('left-side-collapsed')) {
        $(".left-side").getNiceScroll().hide();
    }


    

    // Toggle Left Menu
   jQuery('.menu-list > a').click(function() {
      
      var parent = jQuery(this).parent();
      var sub = parent.find('> ul');
      
      if(!jQuery('body').hasClass('left-side-collapsed')) {
         if(sub.is(':visible')) {
            sub.slideUp(200, function(){
               parent.removeClass('nav-active');
               jQuery('.main-content').css({height: ''});
               mainContentHeightAdjust();
            });
         } else {
            visibleSubMenuClose();
            parent.addClass('nav-active');
            sub.slideDown(200, function(){
                mainContentHeightAdjust();
            });
         }
      }
      return false;
   });

   function visibleSubMenuClose() {
      jQuery('.menu-list').each(function() {
         var t = jQuery(this);
         if(t.hasClass('nav-active')) {
            t.find('> ul').slideUp(200, function(){
               t.removeClass('nav-active');
            });
         }
      });
   }

   function mainContentHeightAdjust() {
      // Adjust main content height
      var docHeight = jQuery(document).height();
      if(docHeight > jQuery('.main-content').height())
         jQuery('.main-content').height(docHeight);
   }

   //  class add mouse hover
   jQuery('.custom-nav > li').hover(function(){
      jQuery(this).addClass('nav-hover');
   }, function(){
      jQuery(this).removeClass('nav-hover');
   });


   // Menu Toggle
   jQuery('.toggle-btn').click(function(){
       $(".left-side").getNiceScroll().hide();
       
       if ($('body').hasClass('left-side-collapsed')) {
           $(".left-side").getNiceScroll().hide();
       }
      var body = jQuery('body');
      var bodyposition = body.css('position');

      if(bodyposition != 'relative') {

         if(!body.hasClass('left-side-collapsed')) {
            body.addClass('left-side-collapsed');
            jQuery('.custom-nav ul').attr('style','');

            jQuery(this).addClass('menu-collapsed');

         } else {
            body.removeClass('left-side-collapsed chat-view');
            jQuery('.custom-nav li.active ul').css({display: 'block'});

            jQuery(this).removeClass('menu-collapsed');

         }
      } else {

         if(body.hasClass('left-side-show'))
            body.removeClass('left-side-show');
         else
            body.addClass('left-side-show');

         mainContentHeightAdjust();
      }

   });
   

   searchform_reposition();

   jQuery(window).resize(function(){

      if(jQuery('body').css('position') == 'relative') {

         jQuery('body').removeClass('left-side-collapsed');

      } else {

         jQuery('body').css({left: '', marginRight: ''});
      }

      searchform_reposition();

   });

   function searchform_reposition() {
      if(jQuery('.searchform').css('position') == 'relative') {
         jQuery('.searchform').insertBefore('.left-side-inner .logged-user');
      } else {
         jQuery('.searchform').insertBefore('.menu-right');
      }
   }

    // panel collapsible
    $('.panel .tools .fa').click(function () {
        var el = $(this).parents(".panel").children(".panel-body");
        if ($(this).hasClass("fa-chevron-down")) {
            $(this).removeClass("fa-chevron-down").addClass("fa-chevron-up");
            el.slideUp(200);
        } else {
            $(this).removeClass("fa-chevron-up").addClass("fa-chevron-down");
            el.slideDown(200); }
    });

    $('.todo-check label').click(function () {
        $(this).parents('li').children('.todo-title').toggleClass('line-through');
    });

    $(document).on('click', '.todo-remove', function () {
        $(this).closest("li").remove();
        return false;
    });


     $(function(){
    // setIdx_TailBottom();
        // window.onresize = function () {
        //     setIdx_TailBottom();}
  });
  function setIdx_TailBottom(){
        var w=$(window).height();
        var d=$(document).height();
        if(d<=w){$(".setIdx_TailBottom").css("position","absolute");$(".setIdx_TailBottom").css("bottom",0+"px");}else{$(".setIdx_TailBottom").css("position","relative")}
    }
   // $("#sortable-todo").sortable();


    // panel close
    $('.panel .tools .fa-times').click(function () {
        $(this).parents(".panel").parent().remove();
    });



    // tool tips

    $('.tooltips').tooltip();

    // popovers

    $('.popovers').popover();




 





})(jQuery);


$(document).ready(function(){
    function updataCategory(){
      $.ajax({
         url:'/categories/?enterprise_id='+$(this).val(),
         success:function(data){
            var catArr = data.results;
            var html = '<option selected="selected" value="">全部</option>'
            for(var i=0;i<catArr.length;i++){
              html+='<option value="'+catArr[i].id+'">'+catArr[i].name+'</option>'
            }
            $("#search_form [name='category_id']").html(html)
         }
       })
    }
    $("#search_form [name='enterprise_list']").change(updataCategory)
})
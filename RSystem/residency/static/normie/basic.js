/**
 * Created by drjeoffreycruzada on 02/07/2017.
 */
console.log("version "+1 );
function update(me){
    autosize($('textarea'));
}
function adjust_size(me){
   var regular = $(me).width();
   var minx = 1280;
   var curr_w = 0;
   if($(me).width() > minx) {
       curr_w = regular - minx;
   }
   else{
       curr_w = 0;
   }

    console.log(curr_w);
    $(".main-body").css({
       "padding": "0 0 0 "+curr_w+"px"
    });
   $(".custom-navtop ul").css({
       "padding": "0 0 0 "+curr_w+"px"
    });
    $(".inner-nav").css({
       "width": (1140+curr_w)+"px"
    });
};

function adjust_scroll(me){
    var myScroll = 0;
    var maxS = 90;
    if($(me).scrollTop() >maxS){
        myScroll = maxS;
        $('.custom-navtop li a').addClass('canHov');
    }
    else{
        myScroll = $(me).scrollTop();
        $('.canHov').removeClass('canHov');
    }

    var percyJackson = (myScroll/90)*0.2;
    $(".custom-navtop").css({
            'background-color': 'rgba(51,51,51,' + (0.8+percyJackson) + ')'
    });
    $(".custom-navtop li").css({
       "padding": (90-myScroll)+"px 0 0 0"
    });
    $(".custom-navtop ul").css({
        "height": (150-myScroll)+"px"
    });
    $(".custom-navtop #starter").css({
        "height": (150-myScroll)+"px",
        "width": (150-myScroll)+"px",
        "padding": "0 0 0 0"
    });
    $(".custom-navtop #starter img").css({
        "height": (150-myScroll)+"px",
        "width": (150-myScroll)+"px"
    });
};
$(window).resize(function(){

    //TIME FOR WIDTH
   adjust_size(this);
   //TIME FOR HEIGHT
});


$(window).scroll(function(){
    adjust_scroll(this);
});
$(document).on('submit','#progress_form', function(e){
    var prog_content = $("#PROG").val();
    var myId = $("#PROG").attr("myid");
    var projId = $("#PROG").attr("projid");
    $.ajax({
        type:'POST',
        url: '/ajax/add_progress/',
        data: {
            'projid': projId,
            'prog_content': prog_content,
            'myId': myId
        },
        datatype: 'json',
        success: function(data){
            console.log("nice");
        }
    });
    console.log("nice");
});

$(document).on('submit','#timeinput',function(e){
    // ORDERS //
    e.preventDefault();
    $("#eventNotifs").empty();
    var curr_time_len = 0;

    var inOrder = false;
    var isInRange = true;
    var collide = false;

    var day = $("#dayval").val();
    var sched1 = $("#mysched").val();
    var sched2 = $("#endsched").val()
    var timearray = $("#mysched").val().split(":");
    var timearray2 = $("#endsched").val().split(":");
    var mytime = parseFloat(timearray[0]) + parseFloat(timearray[1]/60);
    var mytime2 = parseFloat(timearray2[0]) + parseFloat(timearray2[1]/60);
    inOrder = sched1 < sched2;
    var timelen = mytime-mytime2;

    curr_time_len += timelen;
    isInRange = curr_time_len <=3;


    $(".doneSlot").each(function(){
       var thisday = $(this).attr("day");
       var thisstart = $(this).attr("ssched");
       var thisend = $(this).attr("esched");
       if(parseFloat(thisday) == parseFloat(day) && ((sched1 >= thisstart && sched1 <= thisend) || (sched2 >= thisstart && sched2 <= thisend))){
           collide = true;
       }
    });
    if(inOrder == true && isInRange == true && collide == false) {
        $.ajax({
            type: 'POST',
            url: '/ajax/add_sched/',
            data: {
                'day': day,
                'sched1': sched1,
                'sched2': sched2
            },
            datatype: 'json',
            success: function (data) {
                $("#eventNotifs").append("<p> Added sched! </p>");
                location.reload();
            }
        });

    }
    else{
       $("#eventNotifs").append("<p> Something went wrong! </p>");
    }
});

function adjustsched(){
    var timearray = $("#mysched").val().split(":");
    var mytime = parseFloat(timearray[0]) + parseFloat(timearray[1]/60);
    var timearray2 = $("#endsched").val().split(":");
    var mytime2 = parseFloat(timearray2[0]) + parseFloat(timearray2[1]/60);
    var timelen= mytime2-mytime;
    //1.75
    console.log("mytime2: "+mytime2+" mytime:"+mytime)
    console.log(mytime2-mytime);
    timelen = timelen - 0.25*Math.floor(timelen/1.75);
    var full_len = ((timelen)/1.5);
    $("#mySlot").css({
        "transform": "translateX("+(173*$("#dayval").val())+"px) translateY("+(55+70*((mytime-7.5)/1.75))+"px)",
        "height": (full_len * 70 )+"px"
    });
}
$(document).ready(function() {
    autosize($('textarea'));
    adjust_size($(window));
    adjust_scroll($(window));
    var num_pans = ($(".myPanel").length);
    if(num_pans/3 > 2){
        $(".body_container").css({
           "height": (700+(240*Math.ceil(num_pans/3-2)))+"px"
        });
    }
    else{
        $(".body_container").css({
           "height":"700px"
        });
    }
    $(".inner-nav").css({
        "width": 1280+($(window).width() - 1280-140)+"px"
    });
    $("body").css({
       "background-size": 1440+"px"+" "+900+"px"
    });
    $( ".myLoadBar" ).each(function() {
        var grade = $(this).attr("saikotama");
        if(grade > 90){
            $(this).children(".initLoad").css({
              "background-color": "mediumblue"
            });
        }
        else if(grade > 35){
            $(this).children(".initLoad").css({
              "background-color": "limegreen"
            });
        }
        else{
            $(this).children(".initLoad").css({
              "background-color": "firebrick"
            });
        }
      $(this).children(".initLoad").css({
          "width": ($(this).attr("saikotama"))+"%"
      });

    });
    $(".roletype").on('input', function(){
        var myId = $(this).attr("accid");
        var projid = $(this).attr("projid");
        var content = $(this).val();
        $.ajax({
            type:'POST',
            url: '/ajax/change_role/',
            data: {
                'projid': projid,
                'content': content,
                'myId': myId
            },
            datatype: 'json',
            success: function(data){
                console.log("nice");
            }
        });
    });
    $('.objectbox').change(function() {
        var myvalue = $(this).val();
        var done = $(this).is(':checked');
        $.ajax({
            type:'POST',
            url: '/ajax/checkObjective/',
            data: {
                'id': myvalue,
                'done': done,
            },
            datatype: 'json',
            success: function(data){
               location.reload();
            }
        });

    });
    $("#dayval").on('input',function(){
        adjustsched();
    });
    $("#mysched").on('input', function(){
        adjustsched();
    });
    $("#endsched").on('input', function(){
        adjustsched();
    });
});

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
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
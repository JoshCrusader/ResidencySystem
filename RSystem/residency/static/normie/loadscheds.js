/**
 * Created by drjeoffreycruzada on 06/07/2017.
 */

$(document).ready(function (){
    $(".doneSlot").each(function(){
        var timearray = $(this).attr("ssched").split(":");
        var mytime = parseFloat(timearray[0]) + parseFloat(timearray[1]/60);
        var timearray2 = $(this).attr("esched").split(":");
        var mytime2 = parseFloat(timearray2[0]) + parseFloat(timearray2[1]/60);
        var timelen= mytime2-mytime;

        timelen = timelen - 0.25*Math.floor(timelen/1.75);
        var full_len = ((timelen)/1.5);
        $(this).css({
            "transform": "translateX("+(173*parseFloat($(this).attr("day")))+"px) translateY("+(55+70*((mytime-7.5)/1.75))+"px)",
            "height": (full_len * 70 )+"px"
        });
    });
});
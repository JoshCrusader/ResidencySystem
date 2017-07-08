/**
 * Created by drjeoffreycruzada on 06/07/2017.
 */



function getScheds(me){
    var id = $(me).attr("name");
    $("#cubval").attr({"myteam":id});

    var xdCheats = ['None','Monday','Tuesday','Wednesday','Thursday','Friday'];
    curr_team_id = id;
    $.ajax({
        type:'POST',
        url: '/ajax/selected_cubes/',
        data: {
            'id': id,
        },
        datatype: 'json',
        success: function(data){
            $("#cubval").css({"display":"block"});
            $(".panel-primary").each(function(){
                    $(this).addClass('panel-default').removeClass('panel-primary');

               });
            $(me).addClass('panel-primary').removeClass('panel-default');
            $("#schedlist").empty();
            $("#TeamPangalan").empty();
            $("#TeamPangalan").append(data.teamname);
            $("#cuname").empty();
            $("#cuname").append(data.cuname);
            for(i = 0; i < data.yeslist.length; i++){
                $("#schedlist").append('<tr>'+
                    '<td>'+xdCheats[(data.yeslist[i][0])]+'</td>'+
                    '<td>'+(data.yeslist[i][1])+'</td>'+
                    '<td>'+(data.yeslist[i][2])+'</td>'+

                    '</tr>');
            }
            for(i=0; i < data.cubes.length;i++){
                for(x = 0; x<data.cubes[i].length;x++){
                    var str = "."+(i+1)+"day"+(x+1);
                    $(str).empty();
                    $(str).append(data.cubes[i][x]);

                    if(parseFloat(data.cubes[i][x]) > 0){
                        if(data.cuname == "LEXELL"){
                            $(str).css({
                               "background-color" :"green"
                            });
                        }
                        else if(data.cuname == "BORRELY"){
                            $(str).css({
                               "background-color" :"blue"
                            });
                        }
                        else if(data.cuname == "MCNAUGHT"){
                            $(str).css({
                               "background-color" :"yellow"
                            });
                        }
                        else if(data.cuname == "ENCKE"){
                            $(str).css({
                               "background-color" :"red"
                            });
                        }
                    }
                    else{

                        $(str).css({
                           "background-color" :"white"
                        })
                    }


                }
            }
        }
    });
}
$(document).ready(function(){
    $("#cubval").on('input',function(){
       var id = $(this).attr("myteam");
       var cub = $(this).val();
       $.ajax({
           type: 'POST',
           url: '/ajax/change_cub/',
           data: {
               'id': id,
               'cub': cub
           },
           datatype: 'json',
           success: function (data) {
               location.reload();
           }
       });
    });
});

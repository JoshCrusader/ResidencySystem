/**
 * Created by drjeoffreycruzada on 06/07/2017.
 */
function updatesched(){
    var cub = $("#cubval").val();
    $.ajax({
        type:'POST',
        url: '/ajax/user_cub/',
        data: {
            'cubicle': cub,
        },
        datatype: 'json',
        success: function(data){
            $("#cuname").empty();
            $("#cuname").append(data.cuname);
            for(i=0; i < data.cubes.length;i++){
                for(x = 0; x<data.cubes[i].length;x++){
                    var str = "."+(i+1)+"slot"+(x+1);
                    $(str).empty();

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
    updatesched();
    $("#cubval").on('input',function(){
       updatesched();
    });
});
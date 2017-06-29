/**
 * Created by drjeoffreycruzada on 24/06/2017.
 */

// Init
function update(me){
    autosize($('textarea'));
}
function clicky(me, row){
    var uname = $(me).val();
    $.ajax({
        type:'POST',
        url: '/ajax/accept_user/',
        data: {
            'user': uname,
        },
        datatype: 'json',
        success: function(data){
           $(row).remove();
        }
    });
}
function reject(me, row){
    var uname = $(me).val();
    $.ajax({
        type:'POST',
        url: '/ajax/reject_user/',
        data: {
            'user': uname,
        },
        datatype: 'json',
        success: function(data){
           $(row).remove();
        }
    });
}

var curr_team_id = 1;
function getAccounts(me){
    var id = $(me).attr("name");
    curr_team_id = id;
    $.ajax({
        type:'POST',
        url: '/ajax/selected_team/',
        data: {
            'id': id,
        },
        datatype: 'json',
        success: function(data){
            $(".panel-primary").each(function(){
                    $(this).addClass('panel-default').removeClass('panel-primary');

               });
            $(me).addClass('panel-primary').removeClass('panel-default');
            $("#notList").empty();
            $("#Members").empty();
            $("#TeamPangalan").empty();
            $("#TeamPangalan").append(data.teamname);
            for(i = 0; i < data.notlist.length; i++){
                $("#notList").append('<tr>'+
                    '<td>'+(data.notlist[i][0])+'</td>'+
                '<td><button type="button" class="btn btn-success" style = "border-radius:30px;" value = "'+(data.notlist[i][1])+'" onclick = "joinTeam(this)"><span class = "glyphicon glyphicon-circle-arrow-up"></span></button></td>'+
              '</tr>');
            }
            for(i = 0; i < data.yeslist.length; i++){
                $("#Members").append('<tr>'+
                    '<td>'+(data.yeslist[i][0])+'</td>'+
                '<td><button type="button" class="btn btn-danger" style = "border-radius:30px;" value = "'+(data.yeslist[i][1])+'" onclick = "removeFromTeam(this)"><span class = "glyphicon glyphicon-circle-arrow-down"></span></button></td>'+
              '</tr>');
            }
        }
    });
}
function joinTeam(me){
    var id = $(me).val();
    $.ajax({
        type:'POST',
        url: '/ajax/join_request/',
        data: {
            'id': id,
            'teamid': curr_team_id,
        },
        datatype: 'json',
        success: function(data){
                $(me).parent().parent().remove();
                $("#Members").append('<tr>'+
                    '<td>'+(data.name)+'</td>'+
                '<td><button type="button" class="btn btn-danger" style = "border-radius:30px;" value = "'+(data.id)+'" onclick = "removeFromTeam(this)"><span class = "glyphicon glyphicon-circle-arrow-down"></span></button></td>'+
              '</tr>');
        }
    });
}

function removeFromTeam(me){
    var id = $(me).val();
    $.ajax({
        type:'POST',
        url: '/ajax/remove_request/',
        data: {
            'id': id,
            'teamid': curr_team_id,
        },
        datatype: 'json',
        success: function(data){
                $(me).parent().parent().remove();
                $("#notList").append('<tr>'+
                    '<td>'+(data.name)+'</td>'+
                '<td><button type="button" class="btn btn-success" style = "border-radius:30px;" value = "'+(data.id)+'" onclick = "joinTeam(this)"><span class = "glyphicon glyphicon-circle-arrow-up"></span></button></td>'+
              '</tr>');
        }
    });
}
var Curr_id = null;
var Curr_name = null;
function AssignProj(me){
    var id = $(me).attr("myId");
    var name = $(me).attr("name");
    Curr_name = name;
    Curr_id = id;
    $(".panel-primary").each(function(){
                    $(this).addClass('panel-default').removeClass('panel-primary');

               });
    $(me).addClass('panel-primary').removeClass('panel-default');
}

var Team_id = null;
function giveProj(me){
    var id = $(me).attr("myId");
    var name = $(me).attr("name");
    Team_id = id;
    if(Curr_id != null){
        $("#projLabel").empty().append(Curr_name);
        $("#teamLabel").empty().append(name);
        $('#myModal').modal('show');
    }
}

function TransferProtocol(){
    $.ajax({
        type:'POST',
        url: '/ajax/Assign_proj/',
        data: {
            'projid': Curr_id,
            'teamid': Team_id,
        },
        datatype: 'json',
        success: function(data){
            console.log(data.id);
            $(".projpanel").each(function(){
                    if($(this).attr("myId") == data.id){
                        $(this).remove();
                    }
               });
        }
    });
}
$(document).ready(function() {
    autosize($('textarea'));
    $("#CreateProj").click(function () {
        $("#objs").empty();
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
});
$(document).on('submit','#project_form', function(e){
   e.preventDefault();
   var objectiveNames = [];
   var objectivePoints = [];

   $(".pname-input").each(function(){
        objectiveNames.push($(this).val());

   });
   $(".points-input").each(function(){
        objectivePoints.push($(this).val());

   });
   $.ajax({
        type:'POST',
        url: '/ajax/create_project/',
        data: {
            'pname': $("#pname").val(),
            'objectiveNames[]': objectiveNames,
            'objectivePoints[]': objectivePoints,
        },
        datatype: 'json',
        success: function(data){
            $("#project_body").prepend('' +
                    '<a id = "project_panel" href = "/project/'+data.id+'">'+
                    '<div class = "col-md-4">'+
            '<div class="panel panel-default">'+
              '<div class="panel-heading">'+data.name+'</div>'+
              '<div class="panel-body">No Team Assigned</div>'+
            '</div>'+
            '</div>'+
            '</a>');
            $("#myModal").modal('hide');
        }
    });

});

$(document).on('submit','#team_form', function(e){
   e.preventDefault();

   $.ajax({
        type:'POST',
        url: '/ajax/create_team/',
        data: {
            'tname': $("#tname").val(),
        },
        datatype: 'json',
        success: function(data){
            $("#tbody").prepend('<a href = "#" style = "text-decoration: None;color:black;"><div class="panel panel-default" onclick = "getAccounts(this);" name = "'+data.id+'">'+
                '<div class="panel-body">' + data.name+
                '</div>'+
            '</div></a>');
            $("#myModal").modal('hide');
        }
    });

});

function AddObjective(){

    $("#objs").append("<input type=\"text\" class=\"form-control col-md-4 pull-left pname-input\" style = \"width:70%;\" id=\"usr\" placeholder = \"Objective name\">\n<input type=\"Number\" class=\"form-control col-md-8 pull-right points-input\" style = \"width:25%;\" id=\"usr\" placeholder = \"Enter points\"><br><hr>\n");
}

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
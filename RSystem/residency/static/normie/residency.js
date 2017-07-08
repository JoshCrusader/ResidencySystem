/**
 * Created by drjeoffreycruzada on 07/07/2017.
 */
function testlogout(){
    $.ajax({
        type: 'POST',
        url: '/ajax/request_logout/',
        data: {},
        datatype: 'json',
        success: function (data) {

        }
    });
}
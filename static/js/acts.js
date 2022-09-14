$(document).ready(function(){
 $("#cancel").click(function(){
        location.reload();
});

$("#generate").click(function(){
$('#save').removeAttr('disabled');
$('#cancel').removeAttr('disabled');
var data = new FormData($('#createinspection').get(0));
    $.ajax({
    type: "POST",
    url: url_acts_gen,
    data: data,
    cache: false,
    contentType: false,
    processData: false,
    success: function(response){
         $('#myframe').attr('src','data:application/pdf;base64,'+response);
         },
    failure: function(){
          $(this).addClass("error");
          }
    });
});
});

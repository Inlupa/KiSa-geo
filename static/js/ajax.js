
$("#"+ id_ajax_1).blur(function (){
      var form = $(this).closest("form");
      $.ajax({
        url: url_ajax,
        data: form.serialize(),
        dataType: 'json',
        success: function (data) {
            if (data) {
                    for (let key in data) {
                        let element = document.getElementById('id_' + key);
                        switch (element.type) {
                            case 'checkbox':
                                element.checked = data[key];
                                break;
                            default:
                                element.value = data[key];
                                break;
                             }
                      }
            }
        }
      });
    });
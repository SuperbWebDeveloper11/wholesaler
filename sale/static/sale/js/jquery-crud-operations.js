(function ($) {

    // fetch a template and put it in the bootstrap modal
    $("#list-temp-place").on("click", "#fetch-detail-temp", {'temp': 'detail_temp'}, fetchTemp);
    $("#list-temp-place").on("click", "#fetch-create-temp", {'temp': 'create_temp'}, fetchTemp);
    $("#list-temp-place").on("click", "#fetch-update-temp", {'temp': 'update_temp'}, fetchTemp);
    $("#list-temp-place").on("click", "#fetch-delete-temp", {'temp': 'delete_temp'}, fetchTemp);

    // submit the template and return back template list
    $(".modal").on("submit", "#submit-create-temp", submitTemp);
    $(".modal").on("submit", "#submit-update-temp", submitTemp);
    $(".modal").on("submit", "#submit-delete-temp", submitTemp);
    

    /////////////////////// handler functions /////////////////////// 
    
    // fetch a template and put it in the bootstrap modal
    function fetchTemp(e) {
        var btn = $(this);
        $.ajax({
            url: btn.attr('data-url'),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $(".modal").modal("show"); 
            },
            success: function (data) {
                // put the (create, update or delete) templates in our bootstrap modal
                var temp_name = e.data.temp;
                $(".modal-content").html(data[temp_name]); 
            },
            error: function() {
                alert('Error : could not fetch template')
            }
        });
    }
    
    // submit the template and return back template list
    function submitTemp(e) {
        e.preventDefault();
        var form = $(this);
        /*
        let fd = new FormData(form[0]);
        fd.append('key1', 'value1');
        fd.append('key2', 'value2');
        for (var value of fd.values()) {
            console.log(value);
        }
        */
        var fd = new FormData(form[0]);
        // for (var e of fd.entries()) {
            // console.log(e[0] + ': ' + e[1]);
        // }
        $.ajax({
            url: form.attr('action'),
            // data: form.serialize(),
            data: fd, // <-- add this when using FromData
            processData: false, // <-- add this when using FromData
            contentType: false, // <-- add this when using FromData
            type: form.attr("method"),
            dataType: 'json',
            success: function(data) {
                if (data.form_is_valid) { 
                    $(".modal").modal("hide"); 
                    $("#list-temp-place").html(data.list_temp); 
                }
                else { 
                    alert('Error : please fill the form correctly')
                }
            },
            error: function() {
                alert('Error : could not submit template')
            }
        });
        return false;
    }

})(jQuery);

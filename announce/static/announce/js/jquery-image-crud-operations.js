(function ($) {

    // fetching templates for edition or deletion
    $("#image-list-wrapper").on("click", "#fetch-temp", fetchTemp);

    // submiting template for edition or deletion 
    $(".modal").on("submit", "#submit-temp", submitTemp);

    // submiting template for creation
    $(".create-image").on("submit", "#submit-temp", submitTemp);

    /////////////////////// handler functions /////////////////////// 

    // fetch list template 
    function fetchList() { 
        var btn = $(this);
        $.ajax({
            url: btn.attr('data-url'), 
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                console.log('fetching list template from server ... ')
            },
            success: function (data) {
                $("#image-list-wrapper").html(data.temp); 
            }
        });
    }

    // fetch edit and delete template 
    function fetchTemp() {
        var btn = $(this);
        $.ajax({
            url: btn.attr('data-url'),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $(".modal").modal("show"); 
            },
            success: function (data) {
                $(".modal-content").html(data.temp); 
            }
        });
    }

    // submit create, edit and delete templates and get back list template
    function submitTemp() {
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            // data: form.serialize(),
            data: new FormData(form),
            type: form.attr("method"),
            dataType: 'json',
            success: function(data) {
                if (data.form_is_valid) { 
                    // hide modal after editing and deleting
                    $(".modal").modal("hide"); 
                    // set list template in our page
                    $("#image-list-wrapper").html(data.temp); 
                }
                else { 
                    // set template in our page with errors
                    $(".modal-content").html(data.temp); 
                }
            }
        });
        return false;
    }

})(jQuery);

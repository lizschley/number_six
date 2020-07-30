$(document).ready(function() {
    $('.para_by_subtitle').click(function(e) {
        var subtitle = this.getAttribute('data-subtitle');
        // preventing from page reload and default actions
        e.preventDefault();
        // make GET ajax call
        $.ajax({
            type: 'GET',
            //url: "{% url 'para_by_subtitle' %}",
            url: 'para_by_subtitle',
            data: {'subtitle' : subtitle},
            success: function (response) {
                 var paragraph = response['paragraph'];
                 var subtitle  = paragraph['subtitle']
                 var subtitle_note = paragraph['subtitle_note']
                 var text = paragraph['text']
                 var para = subtitle_note + ' ' + text
                 if (paragraph['references']) {
                    para = para + '<h5>References</h5>' + paragraph['references']
                 }
                 $('#subtitle_modal_title').html(subtitle);
                 $('#subtitle_modal_para').html(para);
                 // Display Modal
                 $('#standalone_para_modal').modal('show');
            },
            error: function (response) {
                // alert the error if any error occured
                alert(response["responseJSON"]["error"]);
            }
        })
    })
})

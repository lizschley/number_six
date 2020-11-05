$(document).ready(function() {
    $('.para_by_subtitle').click(function(e) {
        // preventing from page reload and default actions
        e.preventDefault();
        var subtitle = this.getAttribute('data-subtitle');
        $.ajax({
            type: 'GET',
            url: 'para_by_subtitle',
            data: {'subtitle' : subtitle},
            success: function (response) {
                 var paragraph = response['paragraph'];
                 var subtitle  = paragraph['subtitle']
                 var subtitle_note = paragraph['subtitle_note']
                 var para = paragraph['text']
                 if (subtitle_note) {
                    para = subtitle_note + ' ' + para
                 }
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

    $('.category_group').click(function(e) {
        // preventing from page reload and default actions
        e.preventDefault();
        var div_id = '#' + this.getAttribute('data-identifier');
        if (!$(div_id).hasClass('category_group_div')) {
            $(div_id).addClass('category_group_div');
        }
        show_one_id_within_class(div_id, '.category_group_div')
    })
})

function show_one_id_within_class(id_to_show, class_to_hide) {
    $(class_to_hide).addClass('d-none');
    $(id_to_show).removeClass('d-none');
  }

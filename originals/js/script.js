$(document).ready(function() {
    $('.one_para_modal').click(function(e) {
        // preventing from page reload and default actions
        e.preventDefault();
        var slug = this.getAttribute('data-slug');
        $.ajax({
            type: 'GET',
            url: '/projects/study/paragraphs/modal',
            data: {'slug' : slug},
            success: function (response) {
                 var paragraph = response['paragraph'];
                 var subtitle  = paragraph['subtitle'];
                 var subtitle_note = paragraph['subtitle_note'];
                 var image_link = image_html(paragraph['image_path'])
                 var para = image_link + paragraph['text'];
                 if (subtitle_note) {
                    para = subtitle_note + ' ' + para
                 }
                 if (paragraph['references']) {
                    para = para + '<h5>References</h5>' + paragraph['references'];
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

    $('#id_ordered').change(function(){
        id = $( "#id_ordered option:selected" ).text();
        $('#id_flashcard').val("0");
        $('#id_standalone').val("0");
        $('#id_search').val('> 2 characters');
    });

    $('#id_standalone').change(function(){
        id = $( "#id_standalone option:selected" ).text();
        $('#id_flashcard').val("0");
        $('#id_ordered').val("0");
        $('#id_search').val('> 2 characters');
    });

    $('#id_flashcard').change(function(){
        id = $( "#id_flashcard option:selected" ).text();
        $('#id_ordered').val("0");
        $('#id_standalone').val("0");
        $('#id_search').val('> 2 characters');
    });

    $('#id_search').change(function(){
        $('#id_ordered').val("0");
        $('#id_standalone').val("0");
        $('#id_flashcard').val("0");
    });

    $().alert()
    $().alert('close')

    $('.collapse').on('shown.bs.collapse', function (e) {
        var $header = $(this).closest('.card');
        $('html,body').animate({
            scrollTop: $header.offset().top
        }, 500);
    });
})

function image_html(image_path) {
    if (typeof image_path === 'undefined' || image_path.trim().length === 0) {
        return ''
    }
    var link_text = '<div class="text-center">'
    link_text += '<img class="img-fluid" '
    link_text += 'src="' + image_path + '" '
    link_text += 'alt="' + alt_from_path(image_path) + '">'
    link_text += '</div>'
    console.log('link_text==' + link_text);
    return link_text
}

function alt_from_path(image_path) {
    temp = image_path.split('.')
    temp = temp[0].split('/')
    return temp[temp.length - 1]
}

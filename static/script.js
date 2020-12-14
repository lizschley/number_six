$(document).ready(function() {
    $('.para_by_subtitle').click(function(e) {
        // preventing from page reload and default actions
        e.preventDefault();
        var subtitle = this.getAttribute('data-subtitle');
        $.ajax({
            type: 'GET',
            url: '/projects/study/paragraphs/para_by_subtitle',
            data: {'subtitle' : subtitle},
            success: function (response) {
                 var paragraph = response['paragraph'];
                 var subtitle  = paragraph['subtitle'];
                 var subtitle_note = paragraph['subtitle_note'];
                 var para = image_html(paragraph['image_path']) + paragraph['text'];
                 if (subtitle_note) {
                    para = subtitle_note + ' ' + image_html + para
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
    });

    $('#id_standalone').change(function(){
        id = $( "#id_standalone option:selected" ).text();
        $('#id_flashcard').val("0");
        $('#id_ordered').val("0");
    });

    $('#id_flashcard').change(function(){
        id = $( "#id_flashcard option:selected" ).text();
        $('#id_ordered').val("0");
        $('#id_standalone').val("0");
    });

    $().alert()
    $().alert('close')
})

function image_html(image_path) {
    console.log('in image link ' + image_path);
    if (!image_path) return '';
    var image_html = '<div class="text-center">'
    image_html += '<img class="img-fluid" '
    image_html += 'src="/static/' + image_path + '" '
    image_html += 'alt="' + alt_from_path(image_path) + '">'
    image_html += '</div>'
    return image_html
}

function alt_from_path(image_path) {
    temp = image_path.split('.')
    temp = temp[0].split('/')
    return temp[temp.length - 1]
}

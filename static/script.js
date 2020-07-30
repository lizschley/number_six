$(document).ready(function() {
    $('.para_by_subtitle').click(function() {
        // var attribute = this.getAttribute('data-subtitle');
        var data = 'subtitle'
        var subtitle = get_subtitle(data)
        $('#subtitle_modal_title').html(subtitle);
        var new_data = '<p> I am a paragraph</p> <h5>References</h5><p>I am a reference</p>'
        var para = get_para(new_data)
        $('#subtitle_modal_para').html(para);

        // Display Modal
        $('#standalone_para_modal').modal('show');
    })
})

function get_subtitle(data) {
    return data;
}

function get_para(data) {
    return data;
}


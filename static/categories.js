$(document).ready(function() {
    $('.category_group').click(function(e) {
        // preventing from page reload and default actions
        e.preventDefault();
        var div_id = '#' + this.getAttribute('data-identifier');
        var menu_id = '#' + this.getAttribute('id')
        if (!$(div_id).hasClass('category_group_div')) {
            $(div_id).addClass('category_group_div');
        }
        show_one_id_within_class(div_id, '.category_group_div');
        change_selected_menu_color(menu_id, '.category_group')
    })
})

function show_one_id_within_class(id_to_show, class_to_hide) {
    $(class_to_hide).addClass('d-none');
    $(id_to_show).removeClass('d-none');
}

function change_selected_menu_color(menu_id, class_to_unselect) {
    $(class_to_unselect).removeClass('selected');
    $(menu_id).addClass('selected');
}

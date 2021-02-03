$(document).ready(function() {
    begin_flashcards();

    $('#next_question_menu').click(function(e) {
        // preventing from page reload and default actions
        e.preventDefault();
        next_question();
    })

    $('#remove_question_menu').click(function(e) {
        // preventing from page reload and default actions
        e.preventDefault();
        remove_question()
    })

    $('#shuffle_questions_menu').click(function(e) {
        // preventing from page reload and default actions
        e.preventDefault();
        shuffle_questions();
    })
})
function begin_flashcards() {
    hide_all_flashcard_group_div_class();
    var group_array = array_from_flashcard_divs()
    if (group_array.length > 1) {
        var new_array = group_array.sort(() => Math.random() - 0.5);
        $('#hidden_flashcard_divs').val(new_array.join('~'));
    }
    shift_and_show_question();
}

function array_from_flashcard_divs() {
    var group_divs = current_divs()
    if (!group_divs) {
        return []
    }
    return group_divs.split('~');
}

function current_divs(){
    var temp = $('#hidden_flashcard_divs').val();
    if (typeof temp === 'undefined') {
        return ''
    }
    return temp.toString().trim()
}

function hide_all_flashcard_group_div_class(){
    $('.flashcard_group_div').addClass('d-none')
}

function remove_question(){
    var group_divs = current_divs()
    var currently_showing = current_group()
    if (!group_divs && !currently_showing) {
        display_not_enough_questions('to remove one');
    }
    shift_and_show_question();
}

function current_group(){
    var temp = $('#currently_showing').val();
    return temp.toString().trim()
}

function shift_and_show_question() {
    hide_all_flashcard_group_div_class()
    var group_array = array_from_flashcard_divs();
    var currently_showing = ''
    if (group_array.length > 0) {
        currently_showing = group_array.shift().toString().trim();
        show_one_id_within_class('#' + currently_showing, '.flashcard_group_div');
    }
    assign_hidden_variables(currently_showing, group_array);
}

function display_not_enough_questions(operation){
    var message = 'Not enough questions ' + operation + '. Refresh page or click study on top menu to continue. '
    alert_message(message);
}

function assign_hidden_variables(currently_showing, group_array) {
    var curr_divs = ''
    if (group_array.length > 0) {
        curr_divs = group_array.join('~')
    }
    $('#currently_showing').val(currently_showing);
    $('#hidden_flashcard_divs').val(curr_divs);
}

function shuffle_questions() {
    append_currently_showing_to_groups();
    var group_array = array_from_flashcard_divs();
    if (group_array.length < 2) {
        display_not_enough_questions('to shuffle');
        return;
    }
    var new_array = group_array.sort(() => Math.random() - 0.5);
    $('#hidden_flashcard_divs').val(new_array.join('~'));
    shift_and_show_question();
}

function next_question() {
    var group_divs = current_divs()
    if (!group_divs){
        display_not_enough_questions('to show next');
        return;
    }
    append_currently_showing_to_groups();
    shift_and_show_question();
}

function append_currently_showing_to_groups() {
    var currently_showing = current_group();
    if (currently_showing) {
        var group_divs = current_divs()
        if (group_divs) {
            $('#hidden_flashcard_divs').val(group_divs + '~' + currently_showing);
        } else {
            $('#hidden_flashcard_divs').val(currently_showing);
        }
        $('#currently_showing').val('');
    }
}

function alert_message(message) {
    alert_body = '<div class="alert alert-primary alert-dismissible fade show">'
    alert_body += '<strong>Note: </strong>' + message
    alert_body += '<button type="button" class="close" data-dismiss="alert">×</button>'
    alert_body += '</div>'
    $('#flashcard_message').html(alert_body)
}

$(document).ready(function() {
    group_divs = $('#hidden_flashcard_divs').val()
    if (group_divs.length > 3) {
        begin_flashcards(group_divs);
    }

    $('#next_question_menu').click(function(e) {
        // preventing from page reload and default actions
        e.preventDefault();
        next_question();
    })

    $('#remove_question_menu').click(function(e) {
        // preventing from page reload and default actions
        e.preventDefault();
        shift_and_show_question();
    })

    $('#shuffle_questions_menu').click(function(e) {
        // preventing from page reload and default actions
        e.preventDefault();
        shuffle_questions();
    })
})
function begin_flashcards(group_divs) {
    group_array = group_divs.split('~');
    hide_category_group_div_class(group_array);
    if (group_array.length > 1) {
        new_array = group_array.sort(() => Math.random() - 0.5);
        $('#hidden_flashcard_divs').val(new_array.join('~'));
    }
    shift_and_show_question();
}

function array_from_flashcard_divs() {
    group_divs = $('#hidden_flashcard_divs').val()
    return group_divs.split('~');
}

function hide_category_group_div_class(group_array){
    for (idx = 0; idx < group_array.length; idx++) {
        div_id = '#' + group_array[idx];
        if (!$(div_id).hasClass('category_group_div')) {
            $(div_id).addClass('category_group_div');
        }
        if (!$(div_id).hasClass('d-none')) {
            $(div_id).addClass('d-none');
        }
    }
}

function shift_and_show_question() {
    group_array = array_from_flashcard_divs();
    currently_showing = group_array.shift();
    if (!(currently_showing)) {
        $('#flashcard_message').val('We have run out of questions, click study on top menu to continue.');
        return;
    }
    show_one_id_within_class('#' + currently_showing, '.category_group_div');
    $('#currently_showing').val(currently_showing);
    $('#hidden_flashcard_divs').val(group_array.join('~'));
}

function shuffle_questions() {
    append_currently_showing_to_groups();
    group_array = $('#hidden_flashcard_divs').split('~');
    if (group_array.length < 2) {
        $('#flashcard_message').val('Not shuffling, because there is only ' + group_array.length + ' questions left');
        return;
    }
    new_arrary = group_array.sort(() => Math.random() - 0.5);
    $('#hidden_flashcard_divs').val(new_array.join('~'));
    shift_and_show_question();
}

function next_question() {
    append_currently_showing_to_groups();
    shift_and_show_question();
}

function append_currently_showing_to_groups() {
    currently_viewing = $('#currently_showing').val();
    if (currently_showing) {
        group_array_string = $('#hidden_flashcard_divs');
        $('#hidden_flashcard_divs').val(group_array_string + '~' + currently_showing);
        $('#currently_showing').val('');
    }
}

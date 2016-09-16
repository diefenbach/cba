function getUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
        const r = Math.random() * 16 | 0;
        const v = c === 'x' ? r : (r & (0x3 | 0x8));
        return v.toString(16);
    });
}

function collectComponents() {
    const object = {};

    $('input.component, textarea.component').each(function() {
        const id = $(this).attr('id');
        const value = $(this).val();
        object[id] = value;
    });

    return object;
}

function replaceHTML(result) {
    for (const html of result) {
        if ($(html[0]).hasClass('render')) {
            $(html[0]).replaceWith(html[1]);
        } else {
            $(html[0]).parents('.render:first').replaceWith(html[1]);
        }
    }
}

function addMessages(messages) {
    for (const message of messages) {
        const id = getUUID();
        $('#messages').append(`<div class="ui large ${message.type} message" id="message-${id}">${message.text}</div>`);
        setTimeout(() => {
            $(`#message-${id}`).fadeOut(500, function() {
                $(this).remove();
            });
        },
        3000);
    }
}

$(() => {
    $('body').on('click', 'button.default-ajax, a.default-ajax', function(event) {
        const data = collectComponents();
        data.handler = $(this).attr('handler');
        data.event_id = $(this).attr('id');
        data.csrfmiddlewaretoken = $('input[name=csrfmiddlewaretoken]').attr('value');
        $.post('', data, result => {
            replaceHTML(result.html);
            addMessages(result.messages);
        });
        return false;
    });
});

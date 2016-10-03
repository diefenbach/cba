DEBUG = true;

function getUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
        const r = Math.random() * 16 | 0;
        const v = c === 'x' ? r : (r & (0x3 | 0x8));
        return v.toString(16);
    });
}

function collectComponents() {
    const object = new FormData();

    $('input.component, textarea.component, select').each(function() {
        const id = $(this).attr('id');

        if ($(this).attr('type') == 'file') {
            for (const file of $(this)[0].files) {
                object.append(id, file);
            }
        } else if ($(this).attr('type') == 'checkbox') {
            if ($(this).is(':checked')) {
                const value = $(this).val();
                const name = $(this).attr('name');
                object.append(name, value);
            }
        } else if ($(this).is('select')) {
            for (const value of $(this).val()) {
                object.append(`${id}[]`, value);
            }
        } else {
            let value = $(this).val();
            // jquery doesn't post empty lists
            if (value == false) {
                value = '';
            }
            object.append(id, value);
        }
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

function defaultAjaxAction(element, handler) {
    const data = collectComponents();
    data.append('handler', handler);
    data.append('event_id', element.attr('id'));
    data.append('csrfmiddlewaretoken', $('input[name=csrfmiddlewaretoken]').attr('value'));

    if (DEBUG) {
        console.log(data);
    }

    $.ajax({
        url: '',
        type: 'POST',
        data,
        processData: false,
        contentType: false,
        success: result => {
            replaceHTML(result.html);
            addMessages(result.messages);
        },
    });
}

function defaultJSAction(element, handler) {
    const fn = window[handler];
    fn(element);
}


function handleEvent(element, event) {
    const handlerString = element.attr(`${event.type}_handler`);
    const handler = handlerString.split(':');
    if (handler[0] === 'server') {
        defaultAjaxAction(element, handler[1]);
    } else if (handler[0] === 'client') {
        defaultJSAction(element, handler[1]);
    }
}

$(() => {
    $('body').on('click', '.click', function(event) {
        handleEvent($(this), event);
        return false;
    });

    $('body').on('change', '.change', function(event) {
        handleEvent($(this), event);
        return false;
    });

    $('body').on('keyup', '.keyup', function(event) {
        handleEvent($(this), event);
        return false;
    });

    $('body').on('click', 'tr', function(event) {
        $(this).siblings('tr').removeClass('selected');
        $(this).addClass('selected');
    });

    $('body').on('click', '.file-input img', function(event) {
        const checkbox = $(this).siblings('.checkbox').children('input');
        checkbox.prop('checked', !checkbox.prop('checked'));
    });
});


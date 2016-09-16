const getUUID = () => {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = Math.random()*16|0, v = c == 'x' ? r : (r&0x3|0x8);
        return v.toString(16);
    });
};

const collectComponents = () => {
    const object = {};

    $('input.component, textarea.component').each(function() {
        const id = $(this).attr('id');
        const value = $(this).val();
        object[id] = value;
    });

    return object;
};


$(() => {
    $('body').on('click', 'button.default-ajax, a.default-ajax', function(event) {
        const data = collectComponents();
        data.handler = $(this).attr('handler');
        data.event_id = $(this).attr('id');
        data.csrfmiddlewaretoken = $('input[name=csrfmiddlewaretoken]').attr('value');
        $.post('', data, result => {
            for (const html of result.html) {
                if ($(html[0]).hasClass('render')) {
                    $(html[0]).replaceWith(html[1]);
                } else {
                    $(html[0]).parents('.render:first').replaceWith(html[1]);
                }
            }
            for (const message of result.messages) {
                const id = getUUID();
                $('#messages').append('<div class="ui large positive message" id="message-' + id + '">' + message + '</div>');
                setTimeout(() => {
                    $('#message-' + id).fadeOut(500, function() {
                        $(this).remove();
                    });
                },
                1000);
            }
        });
        return false;
    });
});

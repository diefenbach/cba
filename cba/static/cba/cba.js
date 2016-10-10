const CBA = {

    DEBUG: true,

    getUUID: () => {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
            const r = Math.random() * 16 | 0;
            const v = c === 'x' ? r : (r & (0x3 | 0x8));
            return v.toString(16);
        });
    },

    collectComponents: () => {
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
                    object.append(`${name}[]`, value);
                }
            } else if ($(this).attr('type') == 'radio') {
                if ($(this).is(':checked')) {
                    const value = $(this).val();
                    const name = $(this).attr('name');
                    object.append(name, value);
                }
            } else if ($(this).is('select')) {
                if ($(this).attr('multiple')) {
                    for (const value of $(this).val()) {
                        object.append(`${id}[]`, value);
                    }
                } else {
                    object.append(id, $(this).val());
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
    },

    replaceHTML: result => {
        for (const html of result) {
            if ($(html[0]).hasClass('render')) {
                $(html[0]).replaceWith(html[1]);
            } else {
                $(html[0]).parents('.render:first').replaceWith(html[1]);
            }
        }
    },

    addMessages: messages => {
        for (const message of messages) {
            const id = CBA.getUUID();
            $('#messages').append(`<div class="ui large ${message.type} message" id="message-${id}">${message.text}</div>`);
            setTimeout(() => {
                $(`#message-${id}`).fadeOut(500, function() {
                    $(this).remove();
                });
            },
            3000);
        }
    },

    defaultAjaxAction: (element, event, handler) => {
        const data = CBA.collectComponents();
        try {
            data.append('source_id', event.originalEvent.dataTransfer.getData('text'));
        } catch (e) {}

        data.append('handler', handler);
        data.append('event_id', element.attr('id'));
        data.append('csrfmiddlewaretoken', $('input[name=csrfmiddlewaretoken]').attr('value'));

        if (CBA.DEBUG) {
            console.log(data);
        }

        $.ajax({
            url: '',
            type: 'POST',
            data,
            processData: false,
            contentType: false,
            success: result => {
                CBA.replaceHTML(result.html);
                CBA.addMessages(result.messages);
            },
        });
    },

    defaultJSAction: (element, event, handler) => {
        const fn = CBA[handler];
        fn(element);
    },

    handleEvent: (element, event) => {
        const handlerString = element.attr(`${event.type}_handler`);
        const handler = handlerString.split(':');
        if (handler[0] === 'server') {
            CBA.defaultAjaxAction(element, event, handler[1]);
        } else if (handler[0] === 'client') {
            CBA.defaultJSAction(element, event, handler[1]);
        }
    },
};

// Register Events
$(() => {
    $('body').on('click', '.click', function(event) {
        CBA.handleEvent($(this), event);
        return false;
    });

    $('body').on('change', '.change', function(event) {
        // Unfortunately semantic-ui wraps the original select with a div and
        // copy its classes to this.
        let element = $(this);
        if ($(this).hasClass('dropdown')) {
            element = $(this).children('select:first');
        }
        CBA.handleEvent(element, event);
        return false;
    });

    $('body').on('mouseover', '.mouseover', function(event) {
        CBA.handleEvent($(this), event);
        return false;
    });

    $('body').on('mouseout', '.mouseout', function(event) {
        CBA.handleEvent($(this), event);
        return false;
    });

    $('body').on('keyup', '.keyup', function(event) {
        CBA.handleEvent($(this), event);
        return false;
    });

    // DnD: Stores id of the draggable component for later use
    $('body').on('dragstart', '.draggable', function(event) {
        event.originalEvent.dataTransfer.setData('text', event.target.id);
    });

    // DnD: handles drop event
    $('body').on('drop', '.droppable', function(event) {
        CBA.handleEvent($(this), event);
        return false;
    });

    // DnD: Allows drop
    $('body').on('dragover', '.droppable', function(event) {
        return false;
    });

    // Table Component: selects row if clicked.
    $('body').on('click', 'tr', function(event) {
        $(this).siblings('tr').removeClass('selected');
        $(this).addClass('selected');
    });

    // FileInput Component: toggles checkbox when the image is clicked.
    $('body').on('click', '.file-input img', function(event) {
        const checkbox = $(this).siblings('.checkbox').children('input');
        checkbox.prop('checked', !checkbox.prop('checked'));
    });
});

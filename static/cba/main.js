var collect_components = function() {
    var object = {};

    $(".component").each(function() {
        var id = $(this).attr("id");
        try {
            var value = $(this).val();
        } catch(e) {
            var value = undefined;
        };
        object[id] = value;
    });

    return object;
};

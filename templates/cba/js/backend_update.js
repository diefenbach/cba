<script type='text/javascript'>
    $('#{{ component.id }}').on('click', function(event) {
        var data = collect_components();
        data["handler"] = $(this).attr("handler");
        data["event_id"] = $(this).attr("id");
        $.get("/", data, function(data) {
            for (var html in data['html']) {
                var element = $(data['html'][html][0]);
                if (element.hasClass("render")) {
                    element.replaceWith(data['html'][html][1]);
                }
                else {
                    element.parents(".render:first").replaceWith(data['html'][html][1]);
                }
            }
        });
        return false;
    });
</script>

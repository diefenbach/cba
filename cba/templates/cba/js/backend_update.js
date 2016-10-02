<script type='text/javascript'>
    $('#{{ component.id }}').on('click', function(event) {
        const data = collect_components();
        data["handler"] = $(this).attr("handler");
        data["event_id"] = $(this).attr("id");
        data["csrfmiddlewaretoken"] = $("input[name=csrfmiddlewaretoken]").attr("value");
        $.post("/perf", data, data => {
            for (const html of data.html) {
                if ($(html[0]).hasClass("render")) {
                    $(html[0]).replaceWith(html[1]);
                }
                else {
                    $(html[0]).parents(".render:first").replaceWith(html[1]);
                }
            }
        });
        return false;
    });
</script>

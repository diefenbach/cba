<script type='text/javascript'>
    $('body').on('{{ action.event }}', '{{ action.selector }}', function(event) {
        $('{{ action.target }}').html($('{{ action.source }}').val());
        return false;
    });
</script>

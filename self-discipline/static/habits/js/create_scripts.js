function RangeDisplayer() {
    $('#id_period').on('input', function() {
        data = $('#id_period').val()
        $('#range-value').text(data)
    })
}

RangeDisplayer()

$(document).ready(function () {
    let date = new Date();
    days = $('.day-date');
    value = 24
    for (let day of days) {
        data_attr = $(day)
        data = data_attr.attr("data").split(' ')
        dayDate = new Date(Number(data[0]), Number(data[1]) - 1, Number(data[2]))
        
        if (((date - dayDate)/1000/60/60 < value) & ((date - dayDate)/1000/60/60 > 0)) {
            par = $(data_attr.parent());
            par.addClass('current');
        }

        if (dayDate > date) {
            par = $(data_attr.parent());
            par.find('form').remove()
        }
    }
})
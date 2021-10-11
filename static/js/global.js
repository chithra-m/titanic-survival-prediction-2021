$(document).on('change', '#t_class', function () {
    let val = $('#t_class').val();
    let text = '';
    if(val === '1')
        text = 'First Class'
    if(val === '2')
        text = 'Second Class'
    if(val === '3')
        text = 'Third Class'
    
    $('#spn_BookingClass').text(text);
    
})

function predictData() {
    let fullName = $('#fullName').val();
    let gender = $('#male').prop('checked') ? '1' : '0'
    let age = $('#age').val();
    let t_class = $('#t_class').val();
    let sibsp = $('#sibsp').val();
    let parch = $('#parch').val();

    var jsonData = {
        'fullName' : fullName,
        'gender': gender,
        'age': age,
        't_class': t_class,
        'sibsp': sibsp,
        'parch': parch
    }

    $.ajax({
        url: `/predict`,
        method: 'POST',
        data: jsonData,
        success: function (response) {
            if (typeof response !== undefined && response !== null) {
                $('#txtResult').text(response);
                $('#resultContainer').show();
            }
            else {
                console.log('failed');
            }
        },
        error: function () {
            console.log('error');
        }    
    })
}


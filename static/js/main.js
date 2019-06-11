$(document).ready(function(){

  $('#submit').on('click',function(event){

    $.ajax({
      data: {
        name: $('#name').val(),
        age: $('#age').val(),
        gender: $('#gender option:selected').text()
,      },
      type: 'POST',
      url: '/process'

    })
    .done(function(data) {

        $('#advice-result-1').text(data.advice_1);
        $('#advice-result-2').text(data.advice_2);
        $('#advice-result-3').text(data.advice_3);

    });
  });
});

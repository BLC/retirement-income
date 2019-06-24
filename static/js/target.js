$(document).ready(function(){

  $('#calc-take-home-income').on('click',function(event){

    $.ajax({
      data: {
        salary: $('#salary').val(),
        contribution: $('#account-1-contribution').val(),
        tax: $('#account-1-tax option:selected').text(),
        replacement_1: $('#replacement-ratio-1').val(),
        replacement_2: $('#replacement-ratio-2').val()
      },
      type: 'POST',
      url: '/target'

    })
    .done(function(data) {

      if (data.error) {

      }
      else {

        $('.take-home-income').text(data.target_0);
        $('#non-dis-spend').text(data.target_1);
        $('#dis-spend').text(data.target_2);
      }

    });
  });
});

function calc_target_1(ratio) {
  var target_income = $('#take-home-income').text();
  $('#non-dis-spend').text(Math.round(parseFloat(target_income) * parseFloat(ratio) / 100));
};

function calc_target_2(ratio) {
  var target_income = $('#take-home-income').text();
  $('#dis-spend').text(Math.round(parseFloat(target_income) * parseFloat(ratio) / 100));
};

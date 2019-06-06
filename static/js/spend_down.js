$('#calc-spend-down-age').on('click',function(event){

  $.ajax({
    data: {
      confidence_level:$('#spend-down-confidence').val(),
      gender:$('#gender option:selected').text(),
      age: $('#age').val(),
    },
    type: 'POST',
    url: '/spenddown'

  })
  .done(function(data) {

    if (data.error) {

    }
    else {

      console.log(data.spend_down_age)

      $('#spend-down-age').text(data.spend_down_age);
    }

  });

});
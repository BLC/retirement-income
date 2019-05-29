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

      if (data.error) {

        $('#output1').text(data.error);

      }
      else {

        $('.name_output').text(data.name);
        $('.age_output').text(data.age);
        $('.gender_output').text(data.gender);
      }

    });
  });
});

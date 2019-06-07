$('#calc-Social-Security').on('click',function(event){

  $.ajax({
    data: {
      salary: $('#salary').val(),
      claim_age: $('#ss-claim-age').val(),
    },
    type: 'POST',
    url: '/social_security'

  })
  .done(function(data) {

    if (data.error) {

    }
    else {

      console.log(data.social_security_benefit)

      $('#social-security-benefit').text(data.social_security_benefit);
    }

  });

});

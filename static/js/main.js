$(document).ready(function(){

  $('#submit').on('click',function(event){

    $.ajax({
      data: {
        name: $('#name').val(),
        age: parseInt($('#age').val()),
        gender: $('#gender option:selected').text(),
        salary: parseFloat($('#salary').val()),
        retirement_age: parseInt($('#retirement-age').val()),
        manageable_balance: parseFloat($('#account-1-balance').val()),
        manageable_contrib: parseFloat($('#account-1-contribution').val()),
        manageable_tax: $('#account-1-tax option:selected').text(),
        ss_claim_age: parseInt($('#ss-claim-age').val()),
        ss_benefit: parseFloat($('#ss-benefit').val()),
        annuity_start_age: parseInt($('#annuity-start-age').val()),
        annuity_benefit: parseFloat($('#annuity-benefit').val()),
        non_dis_target: parseFloat($('#non-dis-spend').text()),
        dis_target: parseFloat($('#dis-spend').text()),
        spend_down_age: parseInt($('#spend-down-age').text()),
        minimum_spending_ratio: parseFloat($('#min-spending-ratio-output').text())
      },
      type: 'POST',
      url: '/process'

    })
    .done(function(data) {

        $('#advice-result-1').text(data.target.minimum_ratio);
        $('#advice-result-2').text(data.spend_down_age);
        $('#advice-result-3').text(data.social_security.claim_age);

    });
  });
});

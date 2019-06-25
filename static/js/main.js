function wealth_plot(data,percentile) {

  Highcharts.chart('wealth-plot', {
    chart: {
      type: 'area'
    },
    title: {
      text: 'Wealth Projection'
    },
    xAxis: {
      title: {
        text: 'Age'
      },
      allowDecimals: false,
      labels: {
        formatter: function () {
          return this.value; 
        }
      }
    },
    yAxis: {
      title: {
        text: 'Wealth'
      },
      labels: {
        formatter: function () {
          return this.value / 1000 + 'k';
        }
      }
    },
    tooltip: {
      pointFormat: 'Wealth-{series.name} at age <b>{point.x}</b><br/>is {point.y:,.0f}'
    },
    plotOptions: {
      area: {
        pointStart: data.Age[0],
        marker: {
          enabled: false,
          symbol: 'circle',
          radius: 2,
          states: {
            hover: {
              enabled: true
            }
          }
        }
      }
    },
    series: [{
      name: percentile.toString()+'%',
      data: data.Wealth.filter(d => d.percentile === percentile).map(d => d.wealth)[0]
    }]
  });

};


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

      console.log(data);

      wealth_plot(data,30);

      $('input:radio[name="wealth_plot"]').change(function() {
        wealth_plot(data,parseFloat($(this).val()));
      })

    });
  });
});

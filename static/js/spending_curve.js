var slideInput = document.querySelector("#spending-min-ratio");


function drawSpendingCurve (x_1,x_2) {
    // set the dimensions and margins of the graph
    var margin = {top: 10, right: 30, bottom: 20, left: 80},
    width = 580 - margin.left - margin.right,
    height = 240 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    var svg = d3.select("#spending-curve")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform",
      "translate(" + margin.left + "," + margin.top + ")");

    // var x_1 = parseInt($('#retirement-age').val());
    // var x_2 = parseInt($('#spend-down-age').text());
    var a_param = 1/Math.pow((x_1-x_2)/2,2);
    var age_array = Array.from(Array(x_2-x_1+1),(x,index) => index + x_1);

    // add the x Axis
    var x = d3.scaleLinear()
    .domain([x_1, x_2])
    .range([0, width]);

    svg.append("g")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(x));

    // add the y Axis
    var y = d3.scaleLinear()
    .range([height, 0])
    .domain([0, 1]);

    svg.append("g")
    .call(d3.axisLeft(y));

    // Calc Spending Curve Function and Update Curve 
    function calcSpendingCurve(age,alpha) {
    
        var a = (1-alpha) * a_param;
        var b = alpha;
    
        return a * Math.pow((age-(x_1+x_2)/2),2) + b;
    }

    // Calculate the initial input values
    // d3.select("#spending-min-ratio").property("value", "1");
    var alpha_init = 1;
    d3.select("#min-spending-ratio-output").text(alpha_init*100);
    var age_ratio_array_init = age_array.map(d => [d,calcSpendingCurve(d,alpha_init)]);

    var curve = svg
    .append('g')
    .append("path")
      .attr("class", "mypath")
      .datum(age_ratio_array_init)
      .attr("fill", "none")
      .attr("opacity", ".8")
      .attr("stroke", "#69b3a2")
      .attr("stroke-width", 2)
      .attr("stroke-linejoin", "round")
      .attr("d",  d3.line()
        .curve(d3.curveBasis)
          .x(function(d) { return x(d[0]); })
          .y(function(d) { return y(d[1]); })
    );

    function updateCurve(alpha) {
        // recompute density estimation
        var age_ratio_array = age_array.map(d => [d,calcSpendingCurve(d,alpha)]);
        // update the chart
        curve
        .datum(age_ratio_array)
        .transition()
        .duration(1000)
        .attr("d",  d3.line()
            .curve(d3.curveBasis)
            .x(function(d) { return x(d[0]); })
            .y(function(d) { return y(d[1]); })
        );
    }

    slideInput.addEventListener('input',function(event) {
        var selectedValue = parseFloat(slideInput.value);
        d3.select("#min-spending-ratio-output").text(Math.round(selectedValue*100));
        updateCurve(selectedValue);
    },false);
}

var age_1 = parseInt($('#retirement-age').val());
var age_2 = parseInt($('#spend-down-age').text());

drawSpendingCurve (age_1,age_2);

$('#calc-spending-curve').on('click',function(event){

    // Re- render the chart
    d3.select("#spending-curve").selectAll("svg").remove();

    age_1 = parseInt($('#retirement-age').val());
    age_2 = parseInt($('#spend-down-age').text());

    drawSpendingCurve (age_1,age_2);
});


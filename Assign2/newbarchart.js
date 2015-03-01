function bar(flag)
{

var margin = {top: 200, right: 20, bottom: 150, left: 100},
    width = 960 - margin.left - margin.right,
    height = 700 - margin.top - margin.bottom;


var x = d3.scale.ordinal()
    .rangeRoundBands([0, width], .1);

var y = d3.scale.linear()
    .range([height, 0]);

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left")

var tip = d3.tip()
  .attr('class', 'd3-tip')
  .offset([-10, 0])
  .html(function(d) {
    return "<table border='0' style='width:100%;color:red'><tr><td>Player Name: "+d.PlayerName+"</td></tr><tr><td>Country: "+d.Country+"</td></tr><tr><td>Granslam wins: "+d.final+"</td></tr><tr><td>Total Wins: "+d.Wins+"</td></tr><tr><td>Total Matches Played: "+d.Total+"</td></tr><tr><td>Total Defeats: "+d.Lost+"</td></tr><tr><td>Semi Final Wins: "+d.semi+"</td></tr><tr><td>Quarter Final Wins: "+d.quarter+"</td></tr><tr><td>Fourth Round Wins: "+d.fourth+"</td></tr><tr><td>Third Round Wins: "+d.third+"</td></tr><tr><td>Second Round Wins: "+d.second+"</td></tr><tr><td>First Round Wins: "+d.first+"</td></tr></table>";
  })



var svg = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")")

svg.call(tip);


d3.csv("stats_data.csv",  function(error, data) {
  x.domain(data.map(function(d) { return d.Initials; }));
  y.domain([0, d3.max(data, function(d) { return d.Wins; })]);

  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis)
      .append("text")
      .attr("x",500)
      .attr("y",40)
      .style("text-anchor", "middle")
      .style("font-size","16px")
      .text("Players Name");

  var yaxis_obj = svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("x", 3)
      .attr("dy", "-2.25em")
      .style("text-anchor", "end")
      .style("font-size","15px");

    if (flag == 1)
{
  svg.selectAll(".bar")
      .data(data)
    .enter().append("rect")
      .attr("class", "bar")
      .attr("x", function(d) { return x(d.Initials); })
      .attr("width", x.rangeBand())
      .attr("y", function(d) { return y(d.Wins); })
      .attr("height", function(d) { return height - y(d.Wins); })
      .on('mouseover', tip.show)
      .on('mouseout', tip.hide)

      yaxis_obj.text("Total Wins of Players");

}

else if (flag == 2)
{

  svg.selectAll(".bar")
      .data(data)
    .enter().append("rect")
      .attr("class", "bar")
      .attr("x", function(d) { return x(d.Initials); })
      .attr("width", x.rangeBand())
      .attr("y", function(d) { return y(d.Lost); })
      .attr("height", function(d) { return height - y(d.Lost); })
      .on('mouseover', tip.show)
      .on('mouseout', tip.hide)

      yaxis_obj.text("Total Loses of Players");

}

  svg.append("text")
        .attr("x", (width / 2))             
        .attr("y", 0 - (margin.top / 2))
        .attr("text-anchor", "middle")  
        .style("font-size", "16px") 
        .style("text-decoration", "underline")  
        .text("Performance of Players in Australian Open in last 11 years");
    
});

}

function init()
{
d3.select("#data1")
        .on("click", function(d,i) {
            bar(1)
        })   
    d3.select("#data2")
        .on("click", function(d,i) {
            bar(2)
        }) 
}

function type(d) {
  d.Wins = +d.Wins;
  return d;
}

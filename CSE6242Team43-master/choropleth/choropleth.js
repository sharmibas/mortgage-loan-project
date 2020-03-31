var margin = {top: 80, right: 180, bottom: 80, left: 180},
    width = 1100 - margin.left - margin.right,
    height = 650 - margin.top - margin.bottom;

var svg = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right + width / 2)
    .attr("height", height + margin.top + margin.bottom)
    .attr("style", "margin-top:20px")

var state_g = svg.append("g")
	.attr("transform", "translate(" + (width + margin.left + margin.right - 100) + ",0)")

var path = d3.geo.path();
var formatComma = d3.format(",")
var min_obs = 25
var label_data_vals = [0, 0,.00001, 2.5, 5.0, 7.5, 10.0, 12.5, 15.0, 17.5, 20.0, 22.5, 25.0, 27.5, 30.0, 32.5, 35.0, 37.5, 40.0, 42.5, 45.0, 47.5, 50.0, 52.5, 55.0, 57.5, 60.0, 62.5, 65.0, 67.5, 70.0, 72.5, 75.0, 77.5, 80.0, 82.5, 85.0, 87.5, 90.0, 92.5, 95.0, 97.5, 100.0]
//White,grey,black
//var colors_for_legend = ['#ffffff','#f9f9f9','#f1f1f1','#eaeaea','#e5e5e5','#dedede','#d7d7d7','#d1d1d1','#cacaca','#c4c4c4','#bebebe','#b7b7b7','#b1b1b1','#aaaaaa','#a5a5a5','#9e9e9e','#979797','#929292','#8c8c8c','#858585','#808080','#797979','#747474','#6e6e6e','#686868','#636363','#5e5e5e','#585858','#525252','#4d4d4d','#474747','#414141','#3d3d3d','#383838','#323232','#2e2e2e','#282828','#242424','#1f1f1f','#1b1b1b','#161616','#101010','#080808','#000000']
// white, MidnightBlue
var colors_for_legend = ['#ffffff','#faf9fb','#f5f3f8','#f0edf5','#eae7f1','#e5e1ee','#e0dceb','#dbd6e7','#d6cfe4','#d0cae0','#cbc4dd',
												 '#c7beda','#c1b9d6','#bcb3d3','#b8add0','#b2a7cc','#ada2c9','#a89dc6','#a396c2','#9e92bf','#998bbb','#9487b8',
												 '#8f81b5','#8a7bb1','#8576ae','#8071ab','#7b6ca7','#7667a4','#7162a1','#6c5c9e','#67579a','#625397','#5c4e94',
												 '#574991','#52438d','#4c3f8a','#473987','#413583','#3c3080','#362b7d','#2f267a','#292276','#211d73','#191970']
// white, red
//var colors_for_legend = ['#ffffff','#fffcfa','#fff7f5','#fff4ef','#fff0ea','#ffece4','#ffe7df','#ffe3da','#ffe0d4','#ffdbcf','#ffd8ca','#ffd4c4','#ffd0bf','#ffccba','#ffc8b5','#ffc3b0','#ffbfaa','#ffbba4','#ffb69f','#ffb39a','#ffad94','#ffa98f','#ffa58a','#ffa184','#ff9c7e','#ff987a','#ff9374','#ff8d6e','#ff8869','#ff8463','#ff7e5e','#ff7a58','#ff7452','#ff6e4d','#ff6847','#ff6240','#ff5c3b','#ff5434','#ff4d2e','#ff4426','#ff3a1f','#ff2e17','#ff1f0d','#ff0000']
// white, green
//var colors_for_legend = ['#ffffff','#fafcf9','#f5f9f4','#f0f6ee','#ebf4e8','#e6f0e2','#e1eedc','#dcebd7','#d7e8d1','#d2e5cb','#cde2c5','#c8dfbf','#c3dbba','#bed9b4','#b9d5ae','#b3d3a9','#aecfa3','#a9cd9d','#a4ca98','#9fc792','#9ac48d','#95c188','#91be82','#8cbb7d','#87b877','#82b572','#7cb36d','#77b067','#72ac62','#6caa5c','#67a657','#62a351','#5ca04c','#569d46','#509b41','#4a983b','#449535','#3e912f','#378e29','#2f8c23','#27891c','#1e8614','#13830b','#008000']
// '#ffe100', '#ff4700'
//var colors_for_legend = ['#ffe100','#ffde00','#ffdb00','#ffd800','#ffd500','#ffd200','#ffce00','#ffcb00','#ffc800','#ffc500','#ffc200','#ffbf00','#ffbc00','#ffb800','#ffb500','#ffb200','#ffaf00','#ffac00','#ffa800','#ffa500','#ffa200','#ff9e00','#ff9b00','#ff9800','#ff9400','#ff9100','#ff8d00','#ff8a00','#ff8600','#ff8300','#ff7f00','#ff7b00','#ff7800','#ff7400','#ff7000','#ff6c00','#ff6800','#ff6400','#ff5f00','#ff5b00','#ff5600','#ff5100','#ff4c00','#ff4700']
// white, yellow, green
//var colors_for_legend = ['#ffffff','#fffff6','#ffffed','#fffee5','#fffedc','#fffdd4','#fffccc','#fffbc4','#fefabc','#fcf9b4','#faf8ad','#f7f6a5','#f4f59e','#f1f396','#eef18f','#eaef88','#e6ed81','#e2eb7b','#dee874','#d9e66d','#d4e367','#cfe061','#c9dd5b','#c4da55','#bed74f','#b8d349','#b1d043','#abcc3e','#a4c938','#9dc533','#96c12e','#8ebc29','#86b824','#7eb41f','#76af1a','#6daa15','#64a511','#5ba10c','#519b08','#479605','#3b9102','#2e8b01','#1e8600','#008000']

var subchart_color = colors_for_legend[28]

//var legend_labels = ["Obs < x", "0%", "10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"];
//var legend_labels = ["Obs < " + min_obs, '0%', '1%', '2%', '3%', '4%', '5%', '6%', '7%', '8%', '9%', '10%', '11%', '12%', '13%', '14%', '15%', '16%', '17%', '18%', '19%', '20%', '21%', '22%', '23%', '24%', '25%', '26%', '27%', '28%', '29%', '30%', '31%', '32%', '33%', '34%', '35%', '36%', '37%', '38%', '39%', '40%', '41%', '42%', '43%', '44%', '45%', '46%', '47%', '48%', '49%', '50%', '51%', '52%', '53%', '54%', '55%', '56%', '57%', '58%', '59%', '60%', '61%', '62%', '63%', '64%', '65%', '66%', '67%', '68%', '69%', '70%', '71%', '72%', '73%', '74%', '75%', '76%', '77%', '78%', '79%', '80%', '81%', '82%', '83%', '84%', '85%', '86%', '87%', '88%', '89%', '90%', '91%', '92%', '93%', '94%', '95%', '96%', '97%', '98%', '99%', '100%'];
var legend_labels = ["Obs < " + min_obs, '0%', '2.5%', '5%', '7.5%', '10%', '12.5%', '15%', '17.5%', '20%', '22.5%', '25%', '27.5%', '30%', '32.5%', '35%', '37.5%', '40%', '42.5%', '45%', '47.5%', '50%', '52.5%', '55%', '57.5%', '60%', '62.5%', '65%', '67.5%', '70%', '72.5%', '75%', '77.5%', '80%', '82.5%', '85%', '87.5%', '90%', '92.5%', '95%', '97.5%', '100%']

var color = d3.scale.threshold()
    //.range(['#ffffff','#ecf0f7','#d8e1ee','#c5d3e6','#b1c6de','#9db8d5','#89a9cd','#759dc5','#5e8fbc','#4682b4'])
    //.range(["#f7fbff", "#deebf7", "#c6dbef", "#9ecae1", "#6baed6", "#4292c6", "#2171b5", "#08519c", "#08306b"]);
    //.domain([0, 0,.00001, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100])    
    //.range(['#ffffff','#fcfcfe','#f9fafc','#f5f7fb','#f3f5fa','#f0f3f8','#ecf0f7','#e9eef6','#e6ebf4','#e3eaf3','#e0e7f1','#dde5f0','#dae2ef','#d7dfed','#d5ddec','#d1dbeb','#cfd9e9','#ccd6e8','#c9d3e7','#c7d2e6','#c3cee4','#c1cce3','#becae1','#bbc8e0','#b8c5df','#b5c3dd','#b3c1dc','#b0bedb','#aebcda','#abb9d8','#a8b7d7','#a6b4d6','#a3b2d4','#a1afd3','#9eacd2','#9cabd1','#9aa8cf','#97a6ce','#94a3cd','#92a1cb','#909fca','#8d9cc9','#8b99c8','#8997c6','#8695c5','#8493c4','#8190c2','#7f8dc1','#7d8bc0','#7a89bf','#7987be','#7683bc','#7481bb','#717fba','#6f7db8','#6e7bb7','#6b78b6','#6976b5','#6773b4','#6570b2','#636fb1','#616cb0','#5f6aaf','#5d67ad','#5b65ac','#5963ab','#5660aa','#555da8','#535ba7','#5058a6','#4f57a5','#4c54a3','#4b51a2','#494fa1','#474ca0','#454a9f','#43489d','#41459c','#3f439b','#3d419a','#3b3f99','#393c97','#373996','#353695','#333594','#313293','#2f2f92','#2c2d90','#2b2a8f','#28278e','#26258d','#23228c','#21208b','#1e1d89','#1c1a88','#191787','#161386','#121085','#0f0c84','#0a0882','#050481','#000080']);
    .domain(label_data_vals)    
    .range(colors_for_legend);

// Initialize filter values
year = '1999'
vintage = '1999'
fico = '(300,670]'
ltv = '(0,60]'

d3.queue()
  .defer(d3.json, "us.json")
  .defer(d3.csv, "dflts.csv")
  .await(processData);

function processData(error, us, dflt) {
  if (error) throw error;

  var legend = svg.selectAll("g.legend")
  .data(label_data_vals)
  .enter().append("g")
  .attr("class", "legend");

  var ls_w = 20, ls_h = 5;

  legend.append("rect")
    .attr("x", width + margin.left + margin.right-200)
    .attr("y", function(d, i){ return height - (i*ls_h) - 2*ls_h;})
    .attr("width", ls_w)
    .attr("height", ls_h)
    .style("fill", function(d, i) { return color(d); })
    .style("opacity", 0.8);

  legend.append("text")
    .attr("x", function(d, i){
                        if ((i-1)%4 == 0 ) {return width+margin.left+margin.right-260} 
                        else {return 0};})
    .attr("y", function(d, i){
                        if ((i-1)%4 == 0 ) {return height - (i*ls_h) - ls_h - 4}
                        else {return 0};})
    .text(function(d, i){if ((i-1)%4 ==0 ) {return legend_labels[i]} else {return ''};});    
   
        
        
  var map = svg.append("g")
    .attr("class", "counties")
    .selectAll("path")
			.data(topojson.feature(us, us.objects.states).features)
			
	// Removes state specific info
	function removeInfo() {
		state_g.selectAll("rect").remove()
		state_g.selectAll("text").remove()
		state_g.selectAll("g").remove()
	}

  // Function to display detailed default info on state click
  function displayInfo(stateInfo) {
		if (!state_g.selectAll("rect").empty()){
			if (!d3.select("#r" + stateInfo.StateName.replace(" ", "")).empty()){ // If the currently clicked state is the one already shown, just remove it and don't display anything else
				removeInfo();
				return
			}
			removeInfo();
		}
			
		state_g.append("rect")
			.attr({
				id: "r" + stateInfo.StateName.replace(" ", ""),
				width: width / 2,
				height: height + margin.top + margin.bottom,
				fill: "white",
				stroke: "white"
			})
			
		state_g.append("text")
			.text(stateInfo.StateName)
			.attr({
				x: (width / 4),
				y: 30,
				"text-anchor": "middle",
				"font-size": "25px"
				})
				.style({
				fill: "black"
			})
			
		// Reiterate what parameters the user has chosen
		state_g.append("text")
			.text("Vintage:")
			.attr({
			x: 10,
			y: 65,
			"text-anchor": "left",
			"font-size": "15px"
			})
			.style({
			fill: "black"
			})
			
		state_g.append("text")
			.text(vintage)
			.attr({
			x: width/2-10,
			y: 65,
			"text-anchor": "end",
			"font-size": "15px"
			})
			.style({
			fill: "black"
			})
			

		state_g.append("text")
			.text("Year:")
			.attr({
			x: 10,
			y: 85,
			"text-anchor": "left",
			"font-size": "15px"
			})
			.style({
			fill: "black"
			})

		state_g.append("text")
			.text(year)
			.attr({
			x: width/2-10,
			y: 85,
			"text-anchor": "end",
			"font-size": "15px"
			})
			.style({
			fill: "black"
			})

			
		state_g.append("text")
			.text("FICO Range:")
			.attr({
			x: 10,
			y: 105,
			"text-anchor": "right",
			"font-size": "15px"
			})
			.style({
			fill: "black"
			})
			
		state_g.append("text")
			.text(fico)
			.attr({
			x: width/2-10,
			y: 105,
			"text-anchor": "end",
			"font-size": "15px"
			})
			.style({
			fill: "black"
			})	  
			
		state_g.append("text")
			.text("Loan-To-Value Range:")
			.attr({
			x: 10,
			y: 125,
			"text-anchor": "right",
			"font-size": "15px"
			})
			.style({
			fill: "black"
			})
			
		state_g.append("text")	  
			.text(ltv)
			.attr({
			x: width/2-10,
			y: 125,
			"text-anchor": "end",
			"font-size": "15px"
			})
			.style({
			fill: "black"
			})		  
			
		// Show state information
		state_g.append("text")
			.text("Number of Defaults:")
			.attr({
			x: 10,
			y: 155,
			"text-anchor": "left",
			"font-size": "15px"
			})
			.style({
			fill: "black"
			})
			
		state_g.append("text")	  
			.text(formatComma(stateInfo.Defaults))
			.attr({
			x: width/2-10,
			y: 155,
			"text-anchor": "end",
			"font-size": "15px"
			})
			.style({
			fill: "black"
			})	  
				
		state_g.append("text")
			.text("Number of Loans:")
			.attr({
			x: 10,
			y: 175,
			"text-anchor": "left",
			"font-size": "15px"
			})
			.style({
			fill: "black"
			})
			
		state_g.append("text")
			.text(formatComma(stateInfo.Observations))
			.attr({
			x: width/2-10,
			y: 175,
			"text-anchor": "end",
			"font-size": "15px"
			})
			.style({
			fill: "black"
			})	  
			
		state_g.append("text")
			.text("Default Percentage:")
			.attr({
			x: 10,
			y: 195,
			"text-anchor": "left",
			"font-size": "15px"
			})
			.style({
			fill: "black"
			})
			
		state_g.append("text")
			.text(d3.round(stateInfo.Default_Prcnt,2) + "%")
			.attr({
			x: width/2-10,
			y: 195,
			"text-anchor": "end",
			"font-size": "15px"
			})
			.style({
			fill: "black"
			})	  

		state_g.append("text")
			.text("Average Risk Score:")
			.attr({
			x: 10,
			y: 215,
			"text-anchor": "left",
			"font-size": "15px"
			})
			.style({
			fill: "black"
			})

		state_g.append("text")
			.text(d3.round(stateInfo.Avg_RiskPoints,2))
			.attr({
			x: width/2-10,
			y: 215,
			"text-anchor": "end",
			"font-size": "15px"
			})
			.style({
			fill: "black"
			})	  
		
			
		if (vintage != "1999-2017") {
			// Parse default data to display in bar graph
			dflt_data = []
			min_year = 2222
			max_year = 0
			dflt.forEach(function(d){
				if (d.STATE_NAME == stateInfo.StateName && d.fico_filter == fico && d.ltv_filter == ltv && d.vintage_filter == vintage && d.year_filter >= vintage && d.year_filter.length == 4){
					if (min_year > +d.vintage_filter) 
						min_year = +d.vintage_filter;
					if (max_year < +d.vintage_filter) 
						max_year = +d.vintage_filter;
					if (d.Observations < min_obs)
						d.Default_Prcnt = 0;
					dflt_data.push({"Default_Prcnt": parseFloat(d.Default_Prcnt) * 100, "year_filter": +d.year_filter, "Observations": +d.Observations})
				}
			})
		
			// Create the graph of the state throughout the vintage years
			var graph_g = state_g.append("g")
						
			var line_width = 325;
			var xsc = d3.scale.linear()
						.domain([d3.min(dflt_data, function(d){ return d.year_filter; }), d3.max(dflt_data, function(d){ return d.year_filter; }) + 1])
						.range([0, line_width]);
			var ysc = d3.scale.linear()
						.domain([d3.min(dflt_data, function(d){ return d.Default_Prcnt; }), d3.max(dflt_data, function(d){ return d.Default_Prcnt; })])
						.range([line_width, 0]);
					
			graph_g.append("g")
				.attr("class", "axis")
				.attr("transform", "translate(50," + (275 + line_width) + ")")
				.call(d3.svg.axis().scale(xsc).orient("bottom").ticks(dflt_data.length).tickFormat(d3.format("d")))
				.selectAll("text")
					.attr("transform", "rotate(-45)")
					.attr("dx", "-2em")
					.attr("dy", "1em")
					
				
			graph_g.append("g")
				.attr("class", "axis")
				.attr("transform", "translate(50,275)")
				.call(d3.svg.axis().scale(ysc).orient("left").ticks(5).tickFormat(d3.format(".2f")))
			
			graph_g.append("text")
				.text("Historical Default Experience")
				.attr("text-anchor", "middle")
				.attr("font-family", "sans-serif")
				.attr("font-size", "20px")
				.attr("fill", "gray")
				.attr("font-weight", "bold")
				.attr("x", width / 4)
				.attr("y", 250);
			
			graph_g.append("text")
				.text("Default Percentage (%)")
				.attr("text-anchor", "start")
				.attr("font-family", "sans-serif")
				.attr("font-size", "10px")
				.attr("fill", "gray")
				.attr("font-weight", "bold")
				.attr("x", 10)
				.attr("y", 270)
			
			graph_g.append("text")
				.text("Year")
				.attr("text-anchor", "start")
				.attr("font-family", "sans-serif")
				.attr("font-size", "10px")
				.attr("fill", "gray")
				.attr("font-weight", "bold")
				.attr("x", 50 + line_width + 10)
				.attr("y", 275 + line_width + 15)

			var bar = state_g.selectAll(".bar")
				.data(dflt_data)
				.enter().append("g")
				.attr("class", "bar")

			bar.append("rect")
				.data(dflt_data)
				.attr("x", function(d) { return 50 + xsc(d.year_filter)})
				.attr("y", function(d) { return 274 + ysc(d.Default_Prcnt)})
				.attr("width", function(d) { return xsc(dflt_data[1].year_filter)})
				.attr("height", function(d) { 
					if (d.Observations >= min_obs)
						return line_width - ysc(d.Default_Prcnt)
					else
						return 0;
				})
				.attr("fill", function(d) { return color(d.Default_Prcnt) });
		}


  } // displayInfo()

  // Function update map after selecting a different filter.
  function updateMap() {
    // Get default percentage for each state based on filters
    dfltById = []

    // Info by state ID, contains name, defaults, observations, risk score, and default pcnt
    stateInfo = []
    dflt.forEach(function(d) {
      if (d.year_filter == year && d.vintage_filter == vintage && d.fico_filter == fico && d.ltv_filter == ltv) {
        stateObj = {}
        stateObj['StateName'] = d.STATE_NAME;
        stateObj['Defaults'] = +d.Defaults;
        stateObj['Observations'] = +d.Observations;
        stateObj['Avg_RiskPoints'] = +d.Avg_RiskPoints;

        // Only count default percentage if number of observations is significant
        if (+d.Observations >= min_obs) {
          stateObj['Default_Prcnt'] = +d.Default_Prcnt * 100;
          dfltById[+d.STATE] = +d.Default_Prcnt * 100;
        }
        else {
          stateObj['Default_Prcnt'] = 'n/a';
          dfltById[+d.STATE] = 0;
        }
        stateInfo[+d.STATE] = stateObj;
      }
    })

    // Initialize map
    map.enter().append("path")
      .attr("fill", function(d) {
        return color(0);
      })
      .attr("d", path)

    // Fill color according to default percentage
    map.enter().append("path")
      .attr("fill", function(d) {
        return color(dfltById[d.id]);
      })
      .attr("d", path)
      .on('click', function(d) {
        displayInfo(stateInfo[d.id])
      })

    svg.append("path")
      .datum(topojson.mesh(us, us.objects.states, function(a, b) { return a.id !== b.id; }))
      .attr("class", "states")
      .attr("d", path)
  }
  
  // Vintage filter drop-down
  d3.select("#vintagediv")
    .append("select")
    .attr("id", "vintageselector")
    .attr("class", "selector")
    .selectAll("option")
		.data(d3.map(dflt, function(d){return d.vintage_filter;}).keys())
		.enter()
    .append("option")
		.text(function(d) { return d; })

	// Function to update year filter selector after changing vintage filter
	function updateYearSelector() {
		d3.select("#yearselector").remove()
		d3.select("#yeardiv")
		.append("select")
		.attr("id", "yearselector")
		.attr("class", "selector")
		.selectAll("option")
		.data(d3.map(dflt, function(d){
			// Handle special case for 1999-2017
			if (vintage === "1999-2017") {
				return "1999-2017";
			}

			// Only allow year filters later than the selected vintage
			if (vintage == "" ) {
				if (d.year_filter == '1999-2017' || d.year_filter.split("-").length == 1)
					return d.year_filter;
			}
			else if (+(d.year_filter.split("-")[0]) >= +vintage.split("-")[0]) {
				if (d.year_filter.split("-").length <= 1) {
					return d.year_filter;
				}
				else {
					// Only return multi-year filter that starts with selected vintage
					if (d.year_filter.split("-")[0] == +vintage.split("-")[0])
						return d.year_filter;
				}			
			}

			return vintage;
		})
		.keys())
		.enter()
		.append("option")
		.text(function(d) {
			return d;
		})

		d3.select("#yearselector")
    .on("change", function() {
			year = this.value;
			removeInfo();
      updateMap();
    })
	}

	updateYearSelector();
		
	d3.select("#yearselector")
		.on("change", function() {
			year = this.value;
			removeInfo();
			updateMap();
		})
  
  // FICO filter drop-down
  d3.select("#ficodiv")
    .append("select")
    .attr("id", "ficoselector")
    .attr("class", "selector")
    .selectAll("option")
    .data(d3.map(dflt, function(d){return d.fico_filter;}).keys())
		.enter()
    .append("option")
    .text(function(d) { return d; })

  // LTV filter drop-down
  d3.select("#ltvdiv")
    .append("select")
    .attr("id", "ltvselector")
    .attr("class", "selector")
    .selectAll("option")
		.data(d3.map(dflt, function(d){return d.ltv_filter;}).keys())
		.enter()
    .append("option")
    .text(function(d) { return d; })
  
	d3.select("#vintageselector")
    .on("change", function() {
			vintage = this.value;
			removeInfo();

			// Update year filter dropdown
			year = this.value;
			updateYearSelector()

			updateMap();
    })

  d3.select("#ficoselector")
    .on("change", function() {
			fico = this.value;
			removeInfo();
      updateMap();
    })

  d3.select("#ltvselector")
    .on("change", function() {
			ltv = this.value
			removeInfo();
      updateMap();
    })

  updateMap()
};
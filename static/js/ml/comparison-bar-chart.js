var ComparisonBarChart = {
    draw: function (id, data, options) {
        var cfg = {
            width: 0,
            height: 0,
            margin: {},
            color: d3.scaleOrdinal(d3.schemeCategory20),
        };

        console.log(data[0]);

        if ('undefined' !== typeof options) {
            for (var i in options) {
                if ('undefined' !== typeof options[i]) {
                    cfg[i] = options[i];
                }
            }
        }

        var svg = d3.select(id);
        var chart = svg.append("g")
            .classed("display", true)
            .attr("transform", "translate("+ cfg.margin.left +","+ cfg.margin.top +")"); // move chart to implement margin

        //----------------------------------

        function drawAxis(params){
            if(params.initialize === true) {
                // Draw the gridline and axis
                this.append("g")
                    .call(params.gridline.x)
                    .classed("gridline", true)
                    .attr("transform", "translate(0,0)");
            }

            // draw x axis
            this.append("g")						// append <g> to draw xAxis
                .classed("x axis", true)		// set class x axis
                .attr("transform", "translate("+ 0 +","+ cfg.height +")")	// move position
                .call(params.axis.x)			// draw
                .classed("x-axis-label",true);	// used for targeting x-axis-label and only update the label

            // draw y axis
            this.append("g")						// append <g> to draw yAxis
                .classed("y axis", true)		// set class y axis
                .attr("transform", "translate(0,0)")	// move position
                .call(params.axis.y)							// draw
                .classed("y-axis-label",true);

            // draw x axis label
            this.select(".x.axis")
                .append("text")
                .attr("x",0)
                .attr("y",0)
                .style("text-anchor","middle")
                .attr("transform", "translate("+ cfg.width/2 +","+ 40 +")")
                .text("Accuracy");

            // draw y axis label
            this.select(".y.axis")
                .append("text")
                .attr("x",0)
                .attr("y",0)
                .style("text-anchor","middle")
                .attr("transform", "translate("+ -50 +","+ cfg.height/2 +") rotate(-90)")
                .text("Alogrithm");
        }

        function plot(params){
            var a = this.selectAll(".x.axis.x-axis-label");
            this.selectAll(".x.axis.x-axis-label")
                .data(params.data)
                .remove();
            this.selectAll(".y.axis.y-axis-label")
                .data(params.data)
                .remove();

            //TODO: reset domain, when the data is updated, It need to update the data of domain
            params.scale.x.domain([0, 100]);
            params.scale.y.domain(params.data.map(function(entry){	// map allow you return a new array from your function pass in
                return Object.keys(entry);
            }));

            drawAxis.call(this, params);

            // TODO:enter() phase: data bind with element
            // TODO:In this enter phase, only need to append <rect class="bar"> no need to add any bar
            this.selectAll(".bar") 		// prepare to binding data
                .data(params.data)
                .enter()              			// Set Enter Phase: let D3 know this is first time binding data
                .append("rect")
                .classed("bar", true); 			// let future selection be able to select all bars, classed can prevent replacement from add new class

            this.selectAll(".bar-label")
                .data(params.data)
                .enter()
                .append("text")
                .classed("bar-label", true);

            // TODO:update() phase: the binded element update with change of data
            // TODO:In this update phase, update all bars
            this.selectAll(".bar")
                .attr("x", 0)								// set x position of bar
                .attr("y", function(d,i){		// set y position of bar
                    return params.scale.y(Object.keys(d));							// scaling y value
                })
                .attr("width", function(d,i){ // d: data to bind with currect element, i: index of data
                    return params.scale.x(Object.values(d)[0].accuracy);					// scaling x value
                })
                .attr("height",function(){
                    return params.scale.y.bandwidth()-1;
                })
                .style("fill", function(d,i){
                    return cfg.color(i);
                });

            this.selectAll(".bar-label")
                .attr("x",function(d,i){
                    return params.scale.x(Object.values(d)[0].accuracy);
                })
                .attr("dx", -4)
                .attr("y", function(d,i){		// set y position of bar
                    return params.scale.y(Object.keys(d));							// scaling y value
                })
                .attr("dy",function(d,i){		// allow to adjust the y position
                    return params.scale.y.bandwidth()/2 + 6;
                })
                .text(function(d,i){
                    return  Object.values(d)[0].accuracy;
                });

            // TODO:exit() phase: remove unbind element
            // TODO:remove element which does not have corresponding data
            this.selectAll(".bar")
                .data(params.data)
                .exit()
                .remove();

            this.selectAll(".bar-label")
                .data(params.data)
                .exit()
                .remove();

        }

        function update_accuracy_chart_params(data, is_initialize){
            var x = d3.scaleLinear() 	// set domain
                .domain([0, d3.max(data, function(d){	// largest and smallest value
                    return Object.values(d)[0].accuracy;
                })])
                .range([0,cfg.width]);					// inplement domain from range of 0 to width

            var y = d3.scaleBand() 	// set domain as ordinal scale
                .domain(data.map(function(entry){	// map allow you return a new array from your function pass in
                    return Object.keys(entry);
                }))
                .range([0,cfg.height]);					// use rangeBand to process discrete value

            var xAxis = d3.axisBottom()
                .scale(x);

            var yAxis = d3.axisLeft()
                .scale(y);

            var xGridlines = d3.axisBottom()
                .scale(x)
                .tickSize(cfg.height,0,0)
                .tickFormat(""); // hidden all labels

            return {
                data:data,
                axis:{
                    x: xAxis,
                    y: yAxis
                },
                scale:{
                    x: x,
                    y: y
                },
                gridline: {
                    x: xGridlines
                },
                initialize: is_initialize
            };
        }

        var params = update_accuracy_chart_params(data, true);
        plot.call(chart, params);

    }};
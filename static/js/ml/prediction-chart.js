$(function(){

        //define chart margins
        var svg = d3.select("#prediction_chart"),
            margin = {top: 50, right: 10, bottom: 10, left: 80},
            width = svg.attr("width") - margin.left - margin.right,
            height = svg.attr("height") - margin.top - margin.bottom,
            g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        var x = d3.scaleLinear().rangeRound([0, width]),
            y = d3.scaleBand().rangeRound([height, 0]).padding(0.2);

        var current_year = 2017;

        var color = d3.scaleOrdinal(["#F95017", "#66F917", "#F9DA17", "#17F9BB", "#1770F9", "#4417F9", "#F917E1"]);

        var build_bar_chart = function (csv_data) {
            var group_data = d3.nest()
                .key(function (d) {
                    return d.part_id;
                })
                .rollup(function (v) {
                    var start_year = d3.min(v, function (d) {
                        return d.part_year;
                    });

                    var last_failure_year = d3.max(v, function (d) {
                        return d.failure_year;
                    });

                    //console.log("v: "+JSON.stringify(v));

                    return {
                        part_id: v[0].part_id,
                        //len: v.length,
                        start_year: start_year,
                        last_failure_year: last_failure_year,
                        details: v
                    };
                })
                .entries(csv_data);


            //console.log(JSON.stringify(group_data));

            var data = [];
            for (i = 0; i < group_data.length; i++) {
                data.push(group_data[i].value);
            }

            //console.log(JSON.stringify(data));

            //sort data
            data = data.sort(function (a, b) {
                return parseInt(b.part_id) - parseInt(a.part_id);
            });

            var min_year = d3.min(data, function (d) {
                return d.start_year;
            });

            var max_year = d3.max(data, function (d) {
                return current_year+1;// d.last_failure_year;
            });

            var year_range = max_year - min_year;

            console.log("year_range: " + max_year+ ","+ min_year);

            //define domains based on data
            x.domain([d3.min(data, function (d) {
                return d.start_year;
            }), d3.max(data, function (d) {
                return d.last_failure_year;
            })]);
            y.domain(data.map(function (d) {
                return d.part_id;
            }));

            g.selectAll('*').remove();
            //append x axis to svg
            g.append("g")
                .attr("class", "x-axis")
                .attr("transform", "translate(0," + 0 + ")")
                .call(d3.axisTop(x))
                .append("text")
                .attr("y", -30)
                .attr("x", 650)
                .attr("dy", "0.5em")
                .style("fill", "black")
                .text("Years");

            //append y axis to svg
            g.append("g")
                .attr("class", "y-axis")
                .call(d3.axisLeft(y+""));

            //append rects to svg based on data
            g.selectAll(".bar")
                .data(data)
                .enter()
                .append("rect")
                .attr("class", "bar")
                .attr("x", function (d) {
                    return x(d.start_year);
                })
                .attr("y", function (d) {
                    return y(d.part_id);
                })
                .attr("height", y.bandwidth())
                .attr("width", function (d) {
                    return (current_year - d.start_year) * (width / year_range);
                })
                .style("fill", "#CDC7C5");

            // Define the div for the tooltip
            var div = d3.select("body").append("div")
                .attr("class", "tooltip")
                .style("opacity", 0);


            for (var i = 0; i < group_data.length; i++) {
                var item = group_data[i];
                //console.log("details: "+ JSON.stringify(item));


                var detail_data = item.value.details;

                g.selectAll(".gg" + item.key)
                    .data(detail_data)
                    .enter()
                    .append("rect")
                    .attr("class", "gg" + item.key)
                    .attr("x", function (d) {
                        return x(d.failure_year);
                    })
                    .attr("y", function (d) {
                        return y(d.part_id);
                    })
                    .attr("height", y.bandwidth())
                    .attr("width", function (d) {
                        return 10;
                    })
                    .style("fill", function (d) {
                        return color(d.material);
                    })
                    .on("mouseover", function (d) {
                        div.transition()
                            .duration(200)
                            .style("opacity", .99);

                        div.html("failure year: " + d.failure_year + "<br/>" + "diameter: " + d.diameter + "<br/>" + "length: " + d.length + "<br/>")
                            .style("left", (d3.event.pageX) + "px")
                            .style("top", (d3.event.pageY + 5) + "px");
                    })
                    .on("mouseout", function (d) {
                        div.transition()
                            .duration(500)
                            .style("opacity", 0);
                    });
            }


            var key = "_current_year";
            g.selectAll(".gg" + key)
                .data(detail_data)
                .enter()
                .append("rect")
                .attr("class", "gg" + key)
                .attr("x", function (d) {
                    return x(current_year);
                })
                .attr("y", function (d) {
                    return 1;
                })
                .attr("height", height)
                .attr("width", 5)
                .style("fill", function (d) {
                    return "#FE7D0C";
                });


            //append source data to svg
            var source = svg.append("g")
                .attr("class", "source");

            source.append("text")
                .attr("x", 10)
                .attr("y", 480)
                .attr("text-anchor", "left")
                .style("font", "16px sans-serif")
                .text("Created By P04B");

        };



        $.ajax({
            method: "GET",
            url: '/api/ml/prediction-data/?format=json',
            success: function (data) {
                build_bar_chart(data);
            }
        });

});

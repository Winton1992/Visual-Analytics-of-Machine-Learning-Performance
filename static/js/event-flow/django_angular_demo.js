angular.module('app', [])
    .controller('EventFlowController', ['$scope', '$http', function ($scope, $http) {

        var self = $scope;
        self.ms = [];

        self.filter_material = function (m) {
            console.log("filter: "+ m);
        };

        //define chart margins
        var svg = d3.select("#event_chart"),
            margin = {top: 100, right: 50, bottom: 40, left: 80},
            width = svg.attr("width") - margin.left - margin.right,
            height = svg.attr("height") - margin.top - margin.bottom,
            g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        var svg2 = d3.select("#pie_chart"),
            width2 = +svg2.attr("width"),
            height2 = +svg2.attr("height"),
            radius = Math.min(width2, height2) / 2,
            g2 = svg2.append("g").attr("transform", "translate(" + width2 / 2 + "," + height2 / 2 + ")");


        //define scales
        var x = d3.scaleLinear().rangeRound([0, width]),
            y = d3.scaleBand().rangeRound([height, 0]).padding(0.2);


        var color = d3.scaleOrdinal(["#F95017", "#66F917", "#F9DA17", "#17F9BB", "#1770F9", "#4417F9", "#F917E1"]);

        var pie = d3.pie()
            .sort(null)
            .value(function (d) {
                return d.value;
            });

        var path = d3.arc()
            .outerRadius(radius - 10)
            .innerRadius(0);

        var label = d3.arc()
            .outerRadius(radius - 40)
            .innerRadius(radius - 40);



        $http({
            method: 'GET',
            url: '/api/rawdata/event-flow-data/?format=json'
        }).then(function successCallback(r) {

            var csv_data = r.data;

            var groupbymaterial = d3.nest()
                .key(function (d) {
                    return d.material;
                })
                .rollup(function (v) {
                    return v.length / csv_data.length;
                })
                .entries(csv_data);

            groupbymaterial.forEach(function (d) {
                // console.log("m: "+d.key+","+d.value);
            });


            //  console.log("groupbymaterial: " + groupbymaterial);

            var arc = g2.selectAll(".arc")
                .data(pie(groupbymaterial))
                .enter().append("g")
                .attr("class", "arc");

            arc.append("path")
                .attr("d", path)
                .attr("fill", function (d) {
                    return color(d.data.key);
                });

            arc.append("text")
                .attr("transform", function (d) {
                    return "translate(" + label.centroid(d) + ")";
                })
                .attr("dy", "0.35em")
                .text(function (d) {
                    return Math.floor(d.data.value * 100) + " %";
                });


            var materials = d3.map(csv_data, function (d) {
                return d.material;
            }).keys();
            //var colors = ["#F95017", "#66F917", "#F9DA17", "#17F9BB", "#1770F9", "#4417F9", "#F917E1"];

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

            data = [];
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
                return d.last_failure_year;
            });

            var year_range = max_year - min_year;

            console.log("year_range: " + year_range);

            //define domains based on data
            x.domain([d3.min(data, function (d) {
                return d.start_year;
            }), d3.max(data, function (d) {
                return d.last_failure_year;
            })]);
            y.domain(data.map(function (d) {
                return d.part_id;
            }));

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
                .call(d3.axisLeft(y));

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
                    return (d.last_failure_year - d.start_year) * (width / year_range);
                })
                .style("fill", "#CDC7C5");

            // Define the div for the tooltip
            var div = d3.select("body").append("div")
                .attr("class", "tooltip")
                .style("opacity", 0);


            for (i = 0; i < group_data.length; i++) {
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

            materials.forEach(function (item) {
                self.ms.push({"color": color(item), "text": item});

            });

            //$scope.ms = msx;
            console.log("self.ms: " + JSON.stringify(self.ms));

        }); //end json

        //define chart title to svg
        var title = svg.append("g")
            .attr("class", "title");
        title.append("text")
            .attr("x", (width / 1.5))
            .attr("y", 40)
            .attr("text-anchor", "middle")
            .style("font", "20px sans-serif")
            .text("Event-flow Chart Testing");

        //append source data to svg
        var source = svg.append("g")
            .attr("class", "source");

        source.append("text")
            .attr("x", 10)
            .attr("y", 480)
            .attr("text-anchor", "left")
            .style("font", "16px sans-serif")
            .text("Created By P04B");


        // var self = $scope;
        // $scope.ms = [{"color": "#F95017", "text": "A"}, {"color": "#66F917", "text": "B"}, {
        //     "color": "#F9DA17",
        //     "text": "C"
        // }, {"color": "#17F9BB", "text": "D"}, {"color": "#1770F9", "text": "E"}];
        //
        // console.log("materials: " + JSON.stringify(self.ms));


    }]);
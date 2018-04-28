angular.module('app', ['ui.bootstrap'])
    .controller('EventFlowController', ['$scope', '$http', function ($scope, $http) {

        var self = $scope;
        self.all_materials = [];
        self.selected_materials = [];
        self.partid = '';
        self.page = {current: 1, size: 50, total: 0, count: 10};

        //define chart margins
        var svg = d3.select("#event_chart"),
            margin = {top: 50, right: 10, bottom: 10, left: 80},
            width = svg.attr("width") - margin.left - margin.right,
            height = svg.attr("height") - margin.top - margin.bottom,
            g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        var margin_padding = 0;

        var svg2 = d3.select("#pie_chart"),
            width2 = +svg2.attr("width"),
            height2 = +svg2.attr("height"),
            radius = Math.min(width2, height2) / 2,
            g2 = svg2.append("g").attr("transform", "translate(" + width2 / 2 + "," + height2 / 2 + ")");

        var event_width = 10;
        var offest_width = width - event_width;

        //define scales
        var x = d3.scaleLinear().rangeRound([0, offest_width]);
        var y = d3.scaleBand().rangeRound([height, 0]).padding(0.2);
        var x_f = d3.scaleLinear().rangeRound([0, width]);


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

        var build_bar_chart = function (csv_data, highlight_id) {
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
                    return y(d.part_id) - margin_padding;
                })
                .attr("height", y.bandwidth())
                .attr("width", function (d) {
                    return (max_year - d.start_year) * (offest_width / year_range) + event_width;
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
                        return y(d.part_id) - margin_padding;
                    })
                    .attr("height", y.bandwidth())
                    .attr("width", function (d) {
                        return event_width;
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

            if (highlight_id) {
                console.log("highlight: " + highlight_id);
                g.selectAll(".gg_highlight")
                    .data([{"partid": highlight_id}])
                    .enter()
                    .append("rect")
                    .attr("class", "gg_highlight")
                    .attr("x", 0)
                    .attr("y", function (d) {
                        return y(highlight_id) - margin_padding;
                    })
                    .attr("height", y.bandwidth())
                    .attr("width", width)
                    .style("stroke", '#ff8c00')
                    .style("stroke-width", '3')
                    .style("fill", 'transparent');
            }


            //append source data to svg
            var source = svg.append("g")
                .attr("class", "source");


        };

        var build_pie_chart = function (csv_data) {
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


            g2.selectAll('*').remove();
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

        };

        var build_materials_filter = function (csv_data) {
            var materials = d3.map(csv_data, function (d) {
                return d.material;
            }).keys();

            self.all_materials = [];

            materials.forEach(function (item) {
                self.all_materials.push({"color": color(item), "text": item});
            });

            console.log("self.all_materials: " + JSON.stringify(self.all_materials));
        };

        self.filter_material = function (m) {
            console.log("material:" + m);
            var s = new Date().getTime();

            var filter_materials = [];

            self.all_materials.forEach(function (material) {
                if (material.checked) {
                    filter_materials.push(material.text);
                }
            });

            console.log("filter_materials: " + JSON.stringify(filter_materials));

            var filter_data = [];
            self.csv_data.forEach(function (x) {
                filter_materials.forEach(function (material) {
                    if (x.material == material) {
                        filter_data.push(x);
                    }
                });
            });

            //console.log("filter_data: "+JSON.stringify(filter_data));

            //update_bar_chart(filter_data);
            build_bar_chart(filter_data);

            elapsed = new Date().getTime() - s;
            console.log("filter material (s): " + elapsed / 1000);

        };

        self.filter_partid = function (partid) {

            var s = new Date().getTime();

            build_bar_chart(self.csv_data, partid);

            elapsed = new Date().getTime() - s;
            console.log("filter partid (s): " + elapsed / 1000);

        };

        self.pageChanged = function () {
            console.log("page: ", self.page.current);

            var start = new Date().getTime();
            var begin = new Date().getTime();

            $http({
                method: 'GET',
                url: '/api/rawdata/event-flow-data/?format=json&page=' + self.page.current + '&size=' + self.page.size
            }).then(function successCallback(r) {
                self.page.total = r.data.total;
                console.log('r.data.total: ', r.data.total);
                var csv_data = r.data.items;
                self.csv_data = csv_data;

                var elapsed = new Date().getTime() - start;
                console.log("read data (s): " + elapsed / 1000);
                start = new Date().getTime();

                build_bar_chart(csv_data);

                elapsed = new Date().getTime() - start;
                console.log("bar chart (s): " + elapsed / 1000);
                start = new Date().getTime();

                build_pie_chart(csv_data);

                elapsed = new Date().getTime() - start;
                console.log("pie chart (s): " + elapsed / 1000);
                start = new Date().getTime();

                build_materials_filter(csv_data);

                elapsed = new Date().getTime() - begin;
                console.log("total (s): " + elapsed / 1000);

                //self.filter_material ('A');

            }); //end json
        };

        self.pageChanged();

    }]);
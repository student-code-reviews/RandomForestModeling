function showTalk(evt){
    evt.preventDefault();
 
    const selectedId1 = $('#ted_talk1').val();
    const selectedId2 = $('#ted_talk2').val();
    const url = `/compare/${selectedId1}/${selectedId2}`;

    $.get(url, (data) => {
        $('#talk_name1').text(data.talk_name1);
        $('#talk_name2').text(data.talk_name2);
        $('#comments1').text(data.num_comments1);
        $('#comments2').text(data.num_comments2);
        $('#views1').text(data.num_views1);
        $('#views2').text(data.num_views2);
        $('#duration1').text(data.duration1);
        $('#duration2').text(data.duration2);
        console.log(data.rating_list1);
        // myvar = '{{data.rating_dict1|tojson}}';
        const rating1 = data.rating_list1;
        const rating2 = data.rating_list2;




        document.querySelector("#Area1").innerHTML = "";
        document.querySelector("#Area2").innerHTML = "";
        const margin = {top: 20, right: 20, bottom: 50, left: 40},
            width = 400 - margin.left - margin.right,
            height = 300 - margin.top - margin.bottom;
        let x = d3.scale.ordinal()
                .domain(rating1.map(function(d) { return d.name; }))
                .rangeRoundBands([0, width], .1);
        let y = d3.scaleLinear()
                .domain([0, d3.max(rating1, function(d) { return d.count; })])
                .range([height, 0]);

        var yAxis = d3.axisLeft()
            .scale(y);
        
        var xAxis = d3.axisBottom()
            .scale(x)
            .tickSize(0);

        let svg = d3.select("#Area1").append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
          .append("g")
            .attr("transform", 
                  "translate(" + margin.left + "," + margin.top + ")");

        svg.selectAll("whatever")
            .data(rating1)
            .enter().append("rect")
            .style("fill", "steelblue")
            .attr("x", function(d) { return x(d.name); })
            .attr("width", x.rangeBand())
            .attr("y", function(d) { return y(d.count); })
            .attr("height", function(d) { return height - y(d.count); });
        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis)
            .selectAll("text")
                .style("text-anchor", "end")
                .attr("transform", function(d) {
                    return "rotate(-45)" 
                    });
        svg.append("g")
            .attr("class", "y axis")
            .call(yAxis)
          .append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", 6)
            .attr("dy", ".71em")
            .style("text-anchor", "end")
            .text("Count");
        svg.append("text")
            .attr("transform", "translate(100,0)")
            .attr("x", 0)
            .attr("y", 0)
            .attr("font-size", "14px")
            .text(data.talk_name1)

        //2nd graph
        let x2 = d3.scale.ordinal()
                .domain(rating2.map(function(d) { return d.name; }))
                .rangeRoundBands([0, width], .1);
        let y2 = d3.scaleLinear()
                .domain([0, d3.max(rating2, function(d) { return d.count; })])
                .range([height, 0]);

        var yAxis2 = d3.axisLeft()
            .scale(y2);
        
        var xAxis2 = d3.axisBottom()
            .scale(x2)
            .tickSize(0);

        let svg2 = d3.select("#Area2").append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
          .append("g")
            .attr("transform", 
                  "translate(" + margin.left + "," + margin.top + ")");

        svg2.selectAll("whatever")
            .data(rating2)
            .enter().append("rect")
            .style("fill", "steelblue")
            .attr("x", function(d) { return x(d.name); })
            .attr("width", x.rangeBand())
            .attr("y", function(d) { return y(d.count); })
            .attr("height", function(d) { return height - y(d.count); });
        svg2.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis2)
            .selectAll("text")
                .style("text-anchor", "end")
                .attr("transform", function(d) {
                    return "rotate(-45)" 
                    });
        svg2.append("g")
            .attr("class", "y axis")
            .call(yAxis2)
          .append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", 6)
            .attr("dy", ".71em")
            .style("text-anchor", "end")
            .text("Count");
        svg2.append("text")
            .attr("transform", "translate(100,0)")
            .attr("x", 0)
            .attr("y", 0)
            .attr("font-size", "14px")
            .text(data.talk_name2)

    });
}

$("#get-talks").on('submit', showTalk);


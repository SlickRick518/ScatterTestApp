$().ready(function (){
    var circleData = [];
    var pressureData = [];

    //grab test id from the query string
    var fullHeight = $('#image-container').outerHeight();
    var fullWidth  = $('#image-container').outerWidth();
    var margin = {
        top: fullHeight * 0.055,
        right: fullWidth * 0.05,
        bottom: fullWidth * 0.05,
        left: fullWidth * 0.05
    };
    $('#div-controls').hide();

    var width = fullWidth - margin.left - margin.right,
    height = fullHeight - margin.top - margin.bottom;
    //need to fix positioning - this is ALWAYS a problem for me
    var params = new URLSearchParams(window.location.search);
    var testID = params.get('id');
    var svg = d3.select("#svg")
    .attr("preserveAspectRatio", "xMinYMin meet")
    .attr("width", window.outerWidth)
    .attr("height", window.outerHeight);
    //.attr("transform", "translate(" + margin.left + ")");

    var xScale = 0;
    var yScale = 0;
    var counter = 0; //will help us figure out where we are

    $.ajax({
        url: "/data/get_test_data_json",
        data: {id: testID},
        type: 'GET',
        success: function(response) {
            console.log(response)
            circleData = response.CircleData;
            rawPressures = response.PressureData;
            for(i = 0; i < rawPressures.length; i++)
            {
                var currentGroup = [];
                var currentPressures = rawPressures[i];
                for(j = 0; j < currentPressures.length; j++)
                {
                    currentGroup.push($.parseJSON(currentPressures[j].replace(/'/g, '"')));
                }
                pressureData.push(currentGroup);
            }
            
            //load in the test taken
            $.ajax({
                //eventually make this url dynamic
                url: "/data/download_as_json/AlphabetTest_fixed.json",
                type: 'GET',
                success: function(response) {
                    var testData = $.parseJSON($.trim(response));
                    //render the test
                    var symbols = testData.symbols;
                    
                    //scale everything properly - 
                    //hardcoded to dimensions of the test, based upon the last value in the json
                    
                    xScale = d3.scaleLinear().domain([0,1100]).range([0,window.outerWidth]).nice();
                    yScale = d3.scaleLinear().domain([0,800]).range([0,window.outerHeight]).nice();

                    var text = svg.selectAll("text")
                    .data(symbols)
                    .enter()
                    .append("text");
                    // - 75 for swift offset
                    var textLabels = text
                         .attr("x", function(d) { return xScale(d.x); })
                         .attr("y", function(d) { return yScale(d.y); })
                         .text( function (d) { return d.name; })
                         .attr("font-family", "sans-serif")
                         .attr("font-size", "16px")
                         .attr("fill", "black");
                    //and now make all the controls visible
                    $('#div-controls').show();
                }
            });
        }
    });

    //button functionality
    $('#btn-start').on('click', function(){

        for(var i = 0; i < circleData.length; i++)
        {
            counter++;
            var line = d3.line()
            //figure out offset 
            .x(function(d) { return xScale(d.x); })
            .y(function(d) { return yScale(d.y); })
            .curve(d3.curveMonotoneX);

            svg.append('path').datum(pressureData[i])
            .attr('d', line).attr("stroke", "red").attr("fill","none")
            .attr('stroke-dasharray', '385 385')
            .attr('stroke-dashoffset', 385)
            .transition().duration(circleData[i].total_time * 1000)
            .attr('stroke-dashoffset',0);
        }
    });
});
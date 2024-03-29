$().ready(function (){
    //CAVEAT: needs to be on a monitor at least as big as the iPad's resolution to show good results
    //TODO: build voronoi incrementally - would be nice but not necessary
    var circleData = [];
    var pressureData = [];
    var testFrame = [];
    //for voronoi calculations
    var compressedPressureData = [];
    var delaunay = 0;
    var xScale = 0;
    var yScale = 0;
    var counter = 0; //will help us figure out where we are
    let speedFactor = 1000; //regular speed
    let tooltipRadius = 2;
    //width and height are flipped because the iPad's in landscape mode
    let width = 1112;
    let height = 834;
    var isPaused = false;
    
    //grab test id from the query string
    $('#div-controls').hide();

    //need to fix positioning - this is ALWAYS a problem for me
    var params = new URLSearchParams(window.location.search);
    var testID = params.get('id');
    var svg = d3.select("#svg")
    .attr("preserveAspectRatio", "xMinYMin meet")
    .attr("width", width)
    .attr("height", height);

    //shows us where we're hovering over
    var focus = svg.append("g")
    .attr("transform", "translate(-100,-100)")
    .attr("class", "focus").style('opacity', 0);

    focus.append("circle")
    .attr("r", 3.5);

    $.ajax({
        url: "/data/get_test_data_json",
        data: {id: testID},
        type: 'GET',
        success: function(response) {
            testFrame = response;
            circleData = response.CircleData;
            rawPressures = response.PressureData;
            /*console.log(testFrame);
            console.log(circleData);
            */
            for(i = 0; i < rawPressures.length; i++)
            {
                var currentGroup = [];
                var currentPressures = rawPressures[i];
                for(j = 0; j < currentPressures.length; j++)
                {
                    var currentPressure = $.parseJSON(currentPressures[j].replace(/'/g, '"'));
                    //need to do this because python dicts save strangely inside json files
                    currentGroup.push(currentPressure);
                    compressedPressureData.push(currentPressure);
                    
                }
                let mean = d3.mean(currentGroup, function(d) { return d.x;});
                let deviation = d3.deviation(currentGroup, function(d) { return d.x;});
                //filter out outliers - inefficient but WHATEVER
                for(var k = 0; k < currentGroup.length; k++)
                {
                    if(currentGroup[k].x > mean + 2 * deviation)
                    {
                        currentGroup.splice(k,1);
                    }
                }
                pressureData.push(currentGroup);
            }
            var url = "/data/download_as_json/" + testFrame.TestName;
            //load in the test taken
            $.ajax({
                //eventually make this url dynamic
                url: url,
                type: 'GET',
                success: function(response) {
                    var testData = $.parseJSON($.trim(response));
                    //render the test
                    var symbols = testData.symbols;
                    
                    //scale everything properly - 
                    //based upon the last value in the json
                    // x also stretches
                    xScale = d3.scaleIdentity().domain([0, d3.max(symbols, function(d) {return d.x})]).range([0,width]);
                    yScale = d3.scaleIdentity().domain([0, d3.max(symbols, function(d) {return d.y})]).range([0,height]);
                    var text = svg.selectAll("text")
                    .data(symbols)
                    .enter()
                    .append("text");
                    var textLabels = text
                         .attr("x", function(d) { return xScale(d.x); })
                         .attr("y", function(d) { return yScale(d.y); })
                         .text( function (d) { return d.name; })
                         .attr("font-family", "Arial")
                         .attr("font-size", "16px")
                         .attr("fill", "black");
                    //and now make all the controls visible
                    $('#div-controls').show();
                }
            });
        }
    });

    //button functionality
    $('#btn-start').on('click', function()
    {
        counter = 0;
        drawCircle(counter, true);
    });

    $('#btn-rewind').on('click', function () {
        isPaused = true;
        //get current one by id and remove
        $('#btn-pause').text("Continue");
        svg.selectAll("*").interrupt();
        svg.select("#circle-" + circleData[counter].CircleID).remove();
        counter--;
    });
    $('#btn-fastforward').on('click', function () 
    {
        isPaused = true;
        $('#btn-pause').text("Continue");
        svg.selectAll("*").interrupt();
        drawCircle(counter, false);
        counter++;
    });

    $('#btn-pause').on('click', function() {
        if($('#btn-pause').text() === "Pause")
        {
            isPaused = true;
            svg.selectAll("*").interrupt();
            $('#btn-pause').text("Continue");
        }
        else
        {
            isPaused = false;
            drawCircle(counter, true);
            $('#btn-pause').text("Pause");
        }
    })

    $('#btn-reset').on('click', function() {
        counter = 0;
        delaunay = 0;
        d3.select('#moving_tooltip').style('opacity', 0);
        d3.select('#held_tooltip').style('opacity', 0);
        svg.selectAll("*").interrupt();
        svg.selectAll('path').remove();
    });

    $('#btn-showAll').on('click', function() {
        for(var i = 0; i < circleData.length; i++)
        {
            drawCircle(i,false);
        }
        buildVoronoi();
    });

    svg.on('mousemove', function() {
        if(delaunay != 0)
        {
            var mouseX = d3.mouse(this)[0];//d3.event.layerX || d3.event.offsetX;
            var mouseY = d3.mouse(this)[1];//d3.event.layerY || d3.event.offsetY;

            let pointIndex = delaunay.find(mouseX,mouseY, tooltipRadius);
            if(pointIndex)
            {
                d3.select('#moving_tooltip')
                .style('opacity', 1)
                .style('color', 'black')
                .style('top', d3.event.pageY + 15 + 'px')
                .style('left', d3.event.pageX + 15 + 'px')
                .html('X: ' + compressedPressureData[pointIndex].x + '<br>' + 
                      'Y: ' + compressedPressureData[pointIndex].y + '<br>'  +
                      'Pressure: ' + compressedPressureData[pointIndex].pressure + '<br>' +
                      'Altitude: ' + compressedPressureData[pointIndex].altitude + '<br>' +
                      'Azimuth: ' + compressedPressureData[pointIndex].azimuth + '<br>');

                focus.style('opacity', 1);
                //12.5 is the magic offset number
                focus.attr("transform", "translate(" + xScale(compressedPressureData[pointIndex].x - 12.5) + "," + 
                yScale(compressedPressureData[pointIndex].y - 12.5) + ")");
            }else {
		    	d3.select('#moving_tooltip')
				.style('opacity', 0);
            }
        }

    });

    function buildVoronoi()
    {
        delaunay = d3.Delaunay.from(compressedPressureData, function(data) { return xScale(data.x)},
        function(data) { return yScale(data.y)});
    }

    function calcWait(counter)
    {
        if(counter != 0 && (counter != circleData.length - 1))
        {
            return circleData[counter+1].begin_circle - circleData[counter].end_circle;
        }
        else if(counter === circleData.length - 1)
        {
            return circleData[counter].begin_circle - circleData[counter-1].end_circle;
        }
        else
        {
            return circleData[counter].begin_circle;
        }
    }

    function simulateTest()
    {
        //gets called every time a transition ends
        counter++;
        if(!isPaused && counter < circleData.length )
        {
            setTimeout(function() {
                drawCircle(counter, true);
            }, calcWait(counter) * 1000);
            
        }
        else if(counter === circleData.length)
        {
            counter = 0;
            alert("Patient completed the test in " + testFrame.TestLength);
        }
    }

    function calcAvg(data, parameter)
    {
        //stupid and ugly can make it faster later
        var value = 0;
        switch(parameter)
        {
            case 'PRESSURE':
                for(var i = 0; i < pressureData[counter].length; i++)
                {
                    value += pressureData[counter][i].pressure;
                }
                break;
            case 'ALTITUDE':
                for(var i = 0; i < pressureData[counter].length; i++)
                {
                    value += pressureData[counter][i].altitude;
                }
                break;
            case 'AZIMUTH':
                for(var i = 0; i < pressureData[counter].length; i++)
                {
                    value += pressureData[counter][i].azimuth;
                }
                break;
        }
        return value / pressureData[counter].length;
    }

    function drawCircle(counter, isRunning)
    {
        var line = d3.line()
        //figure out offset - guessing here
        .x(function(d) { return xScale(d.x - 12.5) ; })
        .y(function(d) { return yScale(d.y - 12.5) ; });

        //this is broken 
        //lines are caused by the patient putting their palm on the device - here, I filter any points 
        //that are clearly outliers
        var currentCircle = svg.append('path').datum(pressureData[counter])
                            .attr('d', line).attr("stroke", "red").attr("fill","none")
                            .attr("id", "circle-" + circleData[counter].CircleID)
                            .attr("stroke-dasharray", "385 385").attr("stroke-dashoffset", 385).on("click", function() {
                                // -1 cause however the circle id's are in the database
                                var id = parseInt(this.id.replace( /^\D+/g, '')) - 1;
                                d3.selectAll('*').attr("stroke-width", 1);
                                d3.select(this).attr("stroke-width", 2);

                                d3.select('#held_tooltip')
                                .style('opacity', 1)
                                .style('color', 'black')
                                .html('<b>Circle ID:</b> ' + circleData[id].CircleID + '<br>' +
                                      '<b>Symbol Circled:</b> ' + circleData[id].symbol + '<br>' +
                                      '<b>Circle Began at:</b> ' + circleData[id].begin_circle + '<br>' +
                                      '<b>Circle Ended at:</b> ' + circleData[id].end_circle + '<br>' +
                                      '<b>Average Pressure:</b> ' + calcAvg(pressureData[id], 'PRESSURE') + '<br>' +
                                      '<b>Average Altitude:</b> ' + calcAvg(pressureData[id], 'ALTITUDE') + '<br>' +
                                      '<b>Average Azimuth:</b> ' + calcAvg(pressureData[id], 'AZIMUTH') + '<br>')
                            })
                            .transition().duration(circleData[counter].total_time * speedFactor)
                            .attr('stroke-dashoffset', 0)
        if(isRunning)
        {
            currentCircle.on("end", simulateTest);
        }
        if(counter === circleData.length - 1)
        {
            buildVoronoi();
        }
    }
});
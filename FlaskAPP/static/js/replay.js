$().ready(function (){
    //grab test id from the query string
    var fullHeight = $('#image-container').outerHeight();
    var fullWidth  = $('#image-container').outerWidth();
    var margin = {
        top: fullHeight * 0.055,
        right: fullWidth * 0.05,
        bottom: fullWidth * 0.05,
        left: fullWidth * 0.05
    };
    var width = fullWidth - margin.left - margin.right,
    height = fullHeight - margin.top - margin.bottom;
    //need to fix positioning - this is ALWAYS a problem for me
    var params = new URLSearchParams(window.location.search);
    var testID = params.get('id');
    var svg = d3.select("#svg")
    .attr("preserveAspectRatio", "xMinYMin meet")
    .attr("width", window.innerWidth)
    .attr("height", window.outerHeight)
    .attr("transform", "translate(" + margin.left + ")");
    $.ajax({
        url: "/data/download_as_json/AlphabetTest_fixed.json",
        type: 'GET',
        success: function(response) {
            var testData = $.parseJSON($.trim(response));
            console.log(testData);


            //render the test
            var symbols = testData.symbols;
            var text = svg.selectAll("text")
            .data(symbols)
            .enter()
            .append("text");
            // - 75 for swift offset
            var textLabels = text
                 .attr("x", function(d) { return d.x; })
                 .attr("y", function(d) { return d.y; })
                 .text( function (d) { return d.name; })
                 .attr("font-family", "sans-serif")
                 .attr("font-size", "16px")
                 .attr("fill", "black");
        }
    });
});
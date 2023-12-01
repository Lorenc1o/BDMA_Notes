// Select the SVG element and get its width and height
var width = 1000,
height = 300;

margin = {
    top: height * 0.1,
    right: width * 0.15,
    bottom: height * 0.1,
    left: width * 0.3
}

// Adjust SVG transformation to account for margins
var svg = d3.select("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// Append a title to the SVG
svg.append("text")
    .attr("x", width / 2) // Position the title in the middle of the SVG
    .attr("y", -height*0.05) // Position the title 20px from the top of the SVG
    .attr("text-anchor", "middle") // Anchor the text in the middle
    .style("font-size", "20px") // Set the font size
    .style("font-weight", "bold") // Set the font weight
    .text("Crimes per 1.000 inhabitants per category in selected provinces"); // Set the title text


// Define a color scale
var color = d3.scaleOrdinal(d3.schemeCategory10);

// Define categories
var categoriesToInclude = [
    "    1.1.-Homicidios dolosos/asesinatos", 
    "    3.1.-Agresión sexual", 
    "    3.2.-Agresión sexual con penetración", 
    "    5.1.-Hurtos", 
    "    5.2.-Robos con fuerza en las cosas", 
    "    5.3.1.-Robos con violencia en vía pública", 
    "    5.3.2.-Robos con violencia en viviendas", 
    "    5.3.3.-Robos con violencia en establecimientos", 
    "    6.2.-Contra la seguridad vial"];

var categoryTranslations = {
    "    1.1.-Homicidios dolosos/asesinatos": "Intentional Homicides/Assassinations",
    "    3.1.-Agresión sexual": "Sexual Assault",
    "    3.2.-Agresión sexual con penetración": "Sexual Assault with Penetration",
    "    5.1.-Hurtos": "Thefts",
    "    5.2.-Robos con fuerza en las cosas": "Robberies with Force",
    "    5.3.1.-Robos con violencia en vía pública": "Robberies with Violence in Public Spaces",
    "    5.3.2.-Robos con violencia en viviendas": "Robberies with Violence in Houses",
    "    5.3.3.-Robos con violencia en establecimientos": "Robberies with Violence in Establishments",
    "    6.2.-Contra la seguridad vial": "Against Road Safety"
};


categoriesToInclude.forEach(category => {
    var checkbox = document.createElement('input');
    checkbox.type = "checkbox";
    checkbox.name = "category";
    checkbox.value = category;
    checkbox.id = category;
    checkbox.checked = true;

    var label = document.createElement('label');
    label.htmlFor = category;
    label.appendChild(document.createTextNode(categoryTranslations[category]));

    var container = document.getElementById('category-selectors');
    container.appendChild(checkbox);
    container.appendChild(label);
    container.appendChild(document.createElement('br'));
});

// Load the data
d3.csv("data.csv").then((data) => {
// Parse the data
data.forEach(d => {
    d.Year = d3.timeParse("%Y")(d.Year);
    d.Amount = +d.Amount;
    d.Province = d.Place;
    d.Population = +d.Population;
});

const provinces = Array.from(new Set(data.map(d => d.Place)));
console.log("Provinces:", provinces);
// From provinces, remove: 'Total Nacional', 'En el extranjero', 'Desconocida', 'TOTAL INFRACCIONES PENALES' and 'Notas'
const provincesToRemove = ['Total Nacional', 'En el extranjero', 'Desconocida', '    TOTAL INFRACCIONES PENALES', 'Notas:'];
provincesToRemove.forEach(province => {
    const index = provinces.indexOf(province);
    if (index > -1) {
        provinces.splice(index, 1);
    }
});

initialProvinces = ['Madrid', 'Barcelona', 'Murcia']

// Create checkboxes for provinces
provinces.forEach(province => {
    var checkbox = document.createElement('input');
    checkbox.type = "checkbox";
    checkbox.name = "province";
    checkbox.value = province;
    checkbox.id = province;
    checkbox.checked = initialProvinces.includes(province);

    var label = document.createElement('label');
    label.htmlFor = province;
    label.appendChild(document.createTextNode(province));

    var container = document.getElementById('province-selectors');
    container.appendChild(checkbox);
    container.appendChild(label);
    container.appendChild(document.createElement('br'));
});

// Function to process the data
function processData(data, categoriesToInclude, provincesToInclude){
    var filteredData = data.filter(d => categoriesToInclude.includes(d["Crime Category"]) && provincesToInclude.includes(d.Place) && d.Population > 0);
    // We compute the population in the selected provinces, noticing that there can be multiple entries for the same province and year
    var populationPerYear = d3.rollup(filteredData,
        v => d3.sum(Array.from(d3.group(v, d => d.Place + d.Year.getFullYear()).values(), arr => arr[0].Population)),
        d => d.Year.getFullYear()
    );    

    // We compute the crime rate per 1000 inhabitants in the selected provinces for each year
    var aggregatedData = d3.rollup(filteredData,
        (v) => {
            // For each group (crime category and year), calculate the crime rate
            return d3.rollup(v,
                (vv) => {
                    // Calculate total crimes for the group
                    const totalCrimes = d3.sum(vv, d => d.Amount);
                    // Retrieve the population for the year of the current group
                    const year = vv[0].Year.getFullYear();
                    const population = populationPerYear.get(year);
                    // Calculate and return the crime rate per 1000 inhabitants
                    return population ? (totalCrimes / population) * 1000 : 0;
                },
                d => d.Year.getFullYear() // Group by year within each crime category
            );
        },
        d => d["Crime Category"] // Group by crime category
    );
    

    console.log("Aggregated Data:", aggregatedData);

    return aggregatedData;
}

// Function to create scales
function createScales(data) {
    var allYears = Array.from(data.values()).flatMap(map => Array.from(map.keys()));
    // Unique years
    allYears = Array.from(new Set(allYears));
    console.log("All Years Raw:", allYears); // Check the raw year values
    const xScale = d3.scaleLinear().domain(d3.extent(allYears)).range([0, width]);
    const yScale = d3.scaleLinear().domain([0, d3.max(data, ([, yearMap]) => d3.max(yearMap.values()))]).range([height, 0]);

    console.log(xScale.domain(), xScale.range());

    const line = d3.line()
    .x(d => xScale(d.year))
    .y(d => yScale(d.amount));

    const xAxis = d3.axisBottom(xScale); // Format ticks to show years
    const yAxis = d3.axisLeft(yScale);

    return {xScale, yScale, xAxis, yAxis, line};
}

// Function to draw axes
function drawAxes(xAxis, yAxis) {
    svg.append("g")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis);

    svg.append("g")
    .call(yAxis);
}

// Function to create lines for each category
function drawCategoryLines(aggregatedData, line) {
    aggregatedData.forEach((yearMap, category) => {
    const dataArray = Array.from(yearMap, ([year, amount]) => ({ year: new Date(year), amount }));
    
    svg.append("path")
        .datum(dataArray)
        .attr("fill", "none")
        .attr("stroke", color(category))
        .attr("stroke-width", 2)
        .attr("d", line);
    });
}

function computeCrimeRateLastYearPerProvince(data, selectedCategories, selectedProvinces) {
    var lastYear = d3.max(data, d => d.Year);
    var filteredData = data.filter(d => selectedCategories.includes(d["Crime Category"]) && selectedProvinces.includes(d.Place) && d.Population > 0 && d.Year.getFullYear() == lastYear.getFullYear());
    var aggregatedData = d3.rollup(filteredData, 
        v => d3.sum(v, d => d.Amount) / d3.max(v, d => d.Population) * 1000, // Compute the crime rate per 1000 inhabitants
        d => d.Place
    );
    return aggregatedData;
}

// Function to compute the most dangerous provinces
// Returns a map with the top n provinces and their crime rate, and the rest of the provinces grouped in "Rest", with their average crime rate
function mostDangerousProvinces(crimeRatePerProvince, n=2) {
    var sortedProvinces = Array.from(crimeRatePerProvince, ([province, crimeRate]) => ({ province, crimeRate })).sort((a, b) => b.crimeRate - a.crimeRate);
    var topNProvinces = sortedProvinces.slice(0, n);
    var otherProvinces = sortedProvinces.slice(n);
    var averageCrimeRate = d3.mean(otherProvinces, d => d.crimeRate);

    // If there are no other provinces, return the top n provinces
    if (otherProvinces.length == 0) {
        return topNProvinces;
    }

    var otherProvincesMap = new Map();
    otherProvinces.forEach(d => otherProvincesMap.set(d.province, averageCrimeRate));
    topNProvinces.push({province: "Rest", crimeRate: averageCrimeRate});
    console.log("Top N Provinces:", topNProvinces);
    return topNProvinces;
}


// Function to draw the legend
function drawLegend(selectedCategories) {
    var legend = svg.selectAll(".legend")
    .data(color.domain().filter(d => selectedCategories.includes(d)))
    .enter().append("g")
    .attr("class", "legend")
    .attr("transform", (d, i) => "translate(0," + i * 20 + ")");

    legend.append("rect")
    .attr("x", -margin.left)
    .attr("width", 18)
    .attr("height", 18)
    .style("fill", color);

    legend.append("text")
    .attr("x", -margin.left + 24)
    .attr("y", 9)
    .attr("dy", ".35em")
    .style("text-anchor", "start")
    .style("font-size", "14px")
    .text(d => categoryTranslations[d]);
}

function drawStackedBarChart(data, selectedCategories, selectedProvinces) {
    var crimeRatePerProvince = computeCrimeRateLastYearPerProvince(data, selectedCategories, selectedProvinces.map(d => d.value));
    var stackedData = mostDangerousProvinces(crimeRatePerProvince, 2);

    // Now we draw a stacked bar chart with the crime rate per province (a single bar having all provinces)
    var keys = stackedData.map(d => d.province);
    console.log("Keys:", keys);
    var transformedStackedData = [{name: "crimeRate"}];
    stackedData.forEach(d => {
        transformedStackedData[0][d.province] = d.crimeRate;
    });

    console.log("Stacked Data:", transformedStackedData);

    // Stack the data in ascending order
    var stack = d3.stack().keys(keys).order(d3.stackOrderAscending).offset(d3.stackOffsetNone);

    var series = stack(transformedStackedData);

    console.log("Series:", series);

    var colors = ["#BAE3F2", "#C9F2EB", "#E6FCED"]; 

    var yScaleStacked = d3.scaleLinear()
        .domain([0, d3.max(series, d => d3.max(d, d => d[1]))])
        .range([height, 0]);

    var xScaleStacked = d3.scaleBand()
        .domain(["crimeRate"])
        .range([width, width/10*11])
        .padding(0.1);

    var color = d3.scaleOrdinal()
        .domain(keys)
        .range(colors);

    svg.append("g")
        .selectAll("g")
        .data(series)
        .enter().append("g")
            .attr("fill", d => color(d.key))
        .selectAll("rect")
        .data(d => d)
        .enter().append("rect")
            .attr("x", (d, i) => xScaleStacked("crimeRate"))
            .attr("y", d => yScaleStacked(d[1]))
            .attr("height", d => yScaleStacked(d[0]) - yScaleStacked(d[1]))
            .attr("width", xScaleStacked.bandwidth());

    svg.append("g")
    .selectAll("g")
    .data(series)
    .enter().append("g")
    .attr("transform", d => `translate(${xScaleStacked("crimeRate") + xScaleStacked.bandwidth() / 2}, ${yScaleStacked(d[0][1]) + (yScaleStacked(d[0][0]) - yScaleStacked(d[0][1])) / 2})`)
    .each(function(d) {
        d3.select(this).append("text")
            .attr("text-anchor", "middle")
            //.attr("transform", "rotate(-90)")
            .attr("dy", "-0.35em") // Adjust for spacing
            .attr("fill", "black")
            .text(d.key);

        d3.select(this).append("text")
            .attr("text-anchor", "middle")
            //.attr("transform", "rotate(-90)")
            .attr("dy", "0.7em") // Adjust for spacing
            .attr("fill", "black")
            .text((d[0][1] - d[0][0]).toFixed(2));
    });

    // Add title
    svg.append("text")
        .attr("x", width + margin.right/3)
        .attr("y", -margin.top/1.5)
        .attr("text-anchor", "middle")
        .attr("font-size", "14px")
        .attr("font-weight", "bold")
        .text("Most dangerous provinces");

    // Add subtitle
    svg.append("text")
        .attr("x", width + margin.right/3)
        .attr("y", -margin.top/1.5 + 15)
        .attr("text-anchor", "middle")
        .attr("font-size", "12px")
        .text("(Crimes per 1000 inhabitants in 2022)");
}

// Function to update the chart
function updateChart() {
    var selectedCategories = d3.selectAll("input[name='category']:checked").nodes()
    .map(d => d.value);

    var selectedProvinces = d3.selectAll("input[name='province']:checked").nodes()

    // Filter the aggregated data based on selected categories
    var filteredData = processData(data, selectedCategories, selectedProvinces.map(d => d.value));

    // Clear the existing elements
    svg.selectAll("path").remove();
    svg.selectAll(".legend").remove();
    svg.selectAll("g").remove();

    // Redraw lines and legend
    const {xScale, yScale, xAxis, yAxis, line} = createScales(filteredData);
    drawAxes(xAxis, yAxis);
    drawCategoryLines(new Map(filteredData), line);
    drawLegend(selectedCategories);  
    drawStackedBarChart(data, selectedCategories, selectedProvinces);  
}

updateChart();

d3.selectAll("input[name='category']").on("change", updateChart);
d3.selectAll("input[name='category'], input[name='province']").on("change", updateChart);

document.getElementById("select-all-categories").addEventListener("click", function() {
    document.querySelectorAll("#category-selectors input[type='checkbox']").forEach(function(checkbox) {
        checkbox.checked = true;
    });
    updateChart();
});

document.getElementById("deselect-all-categories").addEventListener("click", function() {
    document.querySelectorAll("#category-selectors input[type='checkbox']").forEach(function(checkbox) {
        checkbox.checked = false;
    });
    updateChart();
});

document.getElementById("select-all-provinces").addEventListener("click", function() {
    document.querySelectorAll("#province-selectors input[type='checkbox']").forEach(function(checkbox) {
        checkbox.checked = true;
    });
    updateChart();
});

document.getElementById("deselect-all-provinces").addEventListener("click", function() {
    document.querySelectorAll("#province-selectors input[type='checkbox']").forEach(function(checkbox) {
        checkbox.checked = false;
    });
    updateChart();
});

});
d3.csv("Motor_Vehicle_Collisions_-_Crashes_20241120.csv").then(function(data) {
    // Process data
    data.forEach(d => {
        d["CRASH_DATETIME"] = new Date(d["CRASH DATE"] + ' ' + d["CRASH TIME"]);
        d["LATITUDE"] = +d["LATITUDE"];
        d["LONGITUDE"] = +d["LONGITUDE"];
        d["NUMBER OF PERSONS INJURED"] = +d["NUMBER OF PERSONS INJURED"];
        d["NUMBER OF PERSONS KILLED"] = +d["NUMBER OF PERSONS KILLED"];
        d["NUMBER OF PEDESTRIANS INJURED"] = +d["NUMBER OF PEDESTRIANS INJURED"];
        d["NUMBER OF CYCLIST INJURED"] = +d["NUMBER OF CYCLIST INJURED"];
        d["NUMBER OF MOTORIST INJURED"] = +d["NUMBER OF MOTORIST INJURED"];
        d["NUMBER OF PEDESTRIANS KILLED"] = +d["NUMBER OF PEDESTRIANS KILLED"];
        d["NUMBER OF CYCLIST KILLED"] = +d["NUMBER OF CYCLIST KILLED"];
        d["NUMBER OF MOTORIST KILLED"] = +d["NUMBER OF MOTORIST KILLED"];
    });

    createHeatmap(data);
    createContributingFactorsChart(data);
    createInjuriesChart(data);
    createFatalitiesChart(data);
    createCollisionsOverTimeChart(data);
    createCollisionsByBoroughChart(data);
    createHourlyCollisionTrendsChart(data);
});

function createHeatmap(data) {
    let map = L.map('heatmap').setView([40.7128, -74.0060], 12);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    let heatData = data.map(d => [d.LATITUDE, d.LONGITUDE, 1]);
    L.heatLayer(heatData, {radius: 15}).addTo(map);
}

function createContributingFactorsChart(data) {
    let factors = {};
    data.forEach(d => {
        let factor = d["CONTRIBUTING FACTOR VEHICLE 1"];
        if (factor && factor !== "Unspecified") {
            factors[factor] = (factors[factor] || 0) + 1;
        }
    });

    let sortedFactors = Object.entries(factors).sort((a, b) => b[1] - a[1]).slice(0, 20);

    let chart = vegaEmbed('#contributing-factors', {
        $schema: 'https://vega.github.io/schema/vega-lite/v5.json',
        data: {values: sortedFactors.map(d => ({factor: d[0], count: d[1]}))},
        mark: 'bar',
        encoding: {
            x: {field: 'count', type: 'quantitative', title: 'Number of Occurrences'},
            y: {field: 'factor', type: 'nominal', title: 'Contributing Factor', sort: '-x'}
        },
        title: 'Top Contributing Factors to Collisions'
    });
}

function createInjuriesChart(data) {
    let injuries = {
        Pedestrians: d3.sum(data, d => d["NUMBER OF PEDESTRIANS INJURED"]),
        Cyclists: d3.sum(data, d => d["NUMBER OF CYCLIST INJURED"]),
        Motorists: d3.sum(data, d => d["NUMBER OF MOTORIST INJURED"]),
    };

    let chart = vegaEmbed('#injuries', {
        $schema: 'https://vega.github.io/schema/vega-lite/v5.json',
        data: {values: Object.keys(injuries).map(k => ({Category: k, Injuries: injuries[k]}))},
        mark: 'bar',
        encoding: {
            x: {field: 'Category', type: 'nominal'},
            y: {field: 'Injuries', type: 'quantitative'},
            color: {field: 'Category', type: 'nominal'}
        },
        title: 'Injuries by User-Groups'
    });
}

function createFatalitiesChart(data) {
    let fatalities = {
        Pedestrians: d3.sum(data, d => d["NUMBER OF PEDESTRIANS KILLED"]),
        Cyclists: d3.sum(data, d => d["NUMBER OF CYCLIST KILLED"]),
        Motorists: d3.sum(data, d => d["NUMBER OF MOTORIST KILLED"]),
    };

    let chart = vegaEmbed('#fatalities', {
        $schema: 'https://vega.github.io/schema/vega-lite/v5.json',
        data: {values: Object.keys(fatalities).map(k => ({Category: k, Fatalities: fatalities[k]}))},
        mark: 'bar',
        encoding: {
            x: {field: 'Category', type: 'nominal'},
            y: {field: 'Fatalities', type: 'quantitative'},
            color: {field: 'Category', type: 'nominal'}
        },
        title: 'Fatalities by User-Groups'
    });
}

function createCollisionsOverTimeChart(data) {
    let timeseries = d3.groups(data, d => d3.timeDay(d["CRASH_DATETIME"])).map(d => ({date: d[0], count: d[1].length}));

    let chart = vegaEmbed('#collisions-over-time', {
        $schema: 'https://vega.github.io/schema/vega-lite/v5.json',
        data: {values: timeseries},
        mark: 'line',
        encoding: {
            x: {field: 'date', type: 'temporal', title: 'Date'},
            y: {field: 'count', type: 'quantitative', title: 'Collisions'}
        },
        title: 'Daily Collisions Over Time'
    });
}

function createCollisionsByBoroughChart(data) {
    let boroughs = {};
    data.forEach(d => {
        let borough = d["BOROUGH"];
        if (borough) {
            boroughs[borough] = (boroughs[borough] || 0) + 1;
        }
    });

    let chart = vegaEmbed('#collisions-by-borough', {
        $schema: 'https://vega.github.io/schema/vega-lite/v5.json',
        data: {values: Object.keys(boroughs).map(b => ({Borough: b, Collisions: boroughs[b]}))},
        mark: 'bar',
        encoding: {
            x: {field: 'Borough', type: 'nominal'},
            y: {field: 'Collisions', type: 'quantitative'},
            color: {field: 'Borough', type: 'nominal'}
        },
        title: 'Collisions by Borough'
    });
}

function createHourlyCollisionTrendsChart(data) {
    let hourlyTrends = d3.rollup(data, v => v.length, d => d["CRASH_DATETIME"].getHours());

    let chart = vegaEmbed('#hourly-collision-trends', {
        $schema: 'https://vega.github.io/schema/vega-lite/v5.json',
        data: {values: Array.from(hourlyTrends).map(d => ({Hour: d[0], Collisions: d[1]}))},
        mark: 'line',
        encoding: {
            x: {field: 'Hour', type: 'ordinal', title: 'Hour of Day'},
            y: {field: 'Collisions', type: 'quantitative', title: 'Number of Collisions'}
        },
        title: 'Hourly Collision Trends'
    });
}

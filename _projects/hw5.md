---
name: "HW5: UFO Sightings"
tools: [Python, Altair, Vega-Lite]
description: Two visualizations of reported UFO sightings.
permalink: /hw5/
custom_js:
  - vega.min
  - vega-lite.min
  - vega-embed.min
  - justcharts
---

# UFO Sightings

## Reported Sightings by Year

<vegachart schema-url="{{ site.baseurl }}/assets/json/chart1.json" style="width: 100%"></vegachart>

This line chart shows how many UFO sightings were reported for each year in the dataset. The horizontal axis shows the year, and the vertical axis shows the number of reports. I used a line to make changes over time easy to follow. The line is blue throughout because color does not represent another variable, so a color scale is unnecessary. In Python, I extracted the year from the datetime column, converted it to a number, and grouped the records by year to count the reports. These are counts of reported sightings in this dataset, rather than confirmed UFO events.

## Reported Shapes by Country

<vegachart schema-url="{{ site.baseurl }}/assets/json/chart2.json" style="width: 100%"></vegachart>

This bar chart shows the number of reports for each UFO shape in the selected country. Shape is a category on the vertical axis, and the number of reports is a numeric value on the horizontal axis. The bars are sorted from largest to smallest to make the most common shapes easy to identify. All bars use the same blue because their lengths already show the counts, so a color scale is unnecessary. In Python, I grouped the data by country and shape and counted the records in each group. Records missing a country or shape are excluded by this grouping.

## Interactivity

The country dropdown filters the second chart. Selecting a country updates the bars to show only its reports. This makes it easier to explore the most common reported shapes within each country without mixing all countries together.

## Data and Analysis

[The Data](https://raw.githubusercontent.com/UIUC-iSchool-DataViz/is445_data/main/ufo-scrubbed-geocoded-time-standardized-00.csv)

[The Analysis](https://github.com/fjdegante/fjdegante.github.io/blob/main/python_notebooks/hw5.ipynb)

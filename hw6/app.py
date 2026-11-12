import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="UFO Sightings", layout="wide")

st.title("Exploring UFO Sightings")
st.write("Fernando Degante | Homework 6")

st.write(
    "Explore reported UFO sightings over time and compare reported shapes. "
    "Use the country dropdown and year slider to change both charts."
)

DATA_URL = (
    "https://raw.githubusercontent.com/UIUC-iSchool-DataViz/"
    "is445_data/main/ufo-scrubbed-geocoded-time-standardized-00.csv"
)


@st.cache_data
def load_data():
    columns = [
        "datetime", "city", "state", "country", "shape",
        "duration_seconds", "duration_text", "comments",
        "date_posted", "latitude", "longitude"
    ]

    df = pd.read_csv(
        DATA_URL,
        header=None,
        names=columns,
        low_memory=False
    )

    df["year"] = pd.to_numeric(
        df["datetime"].str.split().str[0].str.split("/").str[2],
        errors="coerce"
    )

    df = df.dropna(subset=["year"]).copy()
    df["year"] = df["year"].astype(int)

    for column in ["country", "shape"]:
        df[column] = (
            df[column].astype("string").str.strip().str.lower()
        )
        df[column] = df[column].fillna("unknown").replace("", "unknown")

    return df


df = load_data()

st.sidebar.header("Filter the data")

countries = ["All countries"] + sorted(df["country"].unique())
country = st.sidebar.selectbox("Country", countries)

min_year = int(df["year"].min())
max_year = int(df["year"].max())

year_range = st.sidebar.slider(
    "Year range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

filtered = df[df["year"].between(*year_range)]

if country != "All countries":
    filtered = filtered[filtered["country"] == country]

st.metric("Reports matching your filters", f"{len(filtered):,}")

st.caption(
    "These records describe reported sightings, not verified events. "
    "Unknown indicates a missing country or shape."
)

if filtered.empty:
    st.warning("No reports match these filters. Try a wider year range.")
else:
    st.subheader("1. Reported UFO Sightings by Year")

    year_counts = (
        filtered.groupby("year")
        .size()
        .reindex(
            range(year_range[0], year_range[1] + 1),
            fill_value=0
        )
        .rename_axis("year")
        .reset_index(name="sightings")
    )

    chart1 = alt.Chart(year_counts).mark_line(
        color="#2563eb",
        point=True
    ).encode(
        x=alt.X(
            "year:Q",
            title="Year",
            axis=alt.Axis(format="d"),
            scale=alt.Scale(zero=False)
        ),
        y=alt.Y(
            "sightings:Q",
            title="Number of reports",
            scale=alt.Scale(zero=True)
        ),
        tooltip=[
            alt.Tooltip("year:Q", title="Year", format="d"),
            alt.Tooltip("sightings:Q", title="Reports", format=",")
        ]
    ).properties(height=350)

    st.altair_chart(chart1, width="stretch")

    st.write(
        "This line chart highlights how the number of reported UFO "
        "sightings varies over time for the selected country and year "
        "range. A line connects yearly counts to make changes over time "
        "easy to follow, and points identify individual years. The "
        "horizontal axis uses numeric years, while the vertical axis "
        "starts at zero so the counts have a clear baseline. A single "
        "blue color keeps attention on the overall pattern. The country "
        "dropdown and year slider allow viewers to explore subsets of "
        "the data. With more time, this chart could include a comparison "
        "between countries. Changes in report counts should not be "
        "interpreted as changes in verified UFO activity."
    )

    st.subheader("2. Reported UFO Shapes")

    shape_counts = (
        filtered.groupby("shape")
        .size()
        .reset_index(name="sightings")
    )

    chart2 = alt.Chart(shape_counts).mark_bar(
        color="#0f766e"
    ).encode(
        x=alt.X(
            "sightings:Q",
            title="Number of reports",
            scale=alt.Scale(zero=True)
        ),
        y=alt.Y(
            "shape:N",
            title="Reported shape",
            sort="-x"
        ),
        tooltip=[
            alt.Tooltip("shape:N", title="Shape"),
            alt.Tooltip("sightings:Q", title="Reports", format=",")
        ]
    ).properties(height=550)

    st.altair_chart(chart2, width="stretch")

    st.write(
        "This horizontal bar chart highlights which UFO shapes appear "
        "most often in reports matching the selected filters. Shapes "
        "are sorted by count so viewers can easily compare the most "
        "and least frequently reported categories. Horizontal bars "
        "leave room for shape labels, and the count axis starts at "
        "zero so bar lengths represent the counts proportionally. "
        "A single teal color avoids suggesting additional categories "
        "through color. Both the country dropdown and year slider "
        "update this chart, allowing viewers to explore how the shape "
        "distribution changes across subsets. With more time, a "
        "percentage option could make comparisons between countries "
        "with different numbers of reports easier."
    )

st.divider()
st.subheader("Relationship to Homework 5")

st.write(
    "Both visualizations are adapted from my Homework 5 notebook, "
    "python_notebooks/hw5.ipynb. I reused the UFO dataset, column names, "
    "year extraction approach, yearly report counts, and shape report "
    "counts. I also reused the line-chart design and sorted horizontal "
    "bar-chart design. For Homework 6, I moved the charts into Streamlit, "
    "replaced the Altair country dropdown with a Streamlit dropdown, "
    "added an all-countries option and a year-range slider that affect "
    "both charts, and added axis labels, tooltips, a report count, and "
    "explicit handling of missing country and shape values. Years with "
    "no matching reports are displayed with zero counts. The explanation "
    "paragraphs on this page are new."
)

st.markdown(f"[View the source dataset]({DATA_URL})")

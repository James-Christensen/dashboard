import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt


st.set_page_config(
    page_title="GOBRI",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

#import style sheet
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
  
#all data

def get_data():
    all_data = pd.read_csv(r"data.csv")
    df = pd.DataFrame(data=all_data)
    return df


df = get_data()

df=df.round(2)

st.sidebar.subheader("Chart Options")
colorSelect = st.sidebar.selectbox("Color Scheme:", ("Region", "Country", "Influence"))
influenceSelect = st.sidebar.selectbox(
    "Select Influence:", ("All", "High", "Medium", "Low")
)
logX = st.sidebar.checkbox("Logarithmic Y-Axis")
st.sidebar.caption("Select to group axes values by high, medium, and low.")
tick_values = st.sidebar.checkbox("Range")
bubbleSize = st.sidebar.slider(
    "Adjust Bubble Size", min_value=50, max_value=500, value=200
)

st.sidebar.markdown("---")

newRegion = st.sidebar.multiselect(
    "Filter Regions:", options=df["Region"].unique(), default=df["Region"].unique()
)

df_Reg = df.query("Region ==@newRegion")

show_countries = st.sidebar.checkbox("Check to Filter by Country")
if show_countries:
    newCountry = st.sidebar.multiselect(
        "Filter Countries",
        options=df_Reg["Country"].unique(),
        default=df_Reg["Country"].unique(),
    )


barDF = df
barDF.sort_values(by="Opportunity Index", ascending=False)
sortx = "Country"
bar_D = barDF["Depth of Relationship"]
newDF = (bar_D * 100).round(2)
newDF = newDF.astype(str)

barDF["Depth of Relationship"] = newDF.astype(str) + "%"


if influenceSelect == "All":
    try:
        df_selection = df.query("Region ==@newRegion & Country == @newCountry")
    except:
        df_selection = df.query("Region ==@newRegion")
else:
    try:
        df_selection = df.query(
            "Region ==@newRegion & Country == @newCountry & Influence ==@influenceSelect"
        )
    except:
        df_selection = df.query("Region ==@newRegion & Influence ==@influenceSelect")
    else:
        df_selection = df.query("Region ==@newRegion")

count = len(df_selection.index)
total = (df_selection["Market Size"].sum() / 1000).round(2)
average = round((df_selection["Opportunity Index"].sum()) / count, 2)


if colorSelect == "Country":
    color_select = "Country"
elif colorSelect == "Region":
    color_select = "Region"
else:
    color_select = "Influence"

# st.markdown('---')

if logX:
    axisValue = True
else:
    axisValue = False

if total >= 1:
    market = "Billion"
else:
    total = (total * 1000).round(2)
    market = "Million"

# KPIS Alt View
with st.expander("Show Stats", expanded=True):
    left_col, middle_col, right_col = st.columns(3)
    with left_col:
        st.subheader("Number of Countries:")
        st.subheader(f"{count}")
    with middle_col:
        st.subheader("Market Size:")
        st.subheader(f"${total} {market}")
    with right_col:
        st.subheader("Opportunity Index Average:")
        st.subheader(f"{average}")


# Bubble Chart
fig = px.scatter(
    df_selection,
    y="Opportunity Index",
    x="Regulatory Index",
    size="Market Size",
    color=color_select,
    hover_name="Country",
    size_max=bubbleSize,
    log_y=axisValue,
    template="simple_white",
)
if color_select == "Influence":
    fig = px.scatter(
        df_selection,
        y="Opportunity Index",
        x="Regulatory Index",
        size="Market Size",
        color=color_select,
        hover_name="Country",
        color_discrete_map={"High": "orange", "Medium": "yellow", "Low": "purple"},
        category_orders={"Regional Influence": ["Low", "Medium", "High"]},
        size_max=bubbleSize,
        log_y=axisValue,
        template="simple_white",
    )

fig.update_layout(
    height=700,
    title="     Market Overview",
    font=dict(
        family="'Noto Sans KR', sans-serif",
        size=18,
        # color="#F79E1B"
    ),
)

if tick_values:
    fig.update_layout(
        xaxis=dict(
            tickmode="array", tickvals=[2, 5, 8], ticktext=["Low", "Med.", "High"]
        )
    )

    fig.update_layout(
        yaxis=dict(
            tickmode="array", tickvals=[1, 2, 3], ticktext=["Low", "Med.", "High"]
        )
    )
else:
    pass

st.plotly_chart(fig, theme="streamlit", height=700, use_container_width=True)

# DataFrame
with st.expander("Show Data Table", expanded=False):
    st.dataframe(df_selection.style.format(precision=2), use_container_width=True)

# BarChart
change_sort = st.checkbox(label="Change Sort", value=False, key="ChangeSort")

if change_sort:
    sortx = alt.X("Country", sort="y")

bars = (
    alt.Chart(df_selection)
    .mark_bar()
    .encode(
        x=sortx,
        y="Opportunity Index",
        tooltip=[
            {"field": "Country", "type": "nominal"},
            {"field": "Count of Aggregators", "type": "quantitative"},
            {"field": "Fintech / Bank Ratio", "type": "quantitative"},
            {"field": "Depth of Relationship", "type": "nominal", "title": "MA Depth of Relationship"},
        ],
    )
    .configure_mark(color="orange")
)
text = bars.mark_text(
    align="left",
    baseline="middle",
    dx=3,  # Nudges text to right so it doesn't appear on top of the bar
).encode(text="Country")
st.altair_chart(bars, use_container_width=True)


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

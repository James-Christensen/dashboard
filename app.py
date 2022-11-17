import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Global Open Banking Readiness Indices",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

#all data
@st.cache
def get_data():
    all_data=pd.read_csv(r'data.csv')  
    df= pd.DataFrame(data=all_data)
    return df

df=get_data()

with open(r'C:\Users\James Christensen\Python_3_10\dashboard\style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

colorSelect= st.sidebar.selectbox("Color Scheme:", ("Region","Country"))
st.sidebar.markdown("---")

newRegion=st.sidebar.multiselect(
    "Filter Regions:",
    options=df["Region"].unique(),
    default=df['Region'].unique()

)

df_Reg=df.query('Region ==@newRegion')

show_countries= st.sidebar.checkbox("Check to Filter by Country")
if show_countries: 
    newCountry=st.sidebar.multiselect(
        "Filter Countries",
        options=df_Reg["Country"].unique(),
        default=df_Reg["Country"].unique(),
    )

try:
    df_selection=df.query("Region ==@newRegion & Country == @newCountry")
except:
    df_selection=df.query("Region ==@newRegion")

count= len(df_selection.index)
total=df_selection['TAM'].sum().round()
average = round((df_selection['Opportunity Index'].sum())/count,2)


if colorSelect == "Country":
    color_select = "Country"
else:
    color_select="Region"

st.markdown('---')

#Reset Button
# if reset = st.sidebar.button("Reset Filters"):
    

#KPIS
# st.markdown(f'<div class="display-flex"><div class="card"><h2>Countries</h2><h1>{count}</h1></div><div class="card"><h2>TAM</h2><h1>${total}B</h1></div><div class="card"><h2>Oppty. Index Avg.</h2><h1>{average}</h1></div></div>', unsafe_allow_html=True)
# st.markdown("---")

#KPIS Alt View
left_col,middle_col,right_col = st.columns(3)
with left_col:
    st.subheader("Number of Countries:")
    st.subheader(f"{count}")
with middle_col:
    st.subheader("Total Addressable  Market:")
    st.subheader(f"${total} Billion")
with right_col:
    st.markdown('### Opportunity Index Average:')
    st.subheader(f"{average}")


#Bubble Chart
fig = px.scatter(df_selection, x='Opportunity Index', y='Regulatory Index*',size="TAM", color=color_select,hover_name="Country", size_max=200,log_x=True,template ="simple_white")
fig.update_layout(height=700,
    title="Market Overview",
    font=dict(
        family="'Noto Sans KR', sans-serif",
        size=18,
        # color="#F79E1B"
    ))

st.plotly_chart(fig, height=700, use_container_width=True)
st.markdown("---")

#DataFrame
with st.expander("Show Data Table", expanded=False): 
    st.dataframe(df_selection,use_container_width=True)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

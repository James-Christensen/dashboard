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


with open(r'style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.sidebar.subheader("Chart Options")
colorSelect= st.sidebar.selectbox("Color Scheme:", ("Region","Country","Influence"))
logX= st.sidebar.checkbox("Logarithmic Y-Axis")
st.sidebar.caption("Select to group axes values by high, medium, and low.")
tick_values= st.sidebar.checkbox("Range")
bubbleSize=st.sidebar.slider("Adjust Bubble Size", min_value=50, max_value=500,value=200)

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
total=(df_selection['Market Size'].sum()/1000).round(2)
average = round((df_selection['Opportunity Index'].sum())/count,2)


if colorSelect == "Country":
    color_select = "Country"
elif colorSelect =="Region":
    color_select="Region"
else:
    color_select="Regional Influence"

# st.markdown('---')

if logX:
    axisValue=True
else:
    axisValue=False


#KPIS Alt View
with st.expander('Show Stats',expanded=False):
    left_col,middle_col,right_col = st.columns(3)
    with left_col:
        st.subheader("Number of Countries:")
        st.subheader(f"{count}")
    with middle_col:
        st.subheader("Market Size:")
        st.subheader(f"${total} Billion")
    with right_col:
        st.subheader('Opportunity Index Average:')
        st.subheader(f"{average}")


#Bubble Chart
fig = px.scatter(df_selection, y='Opportunity Index', x='Regulatory Index',size="Market Size", color=color_select,hover_name="Country", size_max=bubbleSize,log_y=axisValue,template ="simple_white")
fig.update_layout(height=700,
    title="Market Overview",
    font=dict(
        family="'Noto Sans KR', sans-serif",
        size=18,
        # color="#F79E1B"
    ))

if tick_values:
    fig.update_layout(
    xaxis = dict(
        tickmode = 'array',
        tickvals = [2,5,8],
        ticktext = ['Low', 'Med.', 'High']
    )
    )

    fig.update_layout(
    yaxis = dict(
        tickmode = 'array',
        tickvals = [1,2,3],
        ticktext = ['Low', 'Med.', 'High']
    )
    )
else:
    pass

st.plotly_chart(fig,theme="streamlit", height=700, use_container_width=True)



    
#DataFrame
with st.expander("Show Data Table", expanded=False): 
    st.dataframe(df_selection,use_container_width=True)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

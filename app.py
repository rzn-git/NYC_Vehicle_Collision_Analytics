import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px
#@st.cache(persist=True)

Data_Url = r"C:\Users\rzn\Desktop\NYC Vehicle Collision Analytics\NYC_Vehicle_Collision.csv"

st.title(":blue[Motor Vehicle Collision in New York City]")
st.markdown("#### 📊 Data from NYPD with 2.04 M Rows and 29 Columns")
st.markdown("Streamlit Dashboard using pydeck, Plotly Express, Pandas, and NumPy in Python. [Data Source](https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95)")


df = pd.read_csv(Data_Url, nrows = 100000, parse_dates=[['CRASH_DATE','CRASH_TIME']])
df2=df.dropna(subset=['LATITUDE','LONGITUDE'], inplace=False)
df3=df2.rename(lambda x: str(x).lower(),axis='columns')
df4= df3.rename(columns={'crash_date_crash_time' : 'date/time'})


#df4['injured_persons'].max()
df5 = df4.dropna(subset=['injured_persons'], inplace=False)


st.header(":orange[🤕 Where do most people get injured in NYC?]")
injured_people = st.slider("Slide to select a number of people injured in vehicle collisions",0,19)
st.map(df5.query("injured_persons >= @injured_people")[["latitude" , "longitude"]])




st.header(":orange[🚙 How many car accidents happen at a certain time of day?]")
hour=st.slider("Slide to select a timespan", 0,23)
df5 = df5[df5['date/time'].dt.hour == hour]

st.markdown("Vehicle Collisions between %i.00 and %i.00" %(hour, (hour+1) % 24))

midpoint = np.average(df5['latitude']), np.average(df5['longitude'])

st.write ( pdk.Deck (
    map_style = "mapbox://styles/mapbox/light-v9",
    initial_view_state = {
        "latitude" : midpoint[0],
        "longitude" : midpoint[1],
        "zoom" : 11,
        "pitch" :50,
        },
    layers = [        
        pdk.Layer (
        "HexagonLayer",
        data = df5[['date/time','longitude','latitude']],
        get_position = ['longitude' , 'latitude'],
        radius = 100,
        extruded = True,
        pickable = True,
        elevation_scale = 4,
        elevation_range = [0,1000],
        ),
    ],
))   


st.subheader("Breakdown by minute between %i:00 and %i:00" %(hour,(hour + 1) %24))

filtered = df5[
    (df5['date/time'].dt.hour >= hour) & (df5['date/time'].dt.hour < (hour+1))
]



hist = np.histogram(filtered['date/time'].dt.minute, bins=60, range=(0,60))[0]
chart_data = pd.DataFrame({'minute': range(60), 'crashes':hist})
fig = px.bar(chart_data, x='minute', y= 'crashes', hover_data=['minute', 'crashes'], height=400)
st.write(fig)


st.header("🏃 Top 5 dangerous streets by injured people")
select = st.selectbox('Dropdown to select the type of people who got injured', ['Pedestrians','Cyclists','Motorists'])

if select == 'Pedestrians':
    st.write(df5.query("injured_pedestrians >=1")[["on_street_name", "injured_pedestrians"]].sort_values(by=['injured_pedestrians'], ascending=False).dropna(how='any')[:5])

elif select == 'Cyclists':
    st.write(df5.query("injured_cyclists >=1")[["on_street_name", "injured_cyclists"]].sort_values(by=['injured_cyclists'], ascending=False).dropna(how='any')[:5])

elif select == 'Motorists':
    st.write(df5.query("injured_motorists >=1")[["on_street_name", "injured_motorists"]].sort_values(by=['injured_motorists'], ascending=False).dropna(how='any')[:5])



if st.checkbox("Show Raw Data",False):
    st.subheader('🔢 Raw Data')
    st.write(df5)
'''
Name:       Olivia Siracusa
CS230:      Section 004
Data:       Motor Vehicle Crashes in MA in 2017
URL:

Description: This website displays data about motor crash vehicles in 2017.
                It includes 4 pages about the total amount of crashes, analysis on crash
                conditions, maps, and anaylsis on the speed limit.
'''

#Import packages
import streamlit as st
import pandas as pd
import seaborn as sns
import pydeck as pdk
import matplotlib.pyplot as plt
st.set_page_config(page_title="Motor Vehicle Crashes", page_icon="🚗")

#Import Data
path = "C:/Users/sirac/OneDrive - Bentley University/CS 230/"
df_crash = pd.read_csv(path + "2017_Crashes.csv", index_col='OBJECTID', nrows=10000)


#Sidebar
st.sidebar.success("Click on the other pages of the website")
sidebar = st.sidebar.radio("",['Home Page','Analysis', 'Crash Conditions', 'Maps', 'Speed Limit'])

if sidebar == 'Home Page':
    # Title
    st.title("Welcome!")
    st.write("This website explores the first 10000 entries in dataset Motor Vehicle Crashes in 2017.")
    #[DA2]
    st.title("Motor Vehicle Data")
    st.write("This data is ascending in date and descending in town name. ")
    df_multi_sorted = df_crash.sort_values(by=['CRASH_DATE_TEXT', 'CITY_TOWN_NAME'], ascending=[True, False])
    st.write(df_multi_sorted)

    #[PY4]
    def extract_column_values(data, column_name):
        '''
            Extract values from a specified column of a DataFrame using a list comprehension.

            Parameters:
                - data: The dataframe containing the crash data
                - column_name: The name of the column from which the values are to be extracted.

            Returns:
                - A list containing the values of the specified column.
        '''
        return [value for value in data[column_name]]

    st.title("Data in each Column")
    selected_columns = st.selectbox("Select column", ['(None Selected)'] + list(df_crash.columns)) #[ST3]

    if selected_columns and selected_columns != '(None Selected)': #[DA5]
        values = extract_column_values(df_crash, selected_columns)
        st.write(f"Values for column '{selected_columns}': {values}")

#Sidebar Radio

elif sidebar == 'Analysis':
    st.sidebar.header("🚗 Car Crash Analysis")
    # Information about the page
    st.title("Car Crash Analysis")
    st.write(
        "The information below provides an analysis of motor vehicle crashes based on specific location and date parameters."
        "The data below is valuable for conducting targeted analyses and gaining insights into how frequent crashes occur in certain areas over time.")
    st.write("\n Look how many crashes occurred on a certain date by inputting a town name and date:")


    # [PY1]
    def crash_by_location(data, location, date="1/1/2017"):
        '''
            Analyzing motor vehichle crashes for a specific date and location.

            Parameters:
                - data: the dataframe containing the crash data
                - location: The city where the crash occurred
                - date: The date the crash happened. Default is 1/1/2017

            Returns:
                - The total number of crashes on the provided data, year and location
        '''
        total_crashes = 0
        for index, row in data.iterrows():  # [DA8]
            if row['CITY_TOWN_NAME'].lower().capitalize() == location and row['CRASH_DATE_TEXT'] == date:  # [DA5]
                total_crashes += 1
        return total_crashes


    town_name = st.text_input("Enter the town name:")  # [ST1]
    date = st.text_input("Enter a date in MM/DD/YYYY format:", "01/01/2017")
    if st.button("Analyze"):
        crash_count = crash_by_location(df_crash, town_name, date)
        st.write(f"The total number of crashes in {town_name} in {date}: {crash_count}")

    st.title("Barplot")
    st.write(
        "This barplot displays whether the car accident is a hit and run, type of road condition and the average number of cars involved with those two criterias. "
        "This plot is aimed to provide information about patterns and trends in crash occurences, and aiding in informed decision-making for improving road safety measures. ")
    sns.set_theme(style="whitegrid")  # [VIZ3]
    g = sns.catplot(
        data=df_crash, kind="bar",
        x="ROAD_SURF_COND_DESCR", y="NUMB_VEHC", hue="HIT_RUN_DESCR",
        errorbar="sd", palette="dark", alpha=.5, height=15
    )
    g.despine(left=True)
    g.set_axis_labels("", "Average Number of Cars")
    st.set_option('deprecation.showPyplotGlobalUse', False)
    g.legend.set_title("")
    st.pyplot()

elif sidebar == 'Crash Conditions':

    st.sidebar.header("☁️ Analysis on Crash Conditions ")

    st.title("Analysis on Crash Conditions")
    st.write(
        "This page offers a valuable tool for analyzing and visualizing motor vehicle crash data, enabling users to extract"
        " key information about specific crashes and gain insights into the prevailing conditions at the time of the incidents.")


    # [PY2]
    def get_crash_conditions(data, crash_number):
        '''
            Get the light description, weather condition, and road surface condition based on the crash number

            Parameters:
                - data: The dataframe containing the crash data
                - crash_number: The number of the crash for which the conditions are retrieved
            Returns:
                - Light Description, weather condition, and road surface condition for the specified crash.
        '''
        if crash_number in data['CRASH_NUMB'].astype(str).values:
            crash_index = data[data['CRASH_NUMB'].astype(str) == crash_number].index[0]
            light_descript = data.at[crash_index, 'AMBNT_LIGHT_DESCR']
            weather_condition = data.at[crash_index, 'WEATH_COND_DESCR']
            road_surface = data.at[crash_index, 'ROAD_SURF_COND_DESCR']
            return light_descript, weather_condition, road_surface
        else:
            return None, None, None


    st.title("Crash Condition Viewer")

    crash_num = st.text_input("Enter the crash number: ", "4304436")
    if st.button("Get Crash Conditions"):
        light, weather, road_surface = get_crash_conditions(df_crash, crash_num)
        if light is not None:
            st.write(f"The light description for crash number {crash_num} is:", light)
            st.write(f"The weather condition for crash number {crash_num} is:", weather)
            st.write(f"The road surface condition for crash number {crash_num} is:", road_surface)
        else:
            st.write(f"No crash found with number {crash_num}")

    st.title('Bar Chart for various conditions')
    selected_columns = ['AMBNT_LIGHT_DESCR', 'WEATH_COND_DESCR', 'ROAD_SURF_COND_DESCR']
    df_selected = df_crash[selected_columns]
    melt_df = df_selected.melt(var_name='Condition', value_name='Description')
    selected_condition = st.selectbox("Select a condition", selected_columns)
    pivot_df = melt_df[melt_df['Condition'] == selected_condition].groupby('Description').size().reset_index(
        name='count')
    st.bar_chart(pivot_df.set_index('Description'), color="#C70039")

elif sidebar == 'Maps':

    st.sidebar.header("🗺️ Maps")
    # Import Data
    path = "//"
    df_crash = pd.read_csv(path + "2017_Crashes.csv", index_col='OBJECTID', nrows=10000)

    st.title("Maps")
    st.write("This page has multiple different maps visualization of the crash data. ")

    df_crash.dropna(subset=['LAT', 'LON'], inplace=True)

    # Maps
    df_crash.rename(columns={"LAT": "lat", "LON": "lon"}, inplace=True)

    select_map = st.radio('Please select the type of map', ['Simple', 'Heatmap', '3d'])

    if select_map == 'Simple':
        st.title('Simple Map')
        st.map(df_crash)

    elif select_map == '3d':

        st.title('3d Map of Crashes in Massachusetts in 2017')

        st.pydeck_chart(pdk.Deck(
            map_style=None,
            initial_view_state=pdk.ViewState(
                latitude=42.4072,
                longitude=-71.3824,
                zoom=7,
                pitch=50
            ),
            layers=[
                pdk.Layer('HexagonLayer',
                          data=df_crash,
                          get_position='[lon,lat]',
                          radius=200,
                          elevation_scale=4,
                          elevation_range=[0, 1000],
                          pickable=True,
                          extruded=True, ),
                pdk.Layer(
                    'ScatterplotLayer',
                    data=df_crash,
                    get_position='[lon,lat]',
                    get_color='[200, 30, 0, 160]',
                    get_radius=200, ),
            ],
        ))
        select_city = st.selectbox('Select a City to look further into:', (
        'Choose a City', 'Springfield', 'Chelsea', 'Fitchburg', 'Holyoke', 'Hudson', 'New Bedford'))
        if select_city == 'Springfield':
            df_crash_springfield = df_crash[df_crash['CITY_TOWN_NAME'] == 'SPRINGFIELD']
            st.title('3d Map of Crashes in Springfield in 2017')

            st.pydeck_chart(pdk.Deck(
                map_style=None,
                initial_view_state=pdk.ViewState(
                    latitude=42.1015,
                    longitude=-72.5898,
                    zoom=11,
                    pitch=50
                ),
                layers=[
                    pdk.Layer('HexagonLayer',
                              data=df_crash_springfield,
                              get_position='[lon,lat]',
                              radius=200,
                              elevation_scale=4,
                              elevation_range=[0, 1000],
                              pickable=True,
                              extruded=True, ),
                    pdk.Layer(
                        'ScatterplotLayer',
                        data=df_crash_springfield,
                        get_position='[lon,lat]',
                        get_color='[200, 30, 0, 160]',
                        get_radius=200, ),
                ],
            ))
        elif select_city == 'Chelsea':
            df_crash_chelsea = df_crash[df_crash['CITY_TOWN_NAME'] == 'CHELSEA']
            st.title('3d Map of Crashes in Chelsea in 2017')

            st.pydeck_chart(pdk.Deck(
                map_style=None,
                initial_view_state=pdk.ViewState(
                    latitude=42.3918,
                    longitude=-71.0328,
                    zoom=11,
                    pitch=50
                ),
                layers=[
                    pdk.Layer('HexagonLayer',
                              data=df_crash_chelsea,
                              get_position='[lon,lat]',
                              radius=200,
                              elevation_scale=4,
                              elevation_range=[0, 1000],
                              pickable=True,
                              extruded=True, ),
                    pdk.Layer(
                        'ScatterplotLayer',
                        data=df_crash_chelsea,
                        get_position='[lon,lat]',
                        get_color='[255, 0, 0, 128]',
                        get_radius=200, ),
                ],
            ))
        elif select_city == 'Fitchburg':
            df_crash_fitchburg = df_crash[df_crash['CITY_TOWN_NAME'] == 'FITCHBURG']
            st.title('3d Map of Crashes in Fitchburg in 2017')

            st.pydeck_chart(pdk.Deck(
                map_style=None,
                initial_view_state=pdk.ViewState(
                    latitude=42.5834,
                    longitude=-71.8023,
                    zoom=11,
                    pitch=50
                ),
                layers=[
                    pdk.Layer('HexagonLayer',
                              data=df_crash_fitchburg,
                              get_position='[lon,lat]',
                              radius=200,
                              elevation_scale=4,
                              elevation_range=[0, 1000],
                              pickable=True,
                              extruded=True, ),
                    pdk.Layer(
                        'ScatterplotLayer',
                        data=df_crash_fitchburg,
                        get_position='[lon,lat]',
                        get_color='[255, 0, 0, 128]',
                        get_radius=200, ),
                ],
            ))
        elif select_city == 'Holyoke':
            df_crash_holyoke = df_crash[df_crash['CITY_TOWN_NAME'] == 'HOLYOKE']
            st.title('3d Map of Crashes in Holyoke in 2017')

            st.pydeck_chart(pdk.Deck(
                map_style=None,
                initial_view_state=pdk.ViewState(
                    latitude=42.2043,
                    longitude=-72.6162,
                    zoom=11,
                    pitch=50
                ),
                layers=[
                    pdk.Layer('HexagonLayer',
                              data=df_crash_holyoke,
                              get_position='[lon,lat]',
                              radius=200,
                              elevation_scale=4,
                              elevation_range=[0, 1000],
                              pickable=True,
                              extruded=True, ),
                    pdk.Layer(
                        'ScatterplotLayer',
                        data=df_crash_holyoke,
                        get_position='[lon,lat]',
                        get_color='[255, 0, 0, 128]',
                        get_radius=200, ),
                ],
            ))
        elif select_city == 'Hudson':
            df_crash_hudson = df_crash[df_crash['CITY_TOWN_NAME'] == 'HUDSON']
            st.title('3d Map of Crashes in Hudson in 2017')

            st.pydeck_chart(pdk.Deck(
                map_style=None,
                initial_view_state=pdk.ViewState(
                    latitude=42.3917,
                    longitude=-71.5661,
                    zoom=11,
                    pitch=50
                ),
                layers=[
                    pdk.Layer('HexagonLayer',
                              data=df_crash_hudson,
                              get_position='[lon,lat]',
                              radius=200,
                              elevation_scale=4,
                              elevation_range=[0, 1000],
                              pickable=True,
                              extruded=True, ),
                    pdk.Layer(
                        'ScatterplotLayer',
                        data=df_crash_hudson,
                        get_position='[lon,lat]',
                        get_color='[255, 0, 0, 128]',
                        get_radius=200, ),
                ],
            ))
        elif select_city == 'New Bedford':
            df_crash_newbedford = df_crash[df_crash['CITY_TOWN_NAME'] == 'NEW BEDFORD']
            st.title('3d Map of Crashes in New Bedford in 2017')

            st.pydeck_chart(pdk.Deck(
                map_style=None,
                initial_view_state=pdk.ViewState(
                    latitude=41.6362,
                    longitude=-70.9342,
                    zoom=11,
                    pitch=50
                ),
                layers=[
                    pdk.Layer('HexagonLayer',
                              data=df_crash_newbedford,
                              get_position='[lon,lat]',
                              radius=200,
                              elevation_scale=4,
                              elevation_range=[0, 1000],
                              pickable=True,
                              extruded=True, ),
                    pdk.Layer(
                        'ScatterplotLayer',
                        data=df_crash_newbedford,
                        get_position='[lon,lat]',
                        get_color='[255, 0, 0, 128]',
                        get_radius=200, ),
                ],
            ))
    if select_map == 'Heatmap':
        st.title('Heatmap')
        st.pydeck_chart(pdk.Deck(
            map_provider="mapbox",
            map_style=pdk.map_styles.SATELLITE,
            tooltip={"text": "Town Name: {CITY_TOWN_NAME}"},
            initial_view_state=pdk.ViewState(
                latitude=42.4072,
                longitude=-71.3824,
                zoom=7,
                pitch=50
            ),
            layers=[
                pdk.Layer(
                    "HeatmapLayer",
                    data=df_crash,
                    opacity=0.9,
                    get_position=['lon', 'lat'],
                    get_color=[255, 0, 0, 128],
                    pickable=True,
                ),
                pdk.Layer(
                    "ScatterplotLayer",
                    data=df_crash,
                    get_position=['lon', 'lat'],
                    get_color=[255, 0, 0, 128],
                    get_radius=200,
                    pickable=True,
                )
            ]
        ))

elif sidebar =='Speed Limit':
    st.sidebar.header("Speed Limit ")
    # Import Data
    path = "//"
    df_crash = pd.read_csv(path + "2017_Crashes.csv", index_col='OBJECTID', nrows=10000)


    def calc_avg_speed_limit(data):
        """
            Find the average speed limit for roads where crashes were recorded

            Parameters:
                - data: The dataframe containing the crash data

            Returns:
                - The average speed limit of the roads where crashes occurred
        """
        average_speed_limit = data['SPEED_LIMIT'].mean()
        return average_speed_limit


    st.title("Average Speed Limit Analysis")
    st.write("Serves as a valuable tool for analyzing and understanding the speed limit dynamics "
             "surrounding motor vehicle crashes, offering insights into road safety and traffic management.")

    avg_speed_limit = calc_avg_speed_limit(df_crash)
    st.write(f"The average speed limit of roads where crashes occurred is: {avg_speed_limit:.2f}")

    st.title("Speed limit compared to the average speed of crashes")
    slider_speed = st.slider("Select a speed", min_value=0, max_value=100, value=40, step=1)  # [ST2]

    if avg_speed_limit < slider_speed:  # [DA4]
        st.write(
            f"The speed limit of {slider_speed} on roads where crashes occurred is relatively high compared to the average speed of {avg_speed_limit:.2f}.")
    else:
        st.write(
            f"The speed limit of {slider_speed} on roads where crashes occurred is relatively low compared to the average speed of {avg_speed_limit:.2f}.")

    s_speed = df_crash['SPEED_LIMIT'].value_counts()
    st.set_option('deprecation.showPyplotGlobalUse', False)
    plt.figure(figsize=(10, 10))
    explode = (0, 0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,)  # explode second slice
    s_speed.plot(kind='pie', startangle=180, explode=explode,
                 autopct=lambda p: '{:.0f}'.format(p * sum(s_speed / 100)))  # [DA1]
    plt.title('Distribution of Speed Limits')
    plt.legend(title="Speed Limits", loc='lower right')
    st.pyplot()

    # [DA3] Highest speed and lowest speed
    st.write("Below displays the highest and the lowest speed limits at all the crash sites. ")
    highest_speed = df_crash['SPEED_LIMIT'].nlargest(1)
    lowest_speed = df_crash['SPEED_LIMIT'].nsmallest(1)
    st.write(f"The highest speed limit recorded at a crash site is {highest_speed.values[0]:.0f} mph.")
    st.write(f"The lowest speed limit recorded at a crash site is {lowest_speed.values[0]:.0f} mph.")


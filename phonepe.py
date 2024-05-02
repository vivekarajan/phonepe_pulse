# Importing Libraries
import pandas as pd
import mysql.connector
import streamlit as st
import os
import json
import geopandas as gpd
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
from PIL import Image
import seaborn as sns
import numpy as np
import plotly.express as px
plt.style.use('_mpl-gallery')


connection = mysql.connector.connect(
        host='host',
        user='root',
        password="pwd",
        database="dbname"
    )
cur = connection.cursor()

# Setting up page configuration
icon = Image.open("E:\phonepe project\phonepe_logo.png")
st.set_page_config(page_title= "Phonepe Pulse Data Visualization - Vivekarajan S",
                   page_icon= icon,
                   layout= "wide",
                   initial_sidebar_state= "expanded",
                   menu_items={'About': """# This dashboard app is created by *Vivekarajan S*!
                                        Data has been cloned from Phonepe Pulse Github Repository"""})

st.sidebar.header(" :blue[**Hello! Welcome to my dashboard**]")

#create option in side bar
with st.sidebar:
    selected = option_menu("Menu", ["Home","Chart Analysis","India Map"], 
                icons=["house","graph-up-arrow","map"],
                menu_icon= "menu-button-wide",
                default_index=0,
                styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#EEF5FF"},
                        "nav-link-selected": {"background-color": "#008DDA"}})
    
if selected == "Home":
    st.markdown("## :blue[Creating a Dashboard by User-Friendly Tool Using Streamlit and Plotly]")
    st.write(" ")
    st.markdown("### :blue[Technologies used :] Github Cloning, Python, Pandas, MySQL, mysql-connector-python, Streamlit, and Plotly.")
    st.markdown("### :blue[Overview :] In this streamlit web app you can visualize the phonepe pulse data and gain lot of insights on transactions, number of users, top 10 state, district, pincode and which brand has most number of users and so on. Bar charts, Pie charts and Geo map visualization are used to get some insights.")

if selected == "Chart Analysis":
    st.markdown("## :violet[Top Charts]")
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    
    year = ['2018', '2019', '2020', '2021', '2022', '2023']
    selected_option1 = st.selectbox('Select an option:', year)
    quarter=['1st Quarter','2nd Quarter','3rd Quarter','4th Quarter']
    selected_option2 = st.selectbox('Select an option:', quarter)
    if Type == "Transactions":
        st.markdown("### :blue[Top 10 State based on Total number of transaction and Total amount spent on phonepe]")
        
        # Define your SQL query with placeholders
        sql_query = ("""SELECT State, SUM(Transaction_count) AS Total_Transactions_Count,
                     SUM(Transaction_amount) AS Total_Amount FROM agg_trans WHERE year = %s AND quarter = %s 
                     GROUP BY State ORDER BY Total_Amount DESC LIMIT 10;""")
    
        # Execute the query with the current year and quarter
        cur.execute(sql_query, (selected_option1, selected_option2))
    
        # Fetch the data and create a DataFrame
        data = cur.fetchall()
        df = pd.DataFrame(data, columns=['State', 'Total_Transactions_Count', 'Total_Amount'])
        
        # Plotting
        fig = px.bar(df, x='State', y='Total_Amount', color='Total_Transactions_Count')
        st.plotly_chart(fig, use_container_width=True)
#--------------------------------------------------------------------------------------------------------------
        #map_trans
        st.markdown("### :blue[Top 10 districts of Total Transactions]")
        sql_query = """SELECT Year, District, SUM(Count) AS Total_Transactions
               FROM map_trans WHERE year = %s AND quarter = %s
               GROUP BY Year, District
               ORDER BY Total_Transactions DESC
               LIMIT 10;"""

        # Execute the query
        cur.execute(sql_query, (selected_option1, selected_option2))

        # Fetch the data and create a DataFrame
        data = cur.fetchall()
        df = pd.DataFrame(data, columns=['Year', 'District', 'Total_Transactions'])
        fig = px.pie(df, values='Year', names='District', color='Total_Transactions')
        st.plotly_chart(fig, use_container_width=True)

#--------------------------------------------------------------------------------------------------------------
        #top_trans_district and top_trans_pincode
        st.markdown("### :blue[Top Districts by Total Amount from top_transaction data]")
        sql_query="""SELECT ttp.pincode,ttd.District,
                    SUM(ttd.Transaction_count) AS Total_Transactions_Count,
                    SUM(ttd.Transaction_amount) AS Total FROM top_trans_district AS ttd
                    JOIN top_trans_pincode AS ttp ON ttd.State = ttp.State
                    WHERE ttd.year = %s AND ttd.quarter = %s GROUP BY pincode,ttd.District
                    ORDER BY Total DESC LIMIT 10;"""
        cur.execute(sql_query,(selected_option1, selected_option2))
        data = cur.fetchall()
        df = pd.DataFrame(data, columns=['Pincode', 'District', 'Transactions_Count', 'Total_Amount'])

        # Plotting pie chart
        fig = px.pie(df, values='Total_Amount', names='District',
             hover_data=['Transactions_Count'],
             labels={'Transactions_Count': 'Transactions Count'})
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

#--------------------------------------------------------------------------------------------------------------
    if Type == "Users":
        st.markdown("### :blue[Top_users by brands]")
        
        # Define your SQL query with placeholders
        sql_query = ("""SELECT Brands, 
                     SUM(Count) AS Total_Transactions, 
                     SUM(Percentage) AS Total_Percentage
                     FROM agg_user WHERE year = %s AND quarter = %s 
                     GROUP BY Brands ORDER BY Total_Transactions DESC LIMIT 10;""")
        cur.execute(sql_query,(selected_option1, selected_option2))
    
        # Fetch the data and create a DataFrame
        data = cur.fetchall()
        df = pd.DataFrame(data, columns=['Brands', 'Total_Transactions','Total_Percentage'])

        # Plotting
        fig = px.bar(df,
                 x="Brands",
                 y="Total_Transactions",
                 orientation='v',
                 color='Total_Percentage',
                 color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=False)
#--------------------------------------------------------------------------------------------------------------
        #map_user
        st.markdown("### :blue[Top 10 District from registered users]")
        sql_query = ("""SELECT District, Year, Registered_user 
                     FROM map_user WHERE year = %s AND quarter = %s
                     GROUP BY District, Quarter, Year, Registered_user
                     ORDER BY Registered_user DESC 
                     LIMIT 10;""")
        cur.execute(sql_query,(selected_option1, selected_option2))

        # Fetch the data and create a DataFrame
        data = cur.fetchall()

        df = pd.DataFrame(data, columns=['District', 'Year', 'Registered_user'])
        fig = px.pie(df, values='Registered_user', names='District', color='District')
        st.plotly_chart(fig, use_container_width=True)

#------------------------------------------------------------------------------------------------------------------
        #top_use_district and pincode
        st.markdown("### :blue[state wise data for Registered users from top_user data]")
        sql_query = """SELECT state, MAX(district) AS district, MAX(RegisteredUsers) AS RegisteredUsers
                FROM (SELECT tud.state, tud.district, tud.RegisteredUsers, NULL AS Pincode 
                FROM top_user_district AS tud 
                WHERE tud.Year=%s AND tud.Quarter=%s 
                UNION ALL
                SELECT tup.state, NULL AS district, NULL AS RegisteredUsers, tup.Pincode 
                FROM top_user_pincode AS tup) AS combined_data 
                GROUP BY state order by RegisteredUsers desc limit 10;"""

        cur.execute(sql_query, (selected_option1, selected_option2))
        data = cur.fetchall()
        df = pd.DataFrame(data, columns=['state', 'District', 'RegisteredUsers'])

        fig = px.bar(df, x='state', y='RegisteredUsers', color='state', title='Top Districts by Registered Users')
        fig.update_xaxes(tickangle=45)
        fig.update_layout(xaxis_title='State', yaxis_title='Registered Users')
        st.plotly_chart(fig)
#------------------------------------------------------------------------------------------------------------------
#india map
if selected == "India Map":
        sql_query="""SELECT state, MAX(RegisteredUsers) AS RegisteredUsers FROM
        (SELECT tud.state, tud.district, tud.RegisteredUsers, NULL AS Pincode FROM top_user_district AS tud
        UNION ALL SELECT tup.state, NULL AS district, NULL AS RegisteredUsers, tup.Pincode FROM top_user_pincode AS tup) AS combined_data GROUP BY state;"""
        cur.execute(sql_query)
        data = cur.fetchall()
        df1 = pd.DataFrame(data, columns=['state', 'RegisteredUsers'])
        df2 = pd.read_csv('Statenames.csv')
        df1.state = df2
        
        fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                  featureidkey='properties.ST_NM',
                  locations='state',
                  color='RegisteredUsers',
                  color_continuous_scale='sunset')

        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig,use_container_width=True)

        
        

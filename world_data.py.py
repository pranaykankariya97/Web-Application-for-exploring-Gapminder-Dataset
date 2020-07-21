import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.offline as py
from plotly.figure_factory import create_table

st.title("World Data")
st.markdown("This application is to analyze and visualize life expectancy,population and GDP worldwide from year 1952-2007.")
st.sidebar.title("World Data")


@st.cache(persist=True)
def load_data():
    gapminder = px.data.gapminder()
    return gapminder


gapminder = load_data()

# Country Wise Bar Chart
st.sidebar.subheader("Comparing Countrywise Population ")
country_selected = st.sidebar.selectbox("Select Country", ('Afghanistan', 'Albania', 'Algeria', 'Angola', 'Argentina',
                                                           'Australia', 'Austria', 'Bahrain', 'Bangladesh', 'Belgium', 'Benin', 'Bolivia', 'Bosnia and Herzegovina', 'Botswana', 'Brazil',
                                                           'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Central African Republic', 'Chad', 'Chile', 'China',
                                                           'Colombia', 'Comoros', 'Congo, Dem. Rep.', 'Congo, Rep.', 'Costa Rica', "Cote d'Ivoire", 'Croatia', 'Cuba',
                                                           'Czech Republic' 'Denmark' 'Djibouti' 'Dominican Republic' 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Ethiopia', 'Finland', 'France', 'Gabon', 'Gambia', 'Germany', 'Ghana', 'Greece', 'Guatemala',
                                                           'Guinea', 'Guinea-Bissau', 'Haiti', 'Honduras', 'Hong Kong, China', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel',
                                                           'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kenya', 'Korea, Dem. Rep.', 'Korea, Rep.', 'Kuwait', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Madagascar',
                                                           'Malawi', 'Malaysia', 'Mali', 'Mauritania', 'Mauritius', 'Mexico', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nepal',
                                                           'Netherlands', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Norway', 'Oman', 'Pakistan', 'Panama', 'Paraguay', 'Peru', 'Philippines', 'Poland',
                                                           'Portugal', 'Puerto Rico', 'Reunion', 'Romania', 'Rwanda', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Sierra Leone', 'Singapore',
                                                           'Slovak Republic', 'Slovenia', 'Somalia', 'South Africa', 'Spain', 'Sri Lanka', 'Sudan', 'Swaziland', 'Sweden', 'Switzerland', 'Syria', 'Taiwan',
                                                           'Tanzania', 'Thailand', 'Togo', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Uganda', 'United Kingdom', 'United States', 'Uruguay', 'Venezuela',
                                                           'Vietnam', 'West Bank and Gaza', 'Yemen, Rep.', 'Zambia', 'Zimbabwe'))
data = gapminder[gapminder['country'].isin([country_selected])]
if not st.sidebar.checkbox("Close", True, key="country"):
    st.subheader("Comparing population of " + country_selected + " year by year")
    fig = px.bar(data, x="year", y="pop", height=500, width=700, hover_data=["lifeExp", "gdpPercap"], color="lifeExp",
                 labels={"pop": "Population of " + country_selected})
    st.plotly_chart(fig)
    if st.sidebar.checkbox("Show Data", False):
        st.write(create_table(data))

# Continent - Life Expectancy vs GDP
st.sidebar.subheader("Comparing Continents by Year")
year = st.sidebar.number_input("Enter a year (1952-2007) with increment of 5", 1952, 2007, step=5)
chart = st.sidebar.radio("Select a plot to visualize", ("Scatter Plot", "Bubble Plot", "Facet Plot"))
data_year = gapminder[gapminder["year"].isin([year])]
if not st.sidebar.checkbox("Close", True, key="year"):
    st.subheader("Comapring GDP and Life Expectancy for the Year " + str(year))
    if chart == "Scatter Plot":
        fig1 = px.scatter(data_year, x="gdpPercap", y="lifeExp", color="continent", labels={"gdpPercap": "GDP", "lifeExp": "Life Expectancy"})
        st.plotly_chart(fig1)
    if chart == "Bubble Plot":
        fig2 = px.scatter(data_year, x="gdpPercap", y="lifeExp", color="continent", size="pop", size_max=60, hover_name="country",
                          labels={"gdpPercap": "GDP", "lifeExp": "Life Expectancy"})
        st.plotly_chart(fig2)
    if chart == "Facet Plot":
        fig3 = px.scatter(data_year, x="gdpPercap", y="lifeExp", color="continent", size="pop", size_max=60, hover_name="country",
                          facet_col="continent", log_x=True, labels={"gdpPercap": "GDP", "lifeExp": "Life Expectancy"})

        st.plotly_chart(fig3)

# Animation
if st.sidebar.checkbox("Animated Visualization", False, key="animation"):
    fig4 = px.scatter(gapminder, x="gdpPercap", y="lifeExp", color="continent", size="pop", size_max=60, height=500, width=700, hover_name="country",
                      animation_frame="year", animation_group="country", log_x=True, range_x=[100, 100000], range_y=[25, 90],
                      labels={"pop": "Population", "gdpPercap": "GDP per Capita", "lifeExp": "Life Expectancy"})
    st.subheader("Life Expectancy vs GDP")
    st.plotly_chart(fig4)
    fig5 = px.choropleth(gapminder, locations="iso_alpha", color="lifeExp", hover_name="country", animation_frame="year",
                         color_continuous_scale=px.colors.sequential.Plasma, projection="natural earth", height=500, width=700)
    st.subheader("Life Expectancy")
    st.plotly_chart(fig5)

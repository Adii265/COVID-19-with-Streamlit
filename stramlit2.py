import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

DATA_URL = "COVID_dataset_2july2020.csv"

@st.cache
def load_data(nrows):
	data = pd.read_csv(DATA_URL,nrows=nrows)
	lowercase = lambda x: str(x).lower()
	data.rename(lowercase, axis='columns', inplace=True)
	
	return data


st.title(" COVID-19")
st.text("Latest By  - 2nd July, 2020")
data = load_data(10000)
data.columns = data.columns.str.strip().str.lower().str.replace(' ', '_')



st.sidebar.subheader("Home")
if not st.sidebar.checkbox("Hide", True,key = '10'):
	st.write("Total Cases Confirmed: ")
	st.subheader(str(data['confirmed'].sum()))
	st.write("Total Deaths: ")
	st.subheader(str(data['deaths'].sum()))
	st.write("Total Recovered: ")
	st.subheader(str(data['recovered'].sum()))

st.sidebar.subheader("Click here to see the Raw data")
if not st.sidebar.checkbox("Hide", True,key = '9'):
	st.subheader('Raw data')
	st.write(data)



list_of_region= set(data['who_region'])
#st.write(list_of_Country)
arr = [str(i) for i in list_of_region]
list_of_Country = set(data['country'])
arr1 = [str(i) for i in list_of_Country]


st.sidebar.subheader("Specific country") 
type_wise= st.sidebar.radio('Choose any one!', arr)
#st.write(type_wise)
choice_data = data.query("who_region == @type_wise")
#st.write(choice_data)
if not st.sidebar.checkbox("Hide", True, key='1'):
	st.subheader("Number of cases in region in "+type_wise)
	fig_1 = px.histogram( choice_data, x='country',
		y='confirmed',  height=500, width=800,
		labels={'country':'Country','sum of confirmed':'Confirmed Cases','who_region':'Region'})
	st.plotly_chart(fig_1)



st.sidebar.subheader("WHO Region") 
type_wise= st.sidebar.multiselect("Select as many as you want!",arr)
choice_data = data.query("who_region == @type_wise")
if len(type_wise) > 0:
	#st.write(type_wise) 
	#st.write(data.columns)
	if not st.sidebar.checkbox("Hide", True, key='2'):
		choice_data = data[data.who_region.isin(type_wise)]
		st.subheader("Number of cases in regions:")
		st.write(choice_data)
		fig_2 = px.histogram(choice_data, x='who_region', y='confirmed', 
			color='who_region', height=400, width=850,labels={'who_region':'Regions'})
		st.plotly_chart(fig_2)




st.sidebar.subheader("View for all Countries:") 
type_wise= st.sidebar.selectbox("Select any one!",('Confirmed','Active','Deaths','Recovered'))
#choice_data = data.query("")
if not st.sidebar.checkbox("Hide", True, key='3'):
	breakdown_type = st.sidebar.selectbox('Visualization type', ['Pie chart', 'Bar plot', ], key='4')
	#st.write(type_wise)]
	if breakdown_type == 'Bar plot':
		st.subheader('Bar-graph for '+type_wise+' cases.')
		fig_3 = px.histogram(data,x='country',
				y=type_wise.lower(), color='country', height=400, width=850)
		st.plotly_chart(fig_3)
	else:	
		st.subheader('Pie Chart for '+type_wise+' cases.')
		fig_3 = px.pie(data, values = type_wise.lower(), names = 'country')
		st.plotly_chart(fig_3)	





st.sidebar.subheader("View by specific country")
type_wise= st.sidebar.selectbox('Choose the Country', arr1)
if not st.sidebar.checkbox("Hide", True, key='5'):
	st.subheader("Number of Confirmed cases in "+type_wise)
	st.write(data[['country','confirmed','active','recovered','deaths']].query("country == @type_wise"))


st.sidebar.subheader("View by new cases") 
type_wise= st.sidebar.selectbox("Select any one!",('New_Cases','New_Deaths','New_Recovered'))
if not st.sidebar.checkbox("Hide", True, key='6'):
	breakdown_type = st.sidebar.selectbox('Visualization type', ['Pie chart', 'Bar plot', ], key='7')
	#st.write(type_wise)]
	if breakdown_type == 'Bar plot':
		st.subheader('Bar-graph for '+type_wise+' cases.')
		fig_4 = px.histogram(data,x='country',
				y=type_wise.lower(), color='country', height=400, width=850)
		st.plotly_chart(fig_4)
	else:	
		st.subheader('Pie Chart for '+type_wise+' cases.')
		fig_4 = px.pie(data, values = type_wise.lower(), names = 'country')
		st.plotly_chart(fig_4)	






st.sidebar.subheader("View by Deaths/Recovered per 100") 
type_wise= st.sidebar.selectbox("Select any one!",('Deaths_per_100_Cases','Recovered_per_100_Cases'))
if not st.sidebar.checkbox("Hide", True, key='8'):
	st.subheader('Bar-graph for '+type_wise+' cases.')
	fig_5 = px.histogram(data,x='country',
				y=type_wise.lower(), color='country', height=400, width=850)
	st.plotly_chart(fig_5)
	





#st.sidebar.subheader("Pie Chart of total cases and in each country")
#st.sidebar.subheader("View by sorted order of maximum cases/Recovered/Deaths/Active")


st.sidebar.subheader("View by number of Countries")
if not st.sidebar.checkbox("Hide", True, key='12'):
	number_of_values = st.sidebar.slider("Number of entries", 5, 190,step = 5)
	st.write(data[:number_of_values])

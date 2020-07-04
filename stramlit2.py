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
	data = pd.read_csv(DATA_URL, nrows=nrows)
	lowercase = lambda x: str(x).lower()
	data.rename(lowercase, axis='columns', inplace=True)
	
	return data


st.title("COVID-19")
# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(10000)
# Notify the reader that the data was successfully loaded.
data_load_state.text('Loading data...done!')	
data.columns = data.columns.str.strip().str.lower().str.replace(' ', '_')




st.sidebar.subheader("Click here to see the Raw data")
if not st.sidebar.checkbox("Hide", True):
	st.subheader('Raw data')
	st.write(data)


list_of_Country = set(data['who_region'])
#st.write(list_of_Country)
arr = [str(i) for i in list_of_Country]



st.sidebar.subheader("Specific country") 
type_wise= st.sidebar.radio('Choose any one!', arr)
#st.write(type_wise)
choice_data = data.query("who_region == @type_wise")
#st.write(choice_data)
if not st.sidebar.checkbox("Hide", True, key='1'):
	st.subheader("Number of cases in region in "+type_wise)
	fig_1 = px.histogram( choice_data, x='country/region',
		y='confirmed',  height=500, width=800,
		labels={'country/region':'Country','sum of confirmed':'Confirmed Cases','who_region':'Region'})
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
		#st.write(choice_data)
		fig_2 = px.histogram( type_wise, x='who_region',
			y='confirmed', color='who_region', height=400, width=850,labels={'who_region':'Regions'})
		st.plotly_chart(fig_2)




st.sidebar.subheader("View for a specific Country:") 
type_wise= st.sidebar.selectbox("Select any!",('Confirmed','Active','Deaths','Recovered'))
if not st.sidebar.checkbox("Hide", True, key='3'):
	breakdown_type = st.sidebar.selectbox('Visualization type', ['Pie chart', 'Bar plot', ], key='4')
	#st.write(type_wise)]
	#if breakdown_type == 'Bar plot':
	#	if type_wise == 'Confirmed':
	#		fig_3 = px.histogram(data,x='country/region',
	#			y='confirmed', color='country/region', height=400, width=850)
	#		st.plotly_chart(fig_3)
	#else:		





st.sidebar.subheader("View by specific country") 
st.sidebar.subheader("View by new cases") 
st.sidebar.subheader("View by deaths/recovered per 100") 
st.sidebar.subheader("Pie Chart of total cases and in each country")
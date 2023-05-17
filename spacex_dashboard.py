import pandas as pd
import requests
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px



def get_data(url : str) -> pd.DataFrame:
	'''
	Import dataset from given URL
	
	Parameters:
		url (String): URL for the dataset

	Returns:
		data (pd.Dataframe): Dataframe containing the dataset
	'''
	conn = requests.get(url)
	if(conn.status_code != 200):
		print('Data not found')
		return None
	data = pd.read_csv(url)
	return data


url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv'
data = get_data(url)
min_payload = data['Payload Mass (kg)'].min()
max_payload = data['Payload Mass (kg)'].max()

app = dash.Dash(__name__)

app.layout = html.Div(children = [html.H1('SpaceX Launch Records Dashboard',
											style = {'textAlign' : 'center',
													 'color': '#503D36',
													 'font-size' : 40}),

								dcc.Dropdown(id = 'site-dropdown',
											options = [{'label' : 'All Sites', 'value' : 'ALL'},
														{'label' : 'CCAFS LC-40', 'value' : 'CCAFS LC-40'},
														{'label' : 'VAFB SLC-4E', 'value' : 'VAFB SLC-4E'},
														{'label' : 'KSC LC-39A', 'value' : 'KSC LC-39A'},
														{'label' : 'CCAFS SLC-40', 'value' : 'CCAFS SLC-40'}],
											value = 'ALL',
											placeholder = 'Select a launch site',
											searchable = True),

								html.Br(),

								html.Div(dcc.Graph(id = 'success-pie-chart')),

								html.Br(),

								html.P('Payload range(Kg): '),

								dcc.RangeSlider(id = 'payload-slider',
												min = 0,
												max = 10000,
												step = 1000,
												value = [min_payload, max_payload]),

								html.Div(dcc.Graph(id = 'success-payload-scatter-chart')),

					])

@app.callback(Output(component_id = 'success-pie-chart', component_property = 'figure'),
			  Input(component_id = 'site-dropdown', component_property = 'value'))

def get_pie_chart(site):
	'''
	Creates a pie chart for the given site

	Parameters: 
		site (str) : Launch site for which the pie chart is to be created

	Returns:
		fig(plotly.express.pie) : Pie chart for the mentioned site
	'''
	if(site == 'ALL'):
		fig = px.pie(data, values = 'class',
					names = 'Launch Site',
					title = 'Pie Chart')
		return fig
	filtered_data = data[data['Launch Site'] == site]
	fig = px.pie(filtered_data, values = filtered_data['class'].value_counts(),
				names = filtered_data['class'].value_counts().index,
				title = site)
	return fig

@app.callback(Output(component_id = 'success-payload-scatter-chart', component_property = 'figure'),
			  Input(component_id = 'site-dropdown', component_property = 'value'),
			  Input(component_id = 'payload-slider', component_property = 'value'))

def get_scatterplot(site, value):
	'''
	Creates a scatter plot for the given site and the range of payload mass values

	Parameters: 
		site (str) : Launch site for which the pie chart is to be created
		value (List[int, int]) : Upper and lower bound for payload mass

	Returns:
		fig(plotly.express.scatter) : Scatter plot for the mentioned site and the range of payload mass
	'''
	if(site == 'ALL'):
		fig = px.scatter(data[(data['Payload Mass (kg)'] >= value[0]) & (data['Payload Mass (kg)'] <= value[1])], y = 'class', x = 'Payload Mass (kg)', color = 'Booster Version Category')
		return fig
	filtered_data = data[data['Launch Site'] == site]
	fig = px.scatter(filtered_data[(filtered_data['Payload Mass (kg)'] >= value[0]) & (filtered_data['Payload Mass (kg)'] <= value[1])], y = 'class', x = 'Payload Mass (kg)', color = 'Booster Version Category')
	return fig
	
if __name__ == '__main__':
	app.run_server()


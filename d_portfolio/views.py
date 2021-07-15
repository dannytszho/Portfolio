from django.shortcuts import render

from .models import Catagory

from django.views.generic.base import TemplateView

import json
import pandas as pd
import datetime 

import plotly.offline as opy
import plotly.graph_objs as go

class Graph(TemplateView):
	template_name = 'd_portfolio/COVID19.html'

	def get_context_data(self, **kwargs):
		context = super(Graph, self).get_context_data(**kwargs)

		all_covid_data = pd.read_json('d_portfolio/COVID19/Data/readable_covid_data.json', lines=False, orient="records",convert_dates=['Date'] ,dtype={"Confirmed":int, "Country/Region":str, "Deaths":int, "Province/State":str, "Recovered":int})
		#all_covid_data['timestamp'] = pd._to_datetime(all_covid_data['Date'])
		all_covid_data = all_covid_data.rename(columns={'Country/Region':"Country"})
		pd.set_option('display.max_columns', None)
		pd.set_option('display.max_rows', None)
		#print(all_covid_data)
		filtered_date = (all_covid_data['Date'] > '2021-04-08')
		all_covid_data = all_covid_data.loc[filtered_date]
		total_cases_list = all_covid_data.groupby('Country')['Confirmed'].sum().tolist()
		#print(total_cases_list)
		deaths_list = all_covid_data.groupby('Country')['Deaths'].sum().tolist()
		#print(deaths_list)
		recovered_cases = all_covid_data.groupby('Country')['Recovered'].sum().tolist()
		#print(recovered_cases)
		country_list = all_covid_data['Country'].tolist()
		country_set = set(country_list)
		country_list = list(country_set)
		country_list.sort()

		new_all_covid_data = pd.DataFrame(list(zip(country_list, total_cases_list, deaths_list, recovered_cases)),
				columns=['Country', 'Total_Cases', 'Deaths_cases','Recovered_cases'])

		data = go.Data([{
			'type':'choropleth',
			'locations': new_all_covid_data['Country'],
			'locationmode':'country names',
			'z': new_all_covid_data['Total_Cases'],
			'text': [f"Deaths: {x}; Recovered:{y}" for x, y in zip(deaths_list, recovered_cases)],
			'colorscale': 'Viridis'
		}])

		my_layout = go.Layout(title="Global COVID19 confirmed cases")

		figure = go.Figure(data=data, layout=my_layout)
		div = opy.plot(figure, auto_open=False, output_type='div')

 
		context['COVID19'] = div
		return context

		def graph_view(request):
			my_graph = Graph()
			context = my_graph.get_context_data()
			return render(request, 'd_portfolio/COVID19.html', context)

def defi(request):
	"""Page for DeFi App."""
	return render(request, 'd_portfolio/defi.html')

def index(request):
	"""Home page for the portfolio."""
	return render(request, 'd_portfolio/index.html')

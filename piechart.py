from forest import forest_result
import plotly.graph_objects as go

#define variables
info = forest_result
features = info[0]
importances = info[1]

#create Pie Chart
fig = go.Figure(data=[go.Pie(labels=features, values=importances)])

#create html file
fig_html = fig.write_html('chart.html')

class pie_html():
	return fig_html

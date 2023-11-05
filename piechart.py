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

<<<<<<< HEAD
def pie_html():
	return fig_html
=======
#class pie_html():
	#return fig_html
>>>>>>> 9e50f44af60296f3cfcd302cdce032787c414aba

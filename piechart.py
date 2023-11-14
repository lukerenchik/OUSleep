import sleepScore, healthScore
import plotly.graph_objects as go



#define variables
sleepScoreValue, sleepScoreComposition = sleepScore.get_sleep_scores_from_file("UserJsonFiles/current_user_data.json")
healthScoreValue, healthScoreComposition = healthScore.get_health_scores_from_file("UserJsonFiles/current_user_data.json")

inner_sleep_dict = next(iter(sleepScoreValue.values()))  # Assuming you're interested in the first key of the outer dictionary
sleep_date_display, sleep_score_display = list(inner_sleep_dict.items())[-1]
inner_health_dict = next(iter(healthScoreValue.values()))
health_date_display, health_score_display = list(inner_health_dict.items())[-1]
        
sleep_score_display = int((round(sleep_score_display, 2))*100)
health_score_display = int((round(health_score_display, 2))*100)

sleep_score_keys = list(sleepScoreComposition.keys())
sleep_score_values = list(sleepScoreComposition.values())


def pie_html():
	return fig_html

#class pie_html():
	#return fig_html

health_score_keys = list(healthScoreComposition.keys())
health_score_values = list(healthScoreComposition.values())

all_scores = [sleep_score_display, health_score_display]

#print(all_scores)

# create Pie Charts
sleep_fig = go.Figure(data=[go.Pie(labels=sleep_score_keys, values=sleep_score_values)])
health_fig = go.Figure(data=[go.Pie(labels=health_score_keys, values=health_score_values)])

# create html files
fig_html = [sleep_fig.to_html(full_html=False), health_fig.to_html(full_html=False)]


class PieHtml:
    def get_fig_html(self):
        return fig_html

    def get_scores_to_display(self):
        return all_scores


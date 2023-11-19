import sleepScore, healthScore
import re
import plotly.graph_objects as go

sleep_score = sleepScore.get_sleep_scores_from_file("JSON Data/updated_data.json")
sleep_res = list(sleep_score['718OS3'].items())[-1]
total_sleep_score, sleep_score_composition = sleep_res[1]

health_score = healthScore.get_health_scores_from_file("JSON Data/updated_data.json")
health_res = list(health_score['718OS3'].items())[-1]
total_health_score, health_score_composition = health_res[1]

sleep_score_keys = list(sleep_score_composition.keys())
sleep_score_values = list(sleep_score_composition.values())

health_score_keys = list(health_score_composition.keys())
health_score_values = list(health_score_composition.values())

all_scores = [total_sleep_score, total_health_score]

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


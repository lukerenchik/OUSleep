import sleepScore, healthScore
import plotly.graph_objects as go

#define variables
total_sleep_score, sleep_score_composition = sleepScore.get_score_data()

sleep_score_keys = list(sleep_score_composition.keys())
sleep_score_values = list(sleep_score_composition.values())

total_health_score, health_score_composition = healthScore.get_score_data()

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

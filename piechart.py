import sleepScore, healthScore
import plotly.graph_objects as go


class PieHtml:
    @staticmethod
    def build_statistics(username):
        sleep_score = sleepScore.get_sleep_scores_from_file("JSON Data/updated_data.json")
        health_score = healthScore.get_health_scores_from_file("JSON Data/updated_data.json")
        if username in sleep_score and health_score:
            # generate sleep figure
            sleep_res = list(sleep_score[username].items())[-1]
            total_sleep_score, sleep_score_composition = sleep_res[1]
            sleep_score_keys = list(sleep_score_composition.keys())
            sleep_score_values = list(sleep_score_composition.values())
            sleep_fig = go.Figure(data=[go.Pie(labels=sleep_score_keys, values=sleep_score_values)])
            # generate health figure
            health_res = list(health_score[username].items())[-1]
            total_health_score, health_score_composition = health_res[1]
            health_score_keys = list(health_score_composition.keys())
            health_score_values = list(health_score_composition.values())
            health_fig = go.Figure(data=[go.Pie(labels=health_score_keys, values=health_score_values)])

            all_scores = [total_sleep_score, total_health_score]
            fig_html = [sleep_fig.to_html(full_html=False), health_fig.to_html(full_html=False)]
            return fig_html, all_scores
        else:
            all_scores = ["Empty", "Empty"]
            fig_html = ["Missing Upload", "Missing Upload"]
            return fig_html, all_scores

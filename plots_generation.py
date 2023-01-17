import os
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.offline as pyo

FIRST_CHILD_COLOR = "green"
SECOND_CHILD_COLOR = "orange"

def generate_line_bar_charts():
    path_cur_dir = os.getcwd()
    path_to_data_first_child = os.path.join(path_cur_dir, "data", "first_child.csv")
    path_to_data_second_child = os.path.join(path_cur_dir, "data", "second_child.csv")

    df_first_child = pd.read_csv(path_to_data_first_child,  parse_dates=['Date'])
    df_second_child = pd.read_csv(path_to_data_second_child,  parse_dates=['Date'])

    # aggregate data
    first_child_agg_df = df_first_child.groupby("Date").agg({" Breastfeeding / min": "sum", "Formula / mL": "sum", " Wet ": "count", "Bowel Movement": "count"}).reset_index()
    second_child_agg_df = df_second_child.groupby("Date").agg({" Breastfeeding / min": "sum", "Formula / mL": "sum", " Wet ": "count", "Bowel Movement": "count"}).reset_index()
    first_child_agg_df["Days Since Born"] = list(first_child_agg_df.index)
    second_child_agg_df["Days Since Born"] = list(second_child_agg_df.index)

    # retrieve column data for plotting
    # first_child 
    days_1 = first_child_agg_df["Days Since Born"]
    breastfeed_1 = first_child_agg_df[" Breastfeeding / min"]
    formula_1 = first_child_agg_df["Formula / mL"]
    wet_1 = first_child_agg_df[" Wet "]
    bowel_mov_1 = first_child_agg_df["Bowel Movement"]

    # second_child 
    days_2 = second_child_agg_df["Days Since Born"]
    breastfeed_2 = second_child_agg_df[" Breastfeeding / min"]
    formula_2 = second_child_agg_df["Formula / mL"]
    wet_2 = second_child_agg_df[" Wet "]
    bowel_mov_2 = second_child_agg_df["Bowel Movement"]

    # breastfeeding and formula line chart
    fig_1 = make_subplots(rows=2, cols=1, subplot_titles = ("Formula Milk Volume (mL)", "Breastfeeding Time (min)"), 
                        shared_xaxes=True,
                        vertical_spacing=0.08)

    first_child_formula_scatter = go.Scatter(x=days_1, y=formula_1, name="First Child",marker = dict(size = 15, symbol = "pentagon", color = FIRST_CHILD_COLOR, line = {'width': 2}), line = dict(width = 3))
    second_child_formula_scatter = go.Scatter(x=days_2, y=formula_2, name="Second Child", marker = dict(size = 15, symbol = "diamond", color = SECOND_CHILD_COLOR, line = {'width': 2}),  line = dict(width = 3))
    first_child_breastfeed_scatter = go.Scatter(x=days_1, y=breastfeed_1, name = 'First Child', marker = dict(size = 15, color = FIRST_CHILD_COLOR, symbol = "pentagon", line = {'width': 2} ), line = dict(width = 3), showlegend = False)
    second_child_breastfeed_scatter = go.Scatter(x=days_2, y=breastfeed_2, name = 'Second Child', marker = dict(size = 15, color = SECOND_CHILD_COLOR, symbol = "diamond", line = {'width': 2} ), line = dict(width = 3), showlegend = False)

    fig_1.append_trace(first_child_formula_scatter, row=1, col=1)
    fig_1.append_trace(second_child_formula_scatter, row=1, col=1)

    fig_1.append_trace(first_child_breastfeed_scatter, row=2, col=1)
    fig_1.append_trace(second_child_breastfeed_scatter, row=2, col=1)

    #fig.update_xaxes(title_text="Days Elapsed Since Born (Days)", row=1, col=1)
    fig_1.update_xaxes(title_text="Time Elapsed Since Born (Days)", row=2, col=1)

    fig_1.update_yaxes(title_text="Volume (mL)", row=1, col=1)
    fig_1.update_yaxes(title_text="Time (min)", row=2, col=1)

    fig_1.update_layout(title_text="Breastfeeding Time and Formula Milk Consumption Since Born")
    
    # Wet diapers and bowel movements bar chart
    fig_2 = make_subplots(rows=2, cols=1, subplot_titles = ("Daily Wet Diapers", "Daily Bowel Movements"), 
                        shared_xaxes=True,
                        vertical_spacing=0.08)

    first_child_wet_bar = go.Bar(x=days_1, y=wet_1, name="First Child", marker = {"color": FIRST_CHILD_COLOR})
    second_child_wet_bar = go.Bar(x=days_2, y=wet_2, name="Second Child", marker = {"color": SECOND_CHILD_COLOR})
    first_child_bowel_mov_bar = go.Bar(x=days_1, y=bowel_mov_1, name = 'First Child', showlegend = False, marker = {"color": FIRST_CHILD_COLOR})
    second_child_bowel_mov_bar = go.Bar(x=days_2, y=bowel_mov_2, name = 'Second Child', showlegend = False, marker = {"color": SECOND_CHILD_COLOR})

    fig_2.append_trace(first_child_wet_bar, row=1, col=1)
    fig_2.append_trace(second_child_wet_bar, row=1, col=1)

    fig_2.append_trace(first_child_bowel_mov_bar, row=2, col=1)
    fig_2.append_trace(second_child_bowel_mov_bar, row=2, col=1)

    fig_2.update_xaxes(title_text="Time Elapsed Since Born (Days)", row=2, col=1)

    fig_2.update_yaxes(title_text="Counts", row=1, col=1)
    fig_2.update_yaxes(title_text="Counts", row=2, col=1)

    fig_2.update_layout(title_text="Total # of Daily Wet Diapers and Bowel Movements Since Born")
    return fig_1, fig_2

if __name__ == '__main__':
    breastfeed_formula_line_chart, wet_diaper_bowel_mov_bar_chart = generate_line_bar_charts()


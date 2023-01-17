import streamlit as st
from plots_generation import generate_line_bar_charts

st.set_page_config(layout = "wide")
st.header("Track Record of Newborn Activities")

breastfeed_formula_line_chart, wet_diaper_bowel_mov_bar_chart = generate_line_bar_charts()

min_days_since_born = float("inf")
max_days_since_born = float("-inf")

for data in breastfeed_formula_line_chart.data:
    min_days_since_born = min(min_days_since_born, min(data.x))
    max_days_since_born = max(max_days_since_born, max(data.x))

for data in wet_diaper_bowel_mov_bar_chart.data:
    min_days_since_born = min(min_days_since_born, min(data.x))
    max_days_since_born = max(max_days_since_born, max(data.x))

# convert np.int64 to int
min_days_since_born = int(min_days_since_born)
max_days_since_born = int(max_days_since_born)

# slider on change
def new_charts_on_slider_change(lower_bound_value, upper_bound_value):
    for data in breastfeed_formula_line_chart.data:
        # change data.x and data.y
        if upper_bound_value >= len(data.x) or lower_bound_value >= len(data.x):
            data.x = []
            data.y = []
        else:
            data.x = data.x[lower_bound_value:upper_bound_value + 1]
            data.y = data.y[lower_bound_value:upper_bound_value + 1]

    for data in wet_diaper_bowel_mov_bar_chart.data:
        # change data.x and data.y
        if upper_bound_value >= len(data.x) or lower_bound_value >= len(data.x):
            data.x = []
            data.y = []
        else:
            data.x = data.x[lower_bound_value:upper_bound_value + 1]
            data.y = data.y[lower_bound_value:upper_bound_value + 1]

def update_charts_color(first_child_color, second_child_color):
    breastfeed_formula_line_chart.data[0].marker.color = first_child_color
    breastfeed_formula_line_chart.data[1].marker.color = second_child_color
    breastfeed_formula_line_chart.data[2].marker.color = first_child_color
    breastfeed_formula_line_chart.data[3].marker.color = second_child_color

    wet_diaper_bowel_mov_bar_chart.data[0].marker.color = first_child_color
    wet_diaper_bowel_mov_bar_chart.data[1].marker.color = second_child_color
    wet_diaper_bowel_mov_bar_chart.data[2].marker.color = first_child_color
    wet_diaper_bowel_mov_bar_chart.data[3].marker.color = second_child_color

# add a slider
days_since_born = st.slider('Which days since born to visualize?', 
                             min_days_since_born, 
                             max_days_since_born, 
                             (min_days_since_born, max_days_since_born))

# update the line chart and bar chart based on slider value
lower_bound_value, upper_bound_value = days_since_born
new_charts_on_slider_change(lower_bound_value, upper_bound_value)

color_container = st.container()
with color_container:
    color_1, color_2 = st.columns(2)
    with color_1:
        first_child_color = st.color_picker('Pick A Color For First Child', '#008000')
    with color_2:
        second_child_color = st.color_picker('Pick A Color For Second Child', '#FFA500')

update_charts_color(first_child_color, second_child_color)

data_container = st.container()
with data_container:
    plot_1, plot_2 = st.columns(2)
    with plot_1:
        # use st.dataframe instead of st.table
        st.plotly_chart(breastfeed_formula_line_chart, use_container_width=True)

    with plot_2:
        st.plotly_chart(wet_diaper_bowel_mov_bar_chart, use_container_width=True)
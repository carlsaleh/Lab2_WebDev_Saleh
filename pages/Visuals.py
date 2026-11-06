# This creates the page for displaying data visualizations.
import streamlit as st
import json
import pandas as pd
import plotly.express as px

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)
# PAGE TITLE
st.title("Data Visualizations 📈")

# PART 1: GRAPHS FROM data.json
# --- YOUR CODE GOES HERE ---
with open("data.json", "r") as file:
    data = json.load(file)
players = data["players"]
df = pd.DataFrame(players)

st.header("2025-2026 Ballon d'Or: Goals and Assists")

fig = px.bar(
    df,
    x="name",
    y=["goals", "assists"],
    barmode="group",
    color_discrete_map={
        "goals": "#D4AF37",
        "assists": "#3498DB"
    },
    labels={
        "name": "Player",
        "value": "Total",
        "variable": "Statistic"
    },
    height=550
)

fig.update_layout(
    xaxis_tickangle=0,
    legend_title_text="Statistics"
)
st.plotly_chart(fig, use_container_width=True)

st.header("Technical Performance Comparison")

st.write("Select the players you want to compare.")

if "selected_players" not in st.session_state:
    st.session_state.selected_players = [
        "Kylian Mbappe",
        "Lamine Yamal"
    ]

player_names = df["name"].tolist()

selected_players = st.multiselect(
    "Choose players:",
    options=player_names,
    key="selected_players"
)

stats = [
    "dribbles_per_90",
    "pass_accuracy",
    "key_passes_per_90",
    "shots_on_target_per_90"
]

selected_df = df[df["name"].isin(selected_players)]

normalized_df = df.copy()

for stat in stats:
    maximum = df[stat].max()

    if maximum > 0:
        normalized_df[stat] = df[stat] / maximum * 100

radar_df = normalized_df[
    normalized_df["name"].isin(selected_players)
]

radar_df = radar_df.melt(
    id_vars="name",
    value_vars=stats,
    var_name="Statistic",
    value_name="Score"
)
radar_df["Statistic"] = radar_df["Statistic"].replace({
    "dribbles_per_90": "Successful Dribbles per 90",
    "pass_accuracy": "Pass Accuracy (%)",
    "key_passes_per_90": "Key Passes per 90",
    "shots_on_target_per_90": "Shots on Target per 90"
})


radar_fig = px.line_polar(
    radar_df,
    r="Score",
    theta="Statistic",
    color="name",
    line_close=True,
    range_r=[0, 100],
    title="Technical Performance Comparison",
    color_discrete_map={
        "Kylian Mbappe": "#FFD700",
        "Harry Kane": "#E74C3C",
        "Michael Olise": "#9B59B6",
        "Ousmane Dembele": "#00BFFF",
        "Erling Haaland": "#2ECC71",
        "Lamine Yamal": "#FF8C00"
    }
)
radar_fig.update_traces(
    fill="toself",
    opacity=0.55,
    line=dict(width=3)
)

st.plotly_chart(radar_fig, use_container_width=True)


if "previous_metrics" not in st.session_state:
    st.session_state.previous_metrics = {}
if "previous_selection" not in st.session_state:
    st.session_state.previous_selection = []

if "saved_deltas" not in st.session_state:
    st.session_state.saved_deltas = {}
st.subheader("Selected Players: Summary Statistics")

if len(selected_players) > 0:

    mean_goals = selected_df["goals"].mean()
    median_goals = selected_df["goals"].median()
    mean_assists = selected_df["assists"].mean()
    median_assists = selected_df["assists"].median()

    current_metrics = {
        "mean_goals": mean_goals,
        "median_goals": median_goals,
        "mean_assists": mean_assists,
        "median_assists": median_assists
    }

    deltas = {}
    selection_changed = (
        selected_players != st.session_state.previous_selection
    )
    for metric, value in current_metrics.items():
        previous = st.session_state.previous_metrics.get(metric)

        if previous is None:
            deltas[metric] = None
        elif selection_changed:
            deltas[metric] = round(value - previous, 2)
        else:
            deltas[metric] = st.session_state.saved_deltas.get(metric)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            label="Mean Goals",
            value=f"{mean_goals:.2f}",
            delta=deltas["mean_goals"]
        )
    with col2:
        st.metric(
            label="Median Goals",
            value=f"{median_goals:.2f}",
            delta=deltas["median_goals"]
        )
    with col3:
        st.metric(
            label="Mean Assists",
            value=f"{mean_assists:.2f}",
            delta=deltas["mean_assists"]
        )
    with col4:
        st.metric(
            label="Median Assists",
            value=f"{median_assists:.2f}",
            delta=deltas["median_assists"]
        )
    st.session_state.previous_metrics = current_metrics.copy()
    st.session_state.previous_selection = selected_players.copy()
    st.session_state.saved_deltas = deltas.copy()
else:
    st.info("Select at least one player to see the statistics.")
    st.session_state.previous_metrics = {}

# PART 2: GRAPHS FROM data.csv
# --- YOUR CODE GOES HERE ---

st.divider()
st.header("Ballon d'Or Fan Survey Results")
survey_df = pd.read_csv("data.csv")
vote_counts = survey_df["Category"].value_counts()

pie_fig = px.pie(
    names=vote_counts.index,
    values=vote_counts.values,
    title="Ballon d'Or Fan Votes",
    hole=0.3
)
st.plotly_chart(pie_fig, use_container_width=True)


st.subheader("Average Fan Ratings Comparison")
st.write("Select the players you want to compare based on fan ratings.")


average_ratings = survey_df.groupby("Category")["Value"].mean()
rated_players = average_ratings.index.tolist()

if "selected_fan_players" not in st.session_state:
    st.session_state.selected_fan_players = rated_players.copy()

selected_fan_players = st.multiselect(
    "Choose players to compare:",
    options=rated_players,
    key="selected_fan_players"
)


if len(selected_fan_players) > 0:
    filtered_ratings = average_ratings[
        average_ratings.index.isin(selected_fan_players)
    ]
    bar_fig = px.bar(
        x=filtered_ratings.index,
        y=filtered_ratings.values,
        labels={"x": "Player", "y": "Average Fan Rating"},
        title="Average Fan Ratings by Player",
        color=filtered_ratings.index,
        range_y=[0, 10]
    )
    st.plotly_chart(bar_fig, use_container_width=True)
else:
    st.warning("Please select at least one player to display the chart.")



st.subheader("Selected Players: Fan Rating Statistics")

if "previous_fan_metrics" not in st.session_state:
    st.session_state.previous_fan_metrics = {}

if "previous_fan_selection" not in st.session_state:
    st.session_state.previous_fan_selection = []

if "saved_fan_deltas" not in st.session_state:
    st.session_state.saved_fan_deltas = {}

if len(selected_fan_players) > 0:
    selected_votes = survey_df[
        survey_df["Category"].isin(selected_fan_players)
    ]

    mean_rating = selected_votes["Value"].mean()
    median_rating = selected_votes["Value"].median()

    current_fan_metrics = {
        "mean": mean_rating,
        "median": median_rating
    }

    selection_changed = (
        selected_fan_players != st.session_state.previous_fan_selection
    )

    fan_deltas = {}

    for metric, value in current_fan_metrics.items():
        previous = st.session_state.previous_fan_metrics.get(metric)

        if previous is None:
            fan_deltas[metric] = None
        elif selection_changed:
            fan_deltas[metric] = round(value - previous, 2)
        else:
            fan_deltas[metric] = st.session_state.saved_fan_deltas.get(metric)

    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            label="Mean Fan Rating",
            value=f"{mean_rating:.2f}/10",
            delta=fan_deltas["mean"]
        )
    with col2:
        st.metric(
            label="Median Fan Rating",
            value=f"{median_rating:.2f}/10",
            delta=fan_deltas["median"]
        )
    st.session_state.previous_fan_metrics = current_fan_metrics.copy()
    st.session_state.previous_fan_selection = selected_fan_players.copy()
    st.session_state.saved_fan_deltas = fan_deltas.copy()
else:
    st.info("Select at least one player to see fan rating statistics.")
    st.session_state.previous_fan_metrics = {}
    st.session_state.previous_fan_selection = []
    st.session_state.saved_fan_deltas = {}

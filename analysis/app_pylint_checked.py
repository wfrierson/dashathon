import pandas as pd
import numpy as np
import plotly.graph_objs as go

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html


"""This module creates an interactive dashboard that allows users to explore
marathon finisher data and compare their own split times to the finishers'."""

SECONDS = 60.0

EXTERNAL_STYLESHEETS = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=EXTERNAL_STYLESHEETS)

df = pd.read_csv("C:\\Users\\halli_000\\Desktop\\marathon\\boston_all_years_nan.csv")


# pull the list of demographic variables from the data itself
# include 'all' so user can view data without slicing it
genders = df["gender"].unique()
genders = np.append(genders, ["all"])
ages = df["age_range"].unique()
ages = np.append(ages, ["all"])


app.layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        dcc.Dropdown(
                            id="gender_select",
                            options=[{"label": g, "value": g} for g in genders],
                            value="all",
                        )
                    ],
                    style={"width": "48%", "display": "inline-block"},
                ),
                html.Div(
                    [
                        dcc.Dropdown(
                            id="age_select",
                            options=[{"label": a, "value": a} for a in ages],
                            value="all",
                        )
                    ],
                    style={"width": "48%", "float": "right", "display": "inline-block"},
                ),
                dcc.Input(id="5k-input", type="text", value="5k split", size="8"),
                dcc.Input(id="10k-input", type="text", value="10k split", size="8"),
                dcc.Input(id="15k-input", type="text", value="15k split", size="8"),
                dcc.Input(id="20k-input", type="text", value="20k split", size="8"),
                dcc.Input(id="half-input", type="text", value="half split", size="8"),
                dcc.Input(id="25k-input", type="text", value="25k split", size="8"),
                dcc.Input(id="30k-input", type="text", value="30k split", size="8"),
                dcc.Input(id="35k-input", type="text", value="35k split", size="8"),
                dcc.Input(id="40k-input", type="text", value="40k split", size="8"),
                html.Button(id="submit-button", n_clicks=0, children="Submit"),
                html.Div(id="output-state"),
            ]
        ),
        dcc.Graph(id="indicator-graphic"),
        dcc.Graph(id="split-hist"),
    ]
)


@app.callback(
    Output("indicator-graphic", "figure"),
    [Input("submit-button", "n_clicks")],
    [
        State("gender_select", "value"),
        State("age_select", "value"),
        State("5k-input", "value"),
        State("10k-input", "value"),
        State("15k-input", "value"),
        State("20k-input", "value"),
        State("half-input", "value"),
        State("25k-input", "value"),
        State("30k-input", "value"),
        State("35k-input", "value"),
        State("40k-input", "value"),
    ],
)
def update_graph(
    n_clicks,
    gender_,
    age_,
    user5k,
    user10k,
    user15k,
    user20k,
    userhalf,
    user25k,
    user30k,
    user35k,
    user40k,
):
    """
    This function updates the line graph based on user's demographic selection
    and input split times when the submit button is pressed.
    """
    # subset the data based on user's age and gender selection
    if age_ == "all":
        if gender_ == "all":
            subset = df
        else:
            subset = df.loc[(df["gender"] == str(gender_))]
    elif gender_ == "all":
        subset = df.loc[(df["age_range"] == str(age_))]
    else:
        subset = df.loc[(df["gender"] == str(gender_)) & (df["age_range"] == age_)]

    # select the top performers from the selected demographic
    quantile_value = subset["overall"].quantile(0.1)
    subset_winners = subset.loc[(subset["overall"] <= quantile_value)]

    # create variables needed to interpret user's split data
    split_list = [
        "5k",
        "10k",
        "15k",
        "20k",
        "half",
        "25k",
        "30k",
        "35k",
        "40k",
        "overall",
    ]
    split_numeric = [5, 10, 15, 20, 21.082, 25, 30, 35, 40, 42.165]
    mean_paces = []
    mean_paces_w = []
    user_paces = [
        user5k,
        user10k,
        user15k,
        user20k,
        userhalf,
        user25k,
        user30k,
        user35k,
        user40k,
    ]
    user_numeric = []

    # take user's splits as text input, interpret numerically, and report
    # pace in minutes per km
    for i in range(len(user_paces)):
        try:
            numbers = user_paces[i].split(":")
            if len(numbers) == 2:
                mins = float(numbers[0])
                secs = float(numbers[1]) / SECONDS
                user_numeric.append((mins + secs) / split_numeric[i])
            elif len(numbers) == 3:
                hours = float(numbers[0]) * SECONDS
                mins = float(numbers[1])
                secs = float(numbers[2]) / SECONDS
                user_numeric.append((hours + mins + secs) / split_numeric[i])
            else:
                user_numeric.append(np.nan)
        # in case of ANY failure simply insert a nan for this split
        except Exception:
            user_numeric.append(np.nan)

    # find the mean pace for each split for the selected demographic
    # and for the top performers in taht demographic
    for i in range(len(split_list) - 1):
        mean_time = subset[split_list[i]].mean(axis=0) / SECONDS
        mean_pace = mean_time / split_numeric[i]
        mean_paces.append(mean_pace)
        mean_time_w = subset_winners[split_list[i]].mean(axis=0) / SECONDS
        mean_pace_w = mean_time_w / split_numeric[i]
        mean_paces_w.append(mean_pace_w)

        # create a trace for the selected demographic
        trace_historic_data = go.Scatter(
            x=split_list,
            y=mean_paces,
            name="selected demographic average pace",
            mode="lines+markers",
            line=dict(color="yellowgreen", width=2),
        )

        # create a trace for the top performers in the selected demographic
        trace_historic_winners = go.Scatter(
            x=split_list,
            y=mean_paces_w,
            name="demographic top 10% average pace",
            mode="lines+markers",
            line=dict(color="gold", width=2),
        )

        # create a trace for the user submitted data
        trace_user_data = go.Scatter(
            x=split_list,
            y=user_numeric,
            name="user pace",
            mode="lines+markers",
            line=dict(color="skyblue", width=2),
        )

        # create a second trace for the user to connect submitted splits
        # across distances which do not have data; display dashed line
        trace_user_data_extrap = go.Scatter(
            x=split_list,
            y=user_numeric,
            name="user pace",
            mode="lines+markers",
            connectgaps=True,
            showlegend=False,
            line=dict(color="skyblue", width=2, dash="dot"),
        )

    return {
        # display all traces on the shared, fixed axes
        "data": [
            trace_historic_data,
            trace_historic_winners,
            trace_user_data,
            trace_user_data_extrap,
        ],
        "layout": go.Layout(
            xaxis={"title": "splits"},
            yaxis=dict(range=[10, 3], title="average pace in minutes/km"),
            margin={"l": 40, "b": 40, "t": 10, "r": 0},
            hovermode="closest",
        ),
    }


@app.callback(
    Output("split-hist", "figure"),
    [Input("submit-button", "n_clicks")],
    [
        State("gender_select", "value"),
        State("age_select", "value"),
        State("5k-input", "value"),
        State("10k-input", "value"),
        State("15k-input", "value"),
        State("20k-input", "value"),
        State("half-input", "value"),
        State("25k-input", "value"),
        State("30k-input", "value"),
        State("35k-input", "value"),
        State("40k-input", "value"),
    ],
)
def update_hist(
    n_clicks,
    gender_,
    age_,
    user5k,
    user10k,
    user15k,
    user20k,
    userhalf,
    user25k,
    user30k,
    user35k,
    user40k,
):
    """
    This function updates the histograms based on user's demographic selection
    and input half and full marathon times when the submit button is pressed.
    """
    
    # subset the data based on user's age and gender selection
    if age_ == "all":
        if gender_ == "all":
            subset = df.copy()
        else:
            subset = df.loc[(df["gender"] == str(gender_))].copy()
    elif gender_ == "all":
        subset = df.loc[(df["age_range"] == str(age_))].copy()
    else:
        subset = df.loc[
            (df["gender"] == str(gender_)) & (df["age_range"] == age_)
        ].copy()

    # select the top performers from the selected demographic
    quantile_value = subset["overall"].quantile(0.1)
    subset_winners = subset.loc[(subset["overall"] <= quantile_value)].copy()

    # find the split ratios for the selected demographic and top performers
    subset["split_ratio"] = (subset["official_time"] - subset["half"]) / (
        subset["half"]
    )
    subset_winners["split_ratio"] = (
        subset_winners["official_time"] - subset_winners["half"]
    ) / (subset_winners["half"])

    # create variables needed to interpret user's split data
    user_paces = [
        user5k,
        user10k,
        user15k,
        user20k,
        userhalf,
        user25k,
        user30k,
        user35k,
        user40k,
    ]
    user_numeric_time = []

    # take user's splits as text input, interpret numerically, and report
    # pace in minutes per km
    for i in range(len(user_paces)):
        try:
            numbers = user_paces[i].split(":")
            if len(numbers) == 2:
                mins = float(numbers[0])
                secs = float(numbers[1]) / SECONDS
                user_numeric_time.append(mins + secs)
            elif len(numbers) == 3:
                hours = float(numbers[0]) * SECONDS
                mins = float(numbers[1])
                secs = float(numbers[2]) / SECONDS
                user_numeric_time.append(hours + mins + secs)
            else:
                user_numeric_time.append(np.nan)
        # in case of ANY failure simply insert a nan for this split
        except Exception:
            user_numeric_time.append(np.nan)

    # find the user's split ratio only if they have provided a full marathon
    # time and a half marathon time
    try:
        user_first_half = user_numeric_time[4]
        user_second_half = user_numeric_time[8] - user_first_half
        user_x = float(user_second_half / user_first_half)
        user_y = 3000
    except:
        user_x = 0
        user_y = 0

    # create a histogram for split ratios of the selected demographic
    trace_demo_hist = go.Histogram(
        x=subset["split_ratio"],
        opacity=0.5,
        name="selcted demographic",
        marker=dict(color="yellowgreen"),
        histnorm="probability",
    )

    # create a histogram for split ratios of the top performers
    trace_winners_hist = go.Histogram(
        x=subset_winners["split_ratio"],
        opacity=0.5,
        name="top 10% of selcted demographic",
        marker=dict(color="gold"),
        histnorm="probability",
    )

    # display both histograms and a vertical line giving the user's split ratio
    # on shared, unfixed axes
    return {
        "data": [trace_demo_hist, trace_winners_hist],
        "layout": go.Layout(
            xaxis=dict(title="split ratio distribution", range=[-0.5, 2]),
            yaxis=dict(title="percent of group"),
            barmode="overlay",
            shapes=[
                {
                    "type": "line",
                    "xref": "x",
                    "yref": "paper",
                    "x0": user_x,
                    "x1": user_x,
                    "y0": 0,
                    "y1": user_y,
                    "line": {"color": "skyblue", "width": 3},
                }
            ],
        ),
    }


if __name__ == "__main__":
    app.run_server(debug=False)

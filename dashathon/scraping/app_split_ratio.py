import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import pandas as pd
import numpy as np
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv(
    'C:\\Users\\halli_000\\Desktop\\marathon\\boston_all_years_nan.csv')

genders = df['gender'].unique()
genders = np.append(genders, ['all'])
ages = df['age_range'].unique()
ages = np.append(ages, ['all'])


app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='gender_select',
                options=[{'label': i, 'value': i} for i in genders],
                value='all'
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='age_select',
                options=[{'label': i, 'value': i} for i in ages],
                value='all'
            )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),
    
        dcc.Input(id='5k-input', type='text', value='5k split', size='8'),
        dcc.Input(id='10k-input', type='text', value='10k split', size='8'),
        dcc.Input(id='15k-input', type='text', value='15k split', size='8'),
        dcc.Input(id='20k-input', type='text', value='20k split', size='8'),
        dcc.Input(id='half-input', type='text', value='half split', size='8'),
        dcc.Input(id='25k-input', type='text', value='25k split', size='8'),
        dcc.Input(id='30k-input', type='text', value='30k split', size='8'),
        dcc.Input(id='35k-input', type='text', value='35k split', size='8'),
        dcc.Input(id='40k-input', type='text', value='40k split', size='8'),
        html.Button(id='submit-button', n_clicks=0, children='Submit'),
        html.Div(id='output-state')
    
    ]),

    dcc.Graph(id='indicator-graphic'),
    dcc.Graph(id='split-hist')

])

@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('submit-button', 'n_clicks')],
     [State('gender_select', 'value'),
     State('age_select', 'value'),
     State('5k-input', 'value'),
     State('10k-input', 'value'),
     State('15k-input', 'value'),
     State('20k-input', 'value'),
     State('half-input', 'value'),
     State('25k-input', 'value'),
     State('30k-input', 'value'),
     State('35k-input', 'value'),
     State('40k-input', 'value')])

def update_graph(n_clicks, gender_, age_, user5k, user10k, user15k, user20k,
                 userhalf, user25k, user30k, user35k, user40k):
    
    if (age_ == 'all'):
        if (gender_ == 'all'):
            subset = df
        else:
            subset = df.loc[(df['gender'] == str(gender_))]
    elif (gender_ == 'all'):
        subset = df.loc[(df['age_range'] == str(age_))]
    else:
        subset = df.loc[(df['gender'] == str(gender_)) & (df['age_range'] == age_)]
        
    quantile_value = subset['overall'].quantile(.1) 
    subset_winners = subset.loc[(subset['overall'] <= quantile_value)]

    split_list = ['5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k', '40k', 'overall']
    split_numeric = [5, 10, 15, 20, 21.082, 25, 30, 35, 40, 42.165]
    mean_paces = []
    mean_paces_w = []
    
    user_paces = [user5k, user10k, user15k, user20k,
                 userhalf, user25k, user30k, user35k, user40k]
    user_numeric= []
    
    for i in range (len(user_paces)):
        try:
            numbers = user_paces[i].split(':')
            mins = float(numbers[0])
            secs = float(numbers[1])/60
            user_numeric.append((mins+secs)/split_numeric[i])
        except:
            user_numeric.append(np.nan)
    
    for i in range(len(split_list)-1):
        mean_time = subset[split_list[i]].mean(axis=0)/60.0
        mean_pace = mean_time/split_numeric[i]
        mean_paces.append(mean_pace)
        mean_time_w = subset_winners[split_list[i]].mean(axis=0)/60.0
        mean_pace_w = mean_time_w/split_numeric[i]
        mean_paces_w.append(mean_pace_w)

        trace_historic_data = go.Scatter(
            x = split_list,
            y = mean_paces,
            name = 'selected demographic average pace',
            mode = 'lines+markers',
            line = dict(
                    color = 'yellowgreen',
                    width = 2
            )
        )
            
        trace_historic_winners = go.Scatter(
            x = split_list,
            y = mean_paces_w,
            name = 'demographic top 10% average pace',
            mode = 'lines+markers',
            line = dict(
                    color = 'gold',
                    width = 2
            )
        )
        
        trace_user_data = go.Scatter(
            x = split_list,
            y = user_numeric,
            name = 'user pace',
            mode = 'lines+markers',
            line = dict(
                    color = 'skyblue',
                    width = 2
            )
        )
        
        trace_user_data_extrap = go.Scatter(
            x = split_list,
            y = user_numeric,
            name = 'user pace',
            mode = 'lines+markers',
            connectgaps = True,
            showlegend=False,
            line = dict(
                    color = 'skyblue',
                    width = 2,
                    dash = 'dot'
            )
        )

    return {
        
        'data': [trace_historic_data, trace_historic_winners, trace_user_data, trace_user_data_extrap],
        'layout': go.Layout(
            xaxis={
                'title': 'splits'
            },
            yaxis=dict(
                range=[10, 3],
                title = 'average pace in minutes/km'
            ),
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }

@app.callback(
    Output('split-hist', 'figure'),
    [Input('submit-button', 'n_clicks')],
     [State('gender_select', 'value'),
     State('age_select', 'value'),
     State('5k-input', 'value'),
     State('10k-input', 'value'),
     State('15k-input', 'value'),
     State('20k-input', 'value'),
     State('half-input', 'value'),
     State('25k-input', 'value'),
     State('30k-input', 'value'),
     State('35k-input', 'value'),
     State('40k-input', 'value')])

def update_hist(n_clicks, gender_, age_, user5k, user10k, user15k, user20k,
                 userhalf, user25k, user30k, user35k, user40k):
    if (age_ == 'all'):
        if (gender_ == 'all'):
            subset = df.copy()
        else:
            subset = df.loc[(df['gender'] == str(gender_))].copy()
    elif (gender_ == 'all'):
        subset = df.loc[(df['age_range'] == str(age_))].copy()
    else:
        subset = df.loc[(df['gender'] == str(gender_)) & (df['age_range'] == age_)].copy()
    
    quantile_value = subset['overall'].quantile(.9)
    subset_winners = subset.loc[(subset['overall'] <= quantile_value)].copy()
    
    subset['split_ratio'] = (subset['official_time'] - subset['half']) / (subset['half'])
    subset_winners['split_ratio'] = (subset_winners['official_time'] - subset_winners['half']) / (subset_winners['half'])
    
    user_paces = [user5k, user10k, user15k, user20k,
                 userhalf, user25k, user30k, user35k, user40k]
    user_numeric_time = []
    
    for i in range (len(user_paces)):
        try:
            numbers = user_paces[i].split(':')
            mins = float(numbers[0])
            secs = float(numbers[1])/60
            user_numeric_time.append(mins+secs)
        except:
            user_numeric_time.append(np.nan)
    
    try:
        user_first_half = user_numeric_time[4]
        user_second_half = user_numeric_time[8] - user_first_half
        user_x = float(user_second_half / user_first_half)
        user_y = 3000
    except:
        user_x = 0
        user_y = 0
        
    trace_demo_hist = go.Histogram(
        x = subset['split_ratio'],
        opacity = 0.5,
        name='selcted demographic',
        marker = dict(
            color = 'yellowgreen',
        )
    )
            
    trace_winners_hist = go.Histogram(
        x = subset_winners['split_ratio'],
        opacity = 0.5,
        name='top 10% of selcted demographic',
        marker = dict(
            color = 'gold',
        )
    )
    
    return {
        
        'data': [trace_demo_hist, trace_winners_hist],
        'layout': go.Layout(
                xaxis = dict(
                    title = 'split ratio distribution',
                    range = [-0.5, 2]
                ),
                yaxis = dict(
                    title = 'individuals',
                ),
                barmode = 'overlay',
                shapes = [{
                    'type' : 'line',
                    'xref': 'x',
                    'yref': 'paper',
                    'x0' : user_x,
                    'x1' : user_x,
                    'y0' : 0,
                    'y1' : user_y,
                    'line': {
                        'color' : 'skyblue',
                        'width' : 3,
                    },
                }],
        )
    }


if __name__ == '__main__':
    app.run_server(debug=False)

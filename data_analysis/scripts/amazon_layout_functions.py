import dash_bootstrap_components as dbc  # pip install dash-bootstrap-components
import dash_daq as daq
from dash import html, dcc  # pip install dash

from amazon_mongo import select_max_and_min_dates
from amazon_layout_utils import get_min_date_from_max_date_minus_x_days
from amazon_ML_constants import algorithms_options, features, feature_columns_opt


def serve_layout():
    min_date, max_date = select_max_and_min_dates()
    return dbc.Container([
        html.H1("Interactive Amazon Buy Box Analysis", className='mb-2', style={'text-align': 'center'}),
        html.Hr(),
        html.H2("Input Data to Machine Learning Analysis", className='mb-2', style={'text-align': 'left'}),
        build_input_section(max_date, min_date),

        html.Label("Machine Learning Algorithm to use:",
                   title="'ALL ALGORITHMS' option applies all algorithms and return the average accuracy"),
        dcc.Dropdown(
            id='algorithm',
            clearable=False,
            options=algorithms_options,
            value=algorithms_options[0]
        ),
        html.Br(),

        html.Br(),
        html.Div(
            [
                html.Button(id='submit-button-state', n_clicks=0, children='Execute Machine Learning Analysis'),
                html.Br(),
                html.Progress(id="progress_bar")
            ],
            style={'text-align': 'center'}  # Allinea il contenuto al centro
        ),
        dcc.Loading(
            [
                html.Hr(),
                build_output_section()
            ],
            overlay_style={"visibility": "visible", "filter": "blur(2px)"},
            type="circle",
        )
    ])


def build_input_section(max_date, min_date):
    return html.Div([
        html.Div([
            html.Label("Observation Period: "),
            dcc.DatePickerRange(
                id='my-date-picker-range',
                min_date_allowed=min_date, max_date_allowed=max_date,
                display_format='DD-MM-Y',
                start_date=get_min_date_from_max_date_minus_x_days(max_date, 7), end_date=max_date,
                style={'margin': '0px 0px 0px 10px'}
            ),
            html.Br(),
            html.Label('Features to consider: '),
            dcc.Dropdown(
                id='dropdown_features',
                options=features,
                value=feature_columns_opt,
                multi=True
            ),
            html.Div([
                html.Div([
                    html.Label("Filter Amazon as BuyBox winner: ",
                               title="Observations having Amazon as BuyBox winner are filtered"),
                    dcc.RadioItems(
                        id='radio-amazon-bb',
                        options=[{'label': 'Yes', 'value': True}, {'label': 'No', 'value': False}],
                        value=False
                    )
                ], style={'padding': 10, 'flex': 1}),
                html.Div([
                    html.Label("Filter Amazon as non-BuyBox winner: ",
                               title="Only the other sellers having Amazon as Non-BuyBox winner are filtered"),
                    dcc.RadioItems(
                        id='radio-amazon-nbb',
                        options=[{'label': 'Yes', 'value': True}, {'label': 'No', 'value': False}],
                        value=False
                    )
                ], style={'padding': 10, 'flex': 1}),
                html.Div([
                    html.Label("Filter New Seller as BuyBox winner: ",
                               title="Observations having new sellers as BuyBox winner are filtered"),
                    dcc.RadioItems(
                        id='radio-new-bb',
                        options=[{'label': 'Yes', 'value': True}, {'label': 'No', 'value': False}],
                        value=False
                    )
                ], style={'padding': 10, 'flex': 1}),
                html.Div([
                    html.Label("Filter New Seller as non-BuyBox winner: ",
                               title="Only the other sellers having new seller as Non-BuyBox winner are filtered"),
                    dcc.RadioItems(
                        id='radio-new-nbb',
                        options=[{'label': 'Yes', 'value': True}, {'label': 'No', 'value': False}],
                        value=False
                    )
                ], style={'padding': 10, 'flex': 1})
            ], style={'display': 'flex', 'flexDirection': 'row'})

        ], style={'padding': 10, 'flex': 1}),

        html.Div([
            html.Label("Minimum Number of sellers: ",
                       title="Observations having sellers less than this count are filtered"),
            dcc.Slider(
                3, 10,
                step=None,
                value=8,
                marks={str(num): str(num) for num in range(3, 11)},
                id='seller-count'
            ),
            html.Br(),
            html.Label("Number of non-buybox winner sellers to consider: ",
                       title="Last ones as Non-BuyBox winner are filtered"),
            dcc.Slider(
                3, 10,
                step=None,
                value=8,
                marks={str(num): str(num) for num in range(3, 11)},
                id='nbb-seller-count'
            ),
            html.Br(),
            html.Label("Cross Validation Option: ",
                       title="Select the cross validation option to apply on Machine Learning analysis"),
            dcc.RadioItems(
                id='radio-cv-option',
                options=[
                    {'label': ' Hold-out (select test size)', 'value': 0},
                    {'label': ' k-Fold (10 splits)', 'value': 1},
                    {'label': ' Stratified k-Fold (10 splits)', 'value': 2},
                    {'label': ' Repeated k-Fold (10 splits, 3 repeats)', 'value': 3}
                ],
                value=3
            ),
            html.Br(),
            html.Div(id="test-size-div",
                     children=[
                         html.Label("Test size for Machine Learning algorithm: "),
                         dcc.Slider(
                             0.0, 0.4, 0.1,
                             value=0.2,
                             id='test-size'
                         )
                     ], style={'display': 'none'}),
        ], style={'padding': 10, 'flex': 1})

    ], style={'display': 'flex', 'flexDirection': 'row'})


def build_output_section():
    return html.Div(
        id="output-div",
        children=[
            html.H2("Output Data & Graphs", className='mb-2', style={'text-align': 'left'}),
            html.Div(id='output-state'),  # Non visualizzato, ma stampato nella console
            html.Br(),
            html.Div([
                html.Div([
                    html.H3("Normalized Features Dataset Describe Table", className='mb-2',
                            style={'text-align': 'center'}),
                    html.Div(id='normalized-features-stats')
                ], style={'padding': 10, 'flex': 1}),
                html.Div([
                    html.H3("Features Dataset Describe Table", className='mb-2', style={'text-align': 'center'}),
                    html.Div(id='features-stats')
                ], style={'padding': 10, 'flex': 1})
            ], style={'display': 'flex', 'flexDirection': 'row'}),

            html.Br(),

            html.Div([
                html.Div([
                    html.H3("Buy Box Winners", className='mb-2', style={'text-align': 'center'}),
                    dcc.Graph(id='buybox-winners-pie', style={'height': '400px'})
                ], style={'padding': 10, 'flex': 1}),
                html.Div([
                    html.H3("Accuracy Score", className='mb-2', style={'text-align': 'center'},
                            title="Average Accuracy Score if 'ALL ALGORITHMS' option selected"),
                    daq.Gauge(
                        id="accuracy-score-label",
                        color={"gradient": True,
                               "ranges": {"red": [0, 65], "orange": [65, 80], "yellow": [80, 95], "green": [95, 100]}},
                        value=0,
                        label=' ',
                        showCurrentValue=True,
                        units="%",
                        max=100,
                        min=0,
                        size=300
                    )
                ], style={'padding': 10, 'flex': 1})
            ], style={'display': 'flex', 'flexDirection': 'row'}),
            html.Br(),
            html.H3("Features Importance Table", className='mb-2', style={'text-align': 'center'}),
            html.Div(id='importance-features-stats'),
            html.Br(),
            html.H3("Features Importance Graph", className='mb-2', style={'text-align': 'center'}),
            dcc.Graph(id='graph-ml-analysis')
        ],
        style={'display': 'none'})

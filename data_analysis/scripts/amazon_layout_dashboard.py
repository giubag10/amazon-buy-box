import logging

import dash_bootstrap_components as dbc  # pip install dash-bootstrap-components
import matplotlib  # pip install matplotlib
from dash import Dash, Input, Output, State, no_update  # pip install dash

from amazon_data_filters import apply_filters
from amazon_data_normalizer import normalize_amazon_data, calculate_statistics_on_df
from amazon_data_reader import import_data_to_analyze
from amazon_layout_functions import serve_layout
from amazon_layout_utils import generate_all_ml_graphics, generate_ml_graphics, generate_feature_stats, \
    generate_pie_chart
from amazon_ML_constants import all_algorithms

matplotlib.use('agg')
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = serve_layout


@app.callback(
    Output('output-state', 'children'),
    Output('output-div', 'style'),
    Output('normalized-features-stats', 'children'),
    Output('features-stats', 'children'),
    Output('accuracy-score-label', 'value'),
    Output('buybox-winners-pie', 'figure'),
    Output('graph-ml-analysis', 'figure'),
    Output('importance-features-stats', 'children'),
    Input('submit-button-state', 'n_clicks'),
    State('algorithm', 'value'),
    State('my-date-picker-range', 'start_date'),
    State('my-date-picker-range', 'end_date'),
    State('seller-count', 'value'),
    State('nbb-seller-count', 'value'),
    State('test-size', 'value'),
    State('radio-amazon-bb', 'value'),
    State('radio-amazon-nbb', 'value'),
    State('radio-new-bb', 'value'),
    State('radio-new-nbb', 'value'),
    State('dropdown_features', 'value')
)
def update_output(n_clicks, algorithm, start_date, end_date, seller_count, nbb_seller_count, test_size, radio_amazon_bb,
                  radio_amazon_nbb, radio_new_bb, radio_new_nbb, dropdown_features):
    # Utile per debug: non viene esposto (si passa in output no_update)
    output_state = f'''
        The Button has been pressed {n_clicks} times,
        Algorithm: "{algorithm}"\n
        Date-Range: "{start_date}-{end_date}"\n
        Seller Count: "{seller_count}"\n
        NBB Seller Count: "{nbb_seller_count}"\n
        Test Size: "{test_size}"\n
        Amazon BuyBox winner included: "{radio_amazon_bb}"\n
        Amazon NBB Seller included: "{radio_amazon_nbb}"\n
        New Seller BuyBox winner included: "{radio_new_bb}"\n
        New Seller NBB included: "{radio_new_nbb}"\n
        Features: "{dropdown_features}"\n
    '''
    logging.info(output_state)
    if n_clicks == 0:
        return no_update, {'display': 'none'}, no_update, no_update, no_update, no_update, no_update

    amazon_data = import_data_to_analyze(start_date, end_date, True, False)

    # Dati non normalizzati: utili per le label reali
    filtered_data = apply_filters(amazon_data, start_date, end_date, seller_count, nbb_seller_count, radio_amazon_bb,
                                  radio_amazon_nbb, radio_new_bb, radio_new_nbb)

    # Dati normalizzati: utili per i calcoli di ML
    filtered_normalized_data = normalize_amazon_data(filtered_data)

    data_statistics_df = calculate_statistics_on_df(filtered_normalized_data)
    buybox_winners_pie = generate_pie_chart(data_statistics_df)

    feature_stats = generate_feature_stats(dropdown_features, filtered_data)
    normalized_feature_stats = generate_feature_stats(dropdown_features, filtered_normalized_data)

    if algorithm == all_algorithms:
        accuracy_label, graph_ml_analysis, importance_features_stats = (
            generate_all_ml_graphics(dropdown_features,
                                     filtered_normalized_data,
                                     test_size))
    else:
        accuracy_label, graph_ml_analysis, importance_features_stats = (
            generate_ml_graphics(algorithm,
                                 dropdown_features,
                                 filtered_normalized_data,
                                 test_size))

    return (
            no_update,
            {'display': 'block'},  # Visualizza la sezione di output
            normalized_feature_stats, feature_stats, accuracy_label, buybox_winners_pie, graph_ml_analysis,
            importance_features_stats)


if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=8082)

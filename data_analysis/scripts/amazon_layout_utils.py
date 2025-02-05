import datetime
import statistics

import plotly.express as px
from dash import dash_table  # pip install dash

from amazon_ML_analysis import exec_ml_analysis, exec_all_ml_analysis
from amazon_data_normalizer import ml_analysis_output_to_df


def get_min_date_from_max_date_minus_x_days(data_stringa, x_days):
    # Conversione in oggetto datetime
    data_datetime = datetime.datetime.strptime(data_stringa, '%Y-%m-%d %H:%M:%S')

    # Sottrazione di x giorni
    nuova_data = data_datetime - datetime.timedelta(days=x_days)

    # Conversione in stringa (facoltativo)
    nuova_data_stringa = nuova_data.strftime('%Y-%m-%d %H:%M:%S')

    return nuova_data_stringa


def generate_data_table(df):
    return dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns],
                                style_cell={'whiteSpace': 'pre-line', 'textAlign': 'left'})


def generate_bar_plot(ml_analysis_output_df):
    fig = create_feature_importance_histogram(ml_analysis_output_df)
    fig.update_xaxes(categoryorder="mean descending")

    # Calcola la media per ogni feature
    mean_values = ml_analysis_output_df.groupby("feature")["importance"].mean().sort_values(ascending=False)

    feature_index = 0
    # Aggiungi le linee orizzontali
    for feature, mean in mean_values.items():
        # Calcola le coordinate x per la linea
        x0 = feature_index - 0.5  # Inizio della linea
        x1 = feature_index + 0.5  # Fine della linea
        fig.add_shape(
            type="line",
            x0=x0, y0=mean, x1=x1, y1=mean,
            line=dict(color="black", dash="dash")
        )
        feature_index += 1

    return fig


def create_feature_importance_histogram(df, x_col="feature", y_col="importance", color_col="alg_name"):
    return px.histogram(df, x=x_col, y=y_col, color=color_col, barmode="group")


def generate_all_ml_graphics(dropdown_features, filtered_normalized_data, radio_cv_option, test_size, set_progress):
    ml_analysis_output = exec_all_ml_analysis(filtered_normalized_data, radio_cv_option, test_size, dropdown_features, set_progress)
    ml_analysis_output_df = ml_analysis_output_to_df(ml_analysis_output)
    accuracy_avg = statistics.mean(ml_analysis_output_df['accuracy'])
    accuracy_label = round(accuracy_avg * 100, 2)
    graph_plot_all_alg = generate_bar_plot(ml_analysis_output_df)
    ml_analysis_output_pivot = ml_analysis_output_df.pivot(index='feature', columns='alg_name',
                                                           values='importance').reset_index()
    ml_analysis_output_pivot.iloc[:, 1:] = round(ml_analysis_output_pivot.iloc[:, 1:] * 100, 2)
    importance_features_stats = generate_data_table(ml_analysis_output_pivot)
    return accuracy_label, graph_plot_all_alg, importance_features_stats


def generate_ml_graphics(algorithm, dropdown_features, filtered_normalized_data, radio_cv_option, test_size):
    perm_importance, accuracy = exec_ml_analysis(algorithm, filtered_normalized_data, radio_cv_option, test_size, dropdown_features)
    accuracy_label = round(accuracy * 100, 2)
    ml_analysis_output = [{"alg_name": algorithm, "perm_importance": perm_importance, "accuracy": accuracy}]
    ml_analysis_output_df = ml_analysis_output_to_df(ml_analysis_output)
    graph_matplotlib_alg = generate_bar_plot(ml_analysis_output_df)
    result = ml_analysis_output_df[['feature', 'importance']].copy()
    result['importance'] = round(result['importance'] * 100, 2)
    importance_features_stats = generate_data_table(result)
    return accuracy_label, graph_matplotlib_alg, importance_features_stats


def generate_feature_stats(features_input, filtered_data_input):
    feature_stats_data = filtered_data_input[features_input].describe().transpose()
    feature_stats_data = round(feature_stats_data, 2)
    feature_stats_data = feature_stats_data.reset_index().rename(columns={"index": "feature"})
    feature_stats = generate_data_table(feature_stats_data)
    return feature_stats


def generate_pie_chart(df):
    return px.pie(df, values='perc', names='name')


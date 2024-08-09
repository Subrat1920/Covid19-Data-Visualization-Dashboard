import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.figure_factory as ff
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
import base64
import pandas as pd
from dash import dcc, html


# Load datasets
dataset1 = pd.read_csv('covid.csv')
dataset2 = pd.read_csv('covid_grouped.csv')
dataset3 = pd.read_csv('covid+death.csv')


# Create Plotly visualizations
def create_table_figure():
    colorscale = [[0, '#4d004c'], [0.5, '#f2e5ff'], [1.0, '#ffffff']]
    table = ff.create_table(dataset1.head(15), colorscale=colorscale)
    return table


def create_bar_plots():
    bar1 = px.bar(dataset1.head(15), x='Country/Region', y='TotalCases',
                  color='TotalCases', height=500, hover_data=['Country/Region', 'Continent'])
    bar2 = px.bar(dataset1.head(15), x='TotalTests', y='Country/Region', color='TotalTests',
                  orientation='h', height=500, hover_data=['Country/Region', 'Continent'])
    bar3 = px.bar(dataset1.head(15), x='TotalCases', y='Continent', color='TotalTests',
                  orientation='h', height=500, hover_data=['Country/Region', 'Continent'])
    return bar1, bar2, bar3


def create_scatter_plots():
    scatter1 = px.scatter(dataset1, x='Continent', y='TotalCases',
                          hover_data=['Country/Region', 'Continent'], color='TotalCases',
                          size='TotalCases', size_max=80)
    scatter2 = px.scatter(dataset1.head(57), x='Continent', y='TotalCases',
                          hover_data=['Country/Region', 'Continent'], color='TotalCases',
                          size='TotalCases', size_max=80, log_y=True)
    scatter3 = px.scatter(dataset1.head(54), x='Continent', y='TotalTests',
                          hover_data=['Country/Region', 'Continent'], color='TotalTests',
                          size='TotalTests', size_max=80)
    scatter4 = px.scatter(dataset1.head(50), x='Continent', y='TotalTests',
                          hover_data=['Country/Region', 'Continent'], color='TotalTests',
                          size='TotalTests', size_max=80, log_y=True)
    scatter5 = px.scatter(dataset1.head(100), x='Country/Region', y='TotalCases',
                          hover_data=['Country/Region', 'Continent'], color='TotalCases',
                          size='TotalCases', size_max=80)
    scatter6 = px.scatter(dataset1.head(30), x='Country/Region', y='TotalCases',
                          hover_data=['Country/Region', 'Continent'], color='Country/Region',
                          size='TotalCases', size_max=80, log_y=True)
    scatter7 = px.scatter(dataset1.head(10), x='Country/Region', y='TotalDeaths',
                          hover_data=['Country/Region', 'Continent'], color='Country/Region',
                          size='TotalDeaths', size_max=80)
    scatter8 = px.scatter(dataset1.head(30), x='Country/Region', y='Tests/1M pop',
                          hover_data=['Country/Region', 'Continent'], color='Country/Region',
                          size='Tests/1M pop', size_max=80)
    scatter9 = px.scatter(dataset1.head(30), x='Country/Region', y='Tests/1M pop',
                          hover_data=['Country/Region', 'Continent'], color='Tests/1M pop',
                          size='Tests/1M pop', size_max=80)
    scatter10 = px.scatter(dataset1.head(30), x='TotalCases', y='TotalDeaths',
                           hover_data=['Country/Region', 'Continent'], color='TotalDeaths',
                           size='TotalDeaths', size_max=80)
    scatter11 = px.scatter(dataset1.head(30), x='TotalCases', y='TotalDeaths',
                           hover_data=['Country/Region', 'Continent'], color='TotalDeaths',
                           size='TotalDeaths', size_max=80, log_x=True, log_y=True)
    scatter12 = px.scatter(dataset1.head(30), x='TotalTests', y='TotalCases',
                           hover_data=['Country/Region', 'Continent'], color='TotalTests',
                           size='TotalTests', size_max=80, log_x=True, log_y=True)
    return scatter1, scatter2, scatter3, scatter4, scatter5, scatter6, scatter7, scatter8, scatter9, scatter10, scatter11, scatter12


def create_choropleths():
    choropleth1 = px.choropleth(dataset2,
                                locations='iso_alpha',
                                color="Deaths",
                                hover_name="Country/Region",
                                color_continuous_scale="Viridis",
                                animation_frame="Date")
    choropleth2 = px.choropleth(dataset2,
                                locations='iso_alpha',
                                color="Deaths",
                                hover_name="Country/Region",
                                color_continuous_scale="Viridis",
                                animation_frame="Date")
    return choropleth1, choropleth2


def create_bars_lines():
    bar1 = px.bar(dataset2, x="WHO Region", y="Confirmed", color="WHO Region",
                  animation_frame="Date", hover_name="Country/Region")
    bar2 = px.bar(dataset2, x="Date", y="Confirmed", color="Confirmed",
                  hover_data=["Confirmed", "Date", "Country/Region"], height=400)
    bar3 = px.bar(dataset2, x="Date", y="Confirmed", color="Confirmed",
                  hover_data=["Confirmed", "Date", "Country/Region"], log_y=True, height=400)
    df_US = dataset2.loc[dataset2["Country/Region"] == "US"]
    bar4 = px.bar(df_US, x="Date", y="Confirmed", color="Confirmed", height=400)
    line = px.line(df_US, x="Date", y="Recovered", height=400)
    return bar1, bar2, bar3, bar4, line


def create_wordcloud_images():
    sentences = dataset3["Condition"].tolist()
    sentences_as_a_string = ' '.join(sentences)
    wordcloud1 = WordCloud(width=800, height=400, background_color='white').generate(sentences_as_a_string)

    column2_tolist = dataset3["Condition Group"].tolist()
    column_to_string = " ".join(column2_tolist)
    wordcloud2 = WordCloud(width=800, height=400, background_color='white').generate(column_to_string)

    # Convert the wordcloud images to base64 strings
    def wordcloud_to_base64(wordcloud):
        buffer = io.BytesIO()
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        img_str = base64.b64encode(buffer.read()).decode('utf-8')
        plt.close()
        return img_str

    return wordcloud_to_base64(wordcloud1), wordcloud_to_base64(wordcloud2)


# Create figures
table_figure = create_table_figure()
bar1, bar2, bar3 = create_bar_plots()
scatter_plots = create_scatter_plots()
choropleth1, choropleth2 = create_choropleths()
bar1_2, bar2_2, bar3_2, bar4, line = create_bars_lines()
wordcloud_img1, wordcloud_img2 = create_wordcloud_images()

# Initialize the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("COVID-19 Data Visualization"),

    html.H2("Data Table"),
    dcc.Graph(figure=table_figure),

    html.H2("Bar Charts"),
    dcc.Graph(figure=bar1),
    dcc.Graph(figure=bar2),
    dcc.Graph(figure=bar3),

    html.H2("Scatter Plots"),
    dcc.Graph(figure=scatter_plots[0]),
    dcc.Graph(figure=scatter_plots[1]),
    dcc.Graph(figure=scatter_plots[2]),
    dcc.Graph(figure=scatter_plots[3]),
    dcc.Graph(figure=scatter_plots[4]),
    dcc.Graph(figure=scatter_plots[5]),
    dcc.Graph(figure=scatter_plots[6]),
    dcc.Graph(figure=scatter_plots[7]),
    dcc.Graph(figure=scatter_plots[8]),
    dcc.Graph(figure=scatter_plots[9]),
    dcc.Graph(figure=scatter_plots[10]),
    dcc.Graph(figure=scatter_plots[11]),

    html.H2("Choropleth Maps"),
    dcc.Graph(figure=choropleth1),
    dcc.Graph(figure=choropleth2),

    html.H2("Bar Charts and Line Chart"),
    dcc.Graph(figure=bar1_2),
    dcc.Graph(figure=bar2_2),
    dcc.Graph(figure=bar3_2),
    dcc.Graph(figure=bar4),
    dcc.Graph(figure=line),

    html.H2("Word Clouds"),
    html.Img(src=f'data:image/png;base64,{wordcloud_img1}', style={'width': '100%'}),
    html.Img(src=f'data:image/png;base64,{wordcloud_img2}', style={'width': '100%'}),
])

if __name__ == '__main__':
    app.run_server(debug=True)

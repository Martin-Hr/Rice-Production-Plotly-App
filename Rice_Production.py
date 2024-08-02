import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Load the data
file_path = 'rice_production_by_country.csv'
data = pd.read_csv(file_path)

# Data preprocessing
data['Rice Production (Tons)'] = data['Rice Production (Tons)'].str.replace('K', 'e3').str.replace('M', 'e6').astype(float)
data['Rice Acreage (Hectare)'] = data['Rice Acreage (Hectare)'].str.replace('K', 'e3').str.replace('M', 'e6').astype(float)
data['Rice Yield (Kg / Hectare)'] = data['Rice Yield (Kg / Hectare)'].str.replace(',', '').astype(float)

# Initialize the Dash app
app = Dash(__name__)

# Layout of the app
app.layout = html.Div([
    html.H1("Global Rice Production by Country"),
    
    # Dropdown menu to select the feature variable
    html.Label("Select Feature:"),
    dcc.Dropdown(
        id='feature-dropdown',
        options=[
            {'label': 'Rice Production (Tons)', 'value': 'Rice Production (Tons)'},
            {'label': 'Rank of Rice Production', 'value': 'Rank of Rice Production'},
            {'label': 'Rice Production Per Person (Kg)', 'value': 'Rice Production Per Person (Kg)'},
            {'label': 'Rank of Rice Production Per Person', 'value': 'Rank of Rice Production Per Person'},
            {'label': 'Rice Acreage (Hectare)', 'value': 'Rice Acreage (Hectare)'},
            {'label': 'Rank of Rice Acreage', 'value': 'Rank of Rice Acreage'},
            {'label': 'Rice Yield (Kg / Hectare)', 'value': 'Rice Yield (Kg / Hectare)'},
            {'label': 'Rank of Rice Yield', 'value': 'Rank of Rice Yield'}
        ],
        value='Rice Production (Tons)'  # default value
    ),
    
    # Choropleth map to display the feature variable for the selected country
    dcc.Graph(id='choropleth-map', style={'height': '80vh'})  # Set the height of the map
])

# Callback to update the graph based on selected feature variable
@app.callback(
    Output('choropleth-map', 'figure'),
    [Input('feature-dropdown', 'value')]
)
def update_map(selected_feature):
    fig = px.choropleth(data,
                        locations="Country",
                        locationmode="country names",
                        color=selected_feature,
                        hover_name="Country",
                        color_continuous_scale=px.colors.sequential.Plasma,
                        title=f'Global {selected_feature} by Country')

    # Customize the layout to make the map larger
    fig.update_layout(
        autosize=True,
        margin=dict(l=0, r=0, t=50, b=0),
        height=700  # Adjust height to make the map larger
    )
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

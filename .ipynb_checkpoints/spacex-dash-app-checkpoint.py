# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(
                                    id='site-dropdown',  
                                    options=[{'label':'All Site','value':'ALL'},*[{'label':launch,'value':launch} for launch in spacex_df['Launch Site'].unique()]],
                                    value='ALL',
                                    placeholder="Select Launch Site",
                                    searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0,max=10000,step=1000,
                                    marks={0:'0',2500:'2500',5000:'5000',7500:'7500',10000:'10000'},
                                    value=[min_payload,max_payload]
                                    ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart',component_property='figure'),
               Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        filtered_df = spacex_df[spacex_df['class']==1]
        title = "Total Success Launches By Site"
        fig = px.pie(
        filtered_df, 
        values='class', 
        names='Launch Site',
        title=title)
        return fig
    else:
        title = f"Success and Failed Launches for Site: {entered_site}"
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        class_counts = filtered_df['class'].value_counts().reset_index()
        class_counts.columns = ['class','counts']
        fig = px.pie(
        class_counts, 
        values='counts', 
        names='class',
        title=title)
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart',component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")]
    )
def get_scatter_plot(entered_site,entered_slide):
    if entered_site == 'ALL':
        min = int(entered_slide[0])
        max = int(entered_slide[1])
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] > min) & (spacex_df['Payload Mass (kg)'] < max)]
        
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category'
        )
        return fig
    else:
        min = int(entered_slide[0])
        max = int(entered_slide[1])
        filtered_df = spacex_df[spacex_df['Launch Site']==entered_site][(spacex_df['Payload Mass (kg)'] > min) & (spacex_df['Payload Mass (kg)'] < max)]
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category'
        )
        return fig

# Run the app
if __name__ == '__main__':
    app.run()

#!/usr/bin/env python
# coding: utf-8

# In[1]:


#import necessary libraries

# Libraries to help with reading and manipulating data

from dash import Dash, html, dcc, Input, Output  
import plotly.express as px
import dash_ag_grid as dag # pip install dash_ag_grid
import dash_bootstrap_components as dbc   # pip install dash-bootstrap-components
import pandas as pd     # pip install pandas 


# In[2]:


# Libaries to help with data visualization
import matplotlib      # pip install matplotlib for data visualization
matplotlib.use('agg')
import matplotlib.pyplot as plt
import base64
from io import BytesIO


# In[3]:


df=pd.read_csv('Sample_72023 (2).csv')


# In[4]:


# Display the data
print(df)


# In[11]:


#Creating and naming the dashboard components and layout
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dbc.Container([
    html.H1("Interactive Matplotlib Data", className='mb-2', style={'textAlign':'center'}),

    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='category',
                value='AVPU',
                clearable=False,
                options=df.columns[1:])
        ], width=4)
    ]),

    dbc.Row([
        dbc.Col([
            html.Img(id='bar-graph-matplotlib')
        ], width=12)
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='bar-graph-plotly', figure={})
        ], width=20, md=10),
        dbc.Col([
            dag.AgGrid(
                id='grid',
                rowData=df.to_dict("records"),
                columnDefs=[{"field": i} for i in df.columns],
                columnSize="sizeToFit",
            )
        ], width=20, md=10),
    ], className='mt-4'),

])


# In[12]:


# Create interactivity between dropdown component and graph
@app.callback(
    Output(component_id='bar-graph-matplotlib', component_property='src'),
    Output('bar-graph-plotly', 'figure'),
    Output('grid', 'defaultColDef'),
    Input('category', 'value'),
)
def plot_data(selected_yaxis):

    # Build the matplotlib figure
    fig = plt.figure(figsize=(14, 5))
    plt.bar(df['MERCHANT'], df[selected_yaxis])
    plt.ylabel(selected_yaxis)
    plt.xticks(rotation=30)

    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    fig_data = base64.b64encode(buf.getbuffer()).decode("ascii")
    fig_bar_matplotlib = f'data:image/png;base64,{fig_data}'

    # Build the Plotly figure
    fig_bar_plotly = px.bar(df, x='MERCHANT', y=selected_yaxis).update_xaxes(tickangle=330)

    my_cellStyle = {
        "styleConditions": [
            {
                "condition": f"params.colDef.field == '{selected_yaxis}'",
                "style": {"backgroundColor": "#d3d3d3"},
            },
            {   "condition": f"params.colDef.field != '{selected_yaxis}'",
                "style": {"color": "black"}
            },
        ]
    }

    return fig_bar_matplotlib, fig_bar_plotly, {'cellStyle': my_cellStyle}


if __name__ == '__main__':
    app.run_server(debug=False, port=8050)


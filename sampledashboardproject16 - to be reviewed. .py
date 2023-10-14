#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import hvplot.pandas as hv
import panel as pn
from bokeh.layouts import column
from bokeh.models import DateRangeSlider
from bokeh.plotting import curdoc
import holoviews as hv

pn.extension("holoviews")

# Define the date and time format including AM/PM for parsing
date_format = '%m/%d/%Y %H:%M'

# Read the CSV file with headers only
df1 = pd.read_csv('Sample2_72023 (2).csv', parse_dates=['DATE'])

# Define the date range slider
start_date = df1['DATE'].min()  # July 1, 2023, 00:00
end_date = df1['DATE'].max()
date_range_slider = DateRangeSlider(
    title="Select Date Range",
    start=start_date,
    end=end_date,
    value=(start_date, end_date)
)

# Define the Y-axis selector
yaxis = pn.widgets.RadioButtonGroup(
    name='Y axis',
    options=['VOLUME', 'ARPU'],
    button_type='success'
)

# Create the initial plot using hvPlot
Payable_plot = df1.hvplot(
    x='DATE',
    y=yaxis.value,
    by='PROVIDER',
    line_width=2,
    title="July 2023 Volume"
)

# Define a callback function to update the plot when the date range changes
def update_filtered_df(attr, old_range, new_range):
    start_date, end_date = new_range
    filtered_df = df1[
        (df1['DATE'] >= start_date) &
        (df1['DATE'] <= end_date)
    ]
    Payable_plot = filtered_df.hvplot(
        x='DATE',
        y=yaxis.value,
        by='PROVIDER',
        line_width=2,
        title="July 2023 Volume"
    )
    layout[2] = Payable_plot  # Update the plot in the layout

# Attach the callback function to the date_range_slider's value change event
date_range_slider.on_change('value', update_filtered_df)

# Create a Panel layout
layout = pn.Column(date_range_slider, yaxis, Payable_plot)

# Wrap the Panel app with curdoc
curdoc().add_root(layout.servable())


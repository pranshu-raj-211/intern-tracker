from taipy import Gui 
import pandas as pd
from taipy.gui import builder as tgb
import plotly.graph_objects as go

data = pd.read_csv('data/aggregate/aggregate.csv')

location_counts = data['location'].value_counts(sort=True)

location_fig = go.Figure(data=go.Bar(x=location_counts.index, y=location_counts.values))
location_fig.update_layout(title_text='Location counts', xaxis_title='index', yaxis_title='values')

# md='''
# # Analysis of sourced data

# <|{location_counts}|chart|type=bar|x=index|y=values|>'''

with tgb.Page() as analysis_page:
    tgb.text('Analysis od sourced data',class_name='h1')
    tgb.html('br')
    with tgb.part('card'):
        tgb.text('Demand of jobs sourced')

# todo : add the plotly charts - store as image then use html(md is hard, no docs for py)
import dash

import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output,State
import plotly.graph_objs
from iexfinance.stocks import get_historical_data as gst
from datetime import datetime

options=[]
cl=pd.read_csv('NASDAQcompanylist.csv')
cl.set_index('Symbol', inplace=True)
for tic in cl.index:
    options.append({'label':cl.loc[tic]['Name'],'value':tic})

app=dash.Dash()
app.layout=html.Div([
           html.H1('Stock Ticket Dashboard'),
           html.Div([
                html.H2('Enter a Stock Name:',style={'paddingRight':'30px'}),
                dcc.Dropdown(id='Stock_input',
                             options=options,
                             value=['TSLA'],
                             multi=True
                             )
                   ],style={'display':'inline-block','verticalAlign':'top','width':'30%'}),
           html.Div([html.H3('Select start and End Dates!'),
                    dcc.DatePickerRange(
                    id='my-date-picker-range',
                    min_date_allowed=datetime(1995, 8, 5),
                    max_date_allowed=datetime.today(),
                    #initial_visible_month=datetime(2017, 8, 5),
                    start_date=datetime(2016, 8, 25),
                    end_date=datetime.today())],style={'display':'inline-block'}),
             html.Div([
                    html.Button(
                     id='submit-button',
                     n_clicks=0,
                     children='Submit',
                    style={'fontSize':24, 'marginLeft':'30px'}
        ),
    ], style={'display':'inline-block'}),
           dcc.Graph(id='My_graph',figure={'data':
                                  [{'x':[1,2],'y':[3,1]}]
           })
                      ])

@app.callback(Output('My_graph','figure'),
              [Input('submit-button','n_clicks')],
               [State('Stock_input','value'),
               State('my-date-picker-range','start_date'),
               State('my-date-picker-range','end_date')])
def Title_call(n_clicks,Stock_ticker,start_date,end_date):
    start=datetime.strptime(start_date[:10], '%Y-%m-%d')
    end=datetime.strptime(end_date[:10], '%Y-%m-%d')
    trace_list=[]
    for stocks in Stock_ticker:
        trace=gst(stocks,start, end, token="pk_*********", output_format='pandas')
        trace_list.append({'x':trace.index,'y':trace['open'],'name':stocks})
    figure={'data':trace_list,'layout': {'title':', '.join(Stock_ticker)+' Closing Prices'}}
    return(figure)

if __name__ == '__main__':
    app.run_server(debug=True)

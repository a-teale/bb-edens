import numpy, dash
import scipy.special
import plotly.graph_objects as go
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__,external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div([
    html.H1('Black Body Radiation - Energy Densities',style={'font-family': 'sans-serif',"margin-top": "20","margin-bottom": "10"},className='page_header'),
    html.Div([
        html.Div([html.Label('Min. Wavelength / nm',style={'font-family': 'sans-serif'}),dcc.Input(id="minl",type="number",placeholder="minimum wavelength",min=5,max=100000,step=50,value=5,style={'font-family': 'sans-serif','justify': 'center'})],style={'width': '20%', 'display': 'inline-block'}),
        html.Div([html.Label('Max. Wavelength / nm',style={'font-family': 'sans-serif'}),dcc.Input(id="maxl",type="number",placeholder="maximum wavelength",min=5,max=100000,step=500,value=90000,style={'font-family': 'sans-serif','justify': 'center'})],style={'width': '20%', 'display': 'inline-block'}),
        html.Div([html.Label('Temp',style={'font-family': 'sans-serif'}),dcc.Input(id="tval",type="number",placeholder="temperature",min=0,max=1000, step=10,value=20,style={'font-family': 'sans-serif','justify': 'center'})],style={'width': '20%', 'display': 'inline-block'}),
        ],style={'width': '100%', 'display': 'inline-block','vertical-align': 'middle'}),
        html.Br(),html.Br(),
        html.Div([
            html.Div([html.H4('',style={'font-family': 'sans-serif',"margin-top": "10","margin-bottom": "10",'textAlign': 'center'}),dcc.Graph(id='edens',config={'displayModeBar': False})],style={'width': '60%', 'display': 'inline-block'}),
        ],style={'width': '100%', 'display': 'inline-block','vertical-align': 'middle'})
])

#To do -- scientific notation on x axis
#      -- units of energy density -- scientific notation
#      -- enforce max > min ?

@app.callback(
    Output('edens', 'figure'),
    [Input('minl', 'value'),
     Input('maxl', 'value'),
     Input('tval', 'value')])
def UpdateEden(minl,maxl,tval):
    if minl is None:
        minl = 5
    if maxl is None:
        maxl = 5
    minl_m = minl * 10e-9
    maxl_m = maxl * 10e-9
    lam = numpy.linspace(minl_m,maxl_m,num=501)
    t = tval 
    maxpeden = numpy.max(PlanckEden(lam,t))
    maxpeden += 0.5*maxpeden
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=lam,y=RJEden(lam,t),mode='lines',line_shape='spline',name='Rayleigh-Jeans'))
    fig.add_trace(go.Scatter(x=lam,y=PlanckEden(lam,t),mode='lines',line_shape='spline',name='Planck'))
    fig.update_layout(template='plotly_white',margin={'t': 0, 'l': 0, 'r': 0, 'b': 0},hovermode='closest',autosize=True,legend=dict(orientation='h',yanchor='middle',y=1.0,xanchor='center',x=0.5,bgcolor="rgba(0,0,0,0)",font=dict(size=10)),paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',xaxis=dict(title='Wavelength / m',tickformat = '.2e',showgrid=False,showline=True,linewidth=2,linecolor='black',ticks="outside",tickwidth=2,ticklen=6,title_font=dict(size=12),tickfont=dict(size=8)),yaxis=dict(title=r'$Energy Density / Nm<sup>-3</sup>',tickformat = '.3e',showgrid=False,showline=True,linewidth=2,linecolor='black',ticks="outside",tickwidth=2,ticklen=6,title_font=dict(size=12),tickfont=dict(size=8))) 
    fig.update_yaxes(range = [0,maxpeden])
    return fig

def PlanckEden(l,t):
    kb = 1.38064852e-23
    h = 6.62607044e-34
    c = 2.99792458e8
    peden = (8.0*numpy.pi*h*c)/(numpy.power(l,5.0)*(numpy.exp((h*c)/(l*kb*t))-1.0)) 
    return peden

def RJEden(l,t):
    kb = 1.38064852e-23
    rjeden = 8.0*numpy.pi*kb*t / numpy.power(l,4.0)
    return rjeden




if __name__ == '__main__':
    app.run_server(debug=False)

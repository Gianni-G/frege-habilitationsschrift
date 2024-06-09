import plotly.graph_objects as go
import numpy as np
from functools import partial, reduce
from dash import Input, Output, Dash, dcc, html
import dash_bootstrap_components as dbc


# def iterate(x,f,n):
#     if n == 0:
#         return x
#     xi = f(x)
#     for _ in range(n-1):
#         xi = f(xi)    
#     return xi

def iterate(x,f,n):
    xi = x
    for _ in range(n):
        xi = f(xi)    
    return xi

label_plus = dcc.Markdown('$x+b$',mathjax=True)
plus = (lambda x,a,b,c,d: x + b)


label_times = dcc.Markdown('$xb$',mathjax=True)
times = (lambda x,a,b,c,d: x * b)


label_power = dcc.Markdown('$x^b$',mathjax=True)
power = (lambda x,a,b,c,d: x ** b)


label_affine = dcc.Markdown('$a(1-b)+bx$',mathjax=True)
affine = (lambda x,a,b,c,d: a*(1-b)+b*x)


label_rational = dcc.Markdown('$\\frac{A+Bx}{C+Dx}$',mathjax=True)
rational = (lambda x,a,b,c,d: (a+b*x)/(c+d*x))


function_labels = [label_plus,label_times,label_power,label_affine,label_rational]
functions = [plus,times,power,affine,rational]


external_stylesheets = [dbc.themes.BOOTSTRAP]

app = Dash(__name__,external_stylesheets = external_stylesheets)
server = app.server

app.layout = dbc.Container([

    dbc.Row([
        dbc.Col(
            html.Div([
            html.P("Frege's Habilitationsschrift",style={'font-family':'Helvetica', 'font-size': 30, 'font-weight': 'thin', "text-align": "center"}),
            html.Label(['Function:'], style={'font-weight': 'bold', "text-align": "center"}),
            html.Div(
            dcc.Dropdown(
                id="Function",
                options = [{'label': label, 'value' : f_i} for f_i,label in enumerate(function_labels)],
                value = 0,
            )),

            html.Label(['n:'], style={'font-weight': 'bold', "text-align": "center"}),
            dcc.Slider(
                id="n",
                min=0,
                max=10,
                value=5,
                step=1,
                marks={i: '{}'.format(i) for i in range(11)},
                updatemode='drag',
                tooltip={"placement": "bottom", "always_visible": True},
                ),
            html.Div([
            html.Label(['b:'], style={'font-weight': 'bold', "text-align": "center"}),
            dcc.Slider(
                id="b",
                min=0,
                max=5,
                value=1,
                step=.01,
                marks={i: '{}'.format(i) for i in range(5)},
                updatemode='drag',
                tooltip={"placement": "bottom", "always_visible": True}
                ),
            ]),
            html.Div([
            html.Label(['a:'], style={'font-weight': 'bold', "text-align": "center"}),
            dcc.Slider(
                id="a",
                min=0,
                max=5,
                value=1,
                step=.01,
                marks={i: '{}'.format(i) for i in range(5)},
                updatemode='drag',
                tooltip={"placement": "bottom", "always_visible": True}
                ),
            ]),
            html.Div([
            html.Label(['c:'], style={'font-weight': 'bold', "text-align": "center"}),
            dcc.Slider(
                id="c",
                min=0,
                max=5,
                value=1,
                step=.01,
                marks={i: '{}'.format(i) for i in range(5)},
                updatemode='drag',
                tooltip={"placement": "bottom", "always_visible": True}
                ),
            ]),
            html.Div([
            html.Label(['d:'], style={'font-weight': 'bold', "text-align": "center"}),
            dcc.Slider(
                id="d",
                min=0,
                max=5,
                value=1,
                step=.01,
                marks={i: '{}'.format(i) for i in range(5)},
                updatemode='drag',
                tooltip={"placement": "bottom", "always_visible": True}
                ),
            ]),
            ],
            ),
            width='4'
        ),
        dbc.Col(dcc.Graph(id="plot", mathjax=True),width=8),
    ]
    )], fluid = True)

@app.callback(
    Output("plot", "figure"),
    Input("n", "value"),
    Input("b", "value"),
    Input("a", "value"),
    Input("c", "value"),
    Input("d", "value"),
    Input("Function", "value"),
)
def graph_histogram(n,b,a,c,d,f_i):
    fig = go.Figure()

    x = np.arange(-10, 10, 0.01)
    f = functions[f_i]
    fx = partial(f, b=b, a=a, c=c, d=d)

    for n_i in range(n+1):
        fn = partial(iterate, f=fx, n=n_i)
        fig.add_trace(
            go.Scatter(
                line=dict(color=("red" if n_i==0 else f'rgb({5*n_i}, {25*n_i}, 255)'), width=2),
                name= "$\large f^0=x$" if n_i==0 else "$\large f^{" + str(n_i) + "} = " + f"{''.join(['f']*n_i)}(x)$",
                x=x,
                y = [fn(x_i) for x_i in x]
            ))

    fig.update_xaxes(
        range=[-6,6],
        # mirror=True,
        # ticks='outside',
        # showline=True,
        # linecolor='black',
        gridcolor='lightgrey',
        zerolinecolor='black',
        zerolinewidth=1,
        )
    fig.update_yaxes(
        range=[-6,6],
        mirror=True,
        # ticks='outside',
        showline=True,
        # linecolor='black',
        gridcolor='lightgrey',
        zerolinecolor='black',
        zerolinewidth=1,
        )

    fig.update_layout(
        plot_bgcolor='white',
        yaxis_scaleanchor="x",
        # width=800,
        height=800,
        title="$ \huge f(x)="+ function_labels[f_i].children[1:],
        title_x=0.4,
        showlegend= True,
        # margin=dict(l=20, r=20, t=20, b=20),
        margin=dict(r=300),
    )
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
 
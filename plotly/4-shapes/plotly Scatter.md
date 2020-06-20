#### Plotly Scatter objects

A Scatter object is also called a trace.

``(x,y)`` values can be specified as two lists like:

    poly = go.Scatter(x=[0,1,1],y=[1,0,1])

or

    X = [0,1,1]
    Y = [1,0,1]
    poly = go.Scatter(x=X,y=Y)

code:

    import plotly.graph_objects as go

    poly = go.Scatter(x=[0,1,1],y=[1,0,1])
    fig = go.Figure(poly)
    fig.show()

This results in the three points plotted with lines connecting the first two.

``print(poly)`` gives:

    Scatter({
        'x': [0, 1, 1], 'y': [1, 0, 1]
    })

To draw then entire triangle, add the first point at the end.

<hr>

The default color is blue, 
with fairly small points and line widths.  To change the line properties do either:

    line={'color':'black', 'width':10})
    line=dict(color='black',width=10)

This also changes the color of the vertices to black.

Vertices are called markers.

    marker={'size':40, 'color':'blue'}

to color individually:

    dict(size=[40, 60, 80],
         color=[0, 1, 2])

To toggle the markers off/on in the default:

    mode='lines'
    mode='lines+markers'

For marker symbols see [here](https://plotly.com/python/reference/#scatter-marker-symbol)

<hr>

Fill is a bit complicated.  There are a number of possible values.

    "none" | "tozeroy" | "tozerox" | "tonexty" |
    "tonextx" | "toself" | "tonext"

https://plotly.com/python/reference/#scatter-fill

    fill='toself', fillcolor='salmon',

<hr>

To add a second trace to a figure do:

    fig.add_trace(poly2)

final code:

    import plotly.graph_objects as go
    
    poly = go.Scatter(
        x=[0,1,1,0],y=[1,0,1,1],
        line={'color':'black', 'width':3},
        marker={'size':10, 'color':'red'},
        mode='lines+markers',
        fill='toself', fillcolor='salmon')
    
    fig = go.Figure(poly)
    fig.show()

To do:
what is scattergeo

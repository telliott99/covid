import plotly.graph_objects as go

import ucolors

def round_up_n_places(m, n):
    return round(m, -n) + 10000

def plot(rL):
    nrows = len(rL)
    ncols = len(rL[0])
    for row in rL:
        assert len(row) == ncols
    
    cL = ucolors.get_colors(nrows)
    
    MX = 0
    for vL in rL:
        m = max(vL)
        if m > MX:
            MX = m
    ylimit = round_up_n_places(MX, 4)
 
    R = range(ncols)

    fig = go.Figure()
    for vL,color in zip(rL,cL):
        plt = go.Scatter(
            x=list(R),
            y=vL,
            line={'color':color,'width':3},
            marker={'size':15, 'color':color},
            mode='lines+markers')
            
        fig.add_trace(plt)
    
        fig.update_layout(
            yaxis=dict(range=[0,ylimit]))
            
    fig.show()

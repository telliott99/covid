import plotly.express as px

cL = ['green','magenta']
L = ['CA','TX','SC']

fig = px.choropleth(
    locations=L,
    locationmode="USA-states", 
    color_discrete_sequence=cL,
    color=L, 
    scope="usa")

fig.update_layout(
    {
     'geo':{'center': {'lon': -115, 'lat': 37}},
     'xaxis':{'fixedrange':False, 'range':[50,60]},
     'yaxis':{'fixedrange':False, 'range':[50,60]},
    })

print(type(fig))
fig.show()
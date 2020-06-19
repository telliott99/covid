import plotly.express as px

fig = px.choropleth(
    locations=['CA','TX','SC'],
    locationmode="USA-states", 
    color=[1,2,3], 
    scope="usa")
    
fig.show()
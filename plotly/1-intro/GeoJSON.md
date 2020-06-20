#### GeoJSON

GeoJSON is an open-format standard for geo data.

The elemental unit is a Feature, a JSON (dict) object with keys:

We are concerned with individual objects whose 'type' is 'Feature'.

A collection of such objects is a 'FeatureCollection', that is, it has a key:

    'type':'FeatureCollection'
    'features': [ list of Features ]

<hr>

An individual Feature has keys:

  - 'type':'Feature'
  - 'id':'01001'

'id' here is a FIPS code,
where '01' is the state ('Alabama') 
and '001' is the county ('Autauga')

properties is a dict with keys:

  - 'GEO_ID'
  - 'STATE'
  - 'COUNTY'
  - 'NAME'
  - 'LSAD'
  - 'CENSUSAREA'
  - 'geometry'

'GeoID' might be '0500000US01001'.  LSAD is 'County'.

geometry has keys:

  - 'type': 'Polygon'
  - 'coordinates': [[long,lat], [long,lat] ..] list of vertices

<hr>

I downloaded the US counties from plotly's url:

'https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json'

by

    fn = 'counties.json'
    with url(fn) as fh:
        counties = json.load(fh)



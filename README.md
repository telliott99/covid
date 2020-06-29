#### covid

This is a project to download and play with the data collated by the [Johns Hopkins CSSE](https://github.com/CSSEGISandData/COVID-19) folks.

This should work for you if you clone the project.  The file structure depends on a ``base`` path, which is established by an environmental variable.  

In my ``~/.zshrc`` I have the line:

    covid_base=$HOME'/Dropbox/Github/covid'
    export covid_base
    alias cov='cd $covid_base && pwd'
    
You could do this as a one-off in Terminal with just the first line

    covid_base=$HOME'/path/to/covid'
    
Then, in the scripts, one of the first things that usually happens is:

    import sys, os
    
    base = os.environ.get('covid_base')
    sys.path.insert(0,base)
    
From there, it all just works.

#### Run this at home

I'm using Python3 for this project.  I installed it with Homebrew.

Most things should work with Python2.  The tests module uses ``subprocess.run``, which requires Python3.  

Also, I installed ``plotly`` and ``pandas`` with pip3.  These are needed for the choropleth maps.  I don't know how well they work with Python2.

To test, I used the web interface to Github to clone the project by downloading a zipfile and then opened it.  The directory name is covid-master.  Then I set the environmental variable

    covid_base=$HOME"/Desktop/covid-master"

and everything seems to work.

#### More

This is all Python3 code now, after a recent update.

My version of the database is constructed from their database files by **update.py**.  This checks the 'csv.source' directory and if it's not up-to-date, downloads the appropriate data files from their [data](https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data).

As of this morning, there are two databases:  one with just the data from this month, and one with all the data.  You can construct the latter by passing the argument ``--max`` to ``build/update.py``.

The scripts use the standard database.  The mega version is for some not-yet-written stuff to plot the entire course of the pandemic.

My database looks like

```
2020-03-22
2020-04-28

Autauga;Alabama;01001;US
0,0,1,4 ...
0,0,0,0 ...

...
``` 

Rather than mark each data point with the date, we just track the first and last dates for the database as a whole.  This means we have to watch for when updates don't happen properly, if a new key appears, or if a county decides not to report after a while.


Options for scripts are:

- the US broken down by states:  ``all_states.py``
- the US broken down by counties:  ``us_by_counties.py``
- a given state broken down by counties:  ``one_state.py``


Features that are currently supported are given by the ``--help`` flag.

More recently, I have started making what are called choropleth plots, geographic plots where the fill color is based on the statistic for case growth (or whatever else you want).  These can be found in ``geo``, and examples are in ``results``.



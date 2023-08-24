Title: Siuba - Scrappy data analysis in Python you would normally do in R
Date: 2022-08-11
Author: Kristian Maras
Category: Python
Tags: R, tidyverse, Python

### Suiba

<https://siuba.readthedocs.io/en/latest/> 

**Siuba** is a python package that replicates R dplyr language in python. Provides concise, flexible data-analysis over multiple data sources currently including pandas DataFrames and SQL tables. Siuba is build on top of pandas, hence data methods refrence pandas operations you will know already if you use pandas often.


    select() - keep certain columns of data.
    filter() - keep certain rows of data.
    mutate() - create or modify an existing column of data.
    summarize() - reduce one or more columns down to a single number.
    arrange() - reorder the rows of data.

Basic example below. Notice:

* lazy expression _ avoids duplicating name of dataframe in operations

* the _. when referencing columns

*  '>>' is the new pipe as opposed to %>% in R



```
# Load packages

from siuba import _, group_by, summarize, mutate,  arrange
from siuba.data import mtcars

(mtcars
  >> group_by(_.cyl)
  >> summarize(avg_hp = _.hp.mean())
  )

(mtcars >> group_by(_.cyl) >> 
    mutate(var = _.hp - _.hp.mean()) >> 
    arrange(_.cyl))

```

Lazy expression provides concise syntax which also reduces the need for many lambda expressions.

```
# old approach: repeat name
mtcars[mtcars.cyl == 4]

# old approach: lambda
mtcars[lambda _: _.cyl == 4]

# siu approach
mtcars[_.cyl == 4]

#Less lambdas

# pandas
mtcars.assign(avg = lambda d: d.mpg.mean())

# siuba
mutate(mtcars, avg = _.mpg.mean())


```

Suiba works with plotnine (the ggplot equivalent for python) to make python feel alot like R in data manipulation and plotting.


```

from siuba import mutate, _
from plotnine import ggplot, aes, geom_point

(mtcars
  >> mutate(hp_per_cyl = _.hp / _.cyl)
  >> ggplot(aes("cyl", "hp_per_cyl"))
   + geom_point()
)
```


Nest and Unnest operations available.


```
from siuba import _, mutate, unnest
import pandas as pd

tagged = pd.DataFrame({
    'id': [1,2,3],
    'tags': ['a,b,c', 'd,e', 'f']
})

(tagged
    >> mutate(split_tags = _.tags.str.split(','))
    >> unnest("split_tags")
)

```

## Using databases:

Interaction is the same if data is remote data such as sql table, rather than datframe. Generating the SQL query that corresponds to the data manipulation is also available with show_query().

```

from sqlalchemy import create_engine
from siuba.sql import LazyTbl
from siuba import show_query

# copy in to sqlite
engine = create_engine("sqlite:///:memory:")
mtcars.to_sql("mtcars", engine, if_exists = "replace")


# connect with siuba
tbl_mtcars = LazyTbl(engine, "mtcars")

query_data = (tbl_mtcars
  >> group_by(_.cyl)
  >> summarize(avg_hp = _.hp.mean())
  )
#Under the hood siuba’s summarize function is converting the lazy expression show in the code below to SQL

query_data >> show_query()

```

Comparison with other similar packages are available here:

<https://siuba.readthedocs.io/en/latest/key_features.html#Key-features>


Other notable points include fast group by operations and abstract syntax trees for transforming operations.


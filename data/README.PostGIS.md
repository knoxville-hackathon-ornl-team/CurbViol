# Running PostgreSQL and loading data

docker on Mac, postgresql directory is not preserved between reruns

```
docker run --name "knxhx-postgis" -p 25432:5432 -d -t kartoza/postgis
psql -h localhost -U docker -p 25432 gis
```

## loading data

csvkit in python

### create environment
```
python3 -m venv knxhxenv
. ./knxhxenv/bin/activate
pip install csvkit psycopg2
```

### load the data

```
csvsql --db postgresql://docker:docker@localhost:25432/gis --tables violators curbside_violators_master_FAKE_DATA_011719.csv
```

columns H and I are empty and can be ignored


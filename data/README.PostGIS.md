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

# Launching connected geoserver

```
docker run --name "geoserver"  --link knxhx-postgis:postgis -p 8080:8080 -d -t -v $(pwd)/geoserver_data:/opt/geoserver/data_dir kartoza/geoserver
```
get WMS image as

```bash
curl 'http://localhost:8080/geoserver/knxhx/wms?service=WMS&version=1.1.0&request=GetMap&layers=knxhx:violations_jan2&styles=&bbox=-84.0586776733398,35.9098281860352,-83.8466720581055,36.0451049804688&width=768&height=490&srs=EPSG:404000&format=image%2Fpng'
```


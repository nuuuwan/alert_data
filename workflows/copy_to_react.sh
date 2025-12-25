DIR_REACT_DATA=$DIR_JS_REACT/alert/public/data/static/
for file in cities.json hospitals.json police_stations.json fire_stations.json; do
  cp data/static/$file $DIR_REACT_DATA/
done
ls -l $DIR_REACT_DATA
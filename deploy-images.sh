HOST=kornelro

docker build -t abm-0-data-preparation-activity-model 0-data-preparation/activity-model/.
docker tag abm-0-data-preparation-activity-model $HOST/abm-0-data-preparation-activity-model:latest
docker push $HOST/abm-0-data-preparation-activity-model:latest

docker build -t abm-0-data-preparation-facilities 0-data-preparation/facilities/.
docker tag abm-0-data-preparation-facilities $HOST/abm-0-data-preparation-facilities:latest
docker push $HOST/abm-0-data-preparation-facilities:latest

docker build -t abm-0-data-preparation-network 0-data-preparation/network/.
docker tag abm-0-data-preparation-network $HOST/abm-0-data-preparation-network:latest
docker push $HOST/abm-0-data-preparation-network:latest

docker build -t abm-0-data-preparation-traffic-counts 0-data-preparation/traffic-counts/.
docker tag abm-0-data-preparation-traffic-counts $HOST/abm-0-data-preparation-traffic-counts:latest
docker push $HOST/abm-0-data-preparation-traffic-counts:latest

docker build -t abm-1-simulation-activity-model 1-simulation/activity-model/.
docker tag abm-1-simulation-activity-model $HOST/abm-1-simulation-activity-model:latest
docker push $HOST/abm-1-simulation-activity-model:latest

docker build -t abm-1-simulation-population 1-simulation/population/.
docker tag abm-1-simulation-population $HOST/abm-1-simulation-population:latest
docker push $HOST/abm-1-simulation-population:latest

docker build -t abm-1-simulation-traffic-model 1-simulation/traffic-model/.
docker tag abm-1-simulation-traffic-model $HOST/abm-1-simulation-traffic-model:latest
docker push $HOST/abm-1-simulation-traffic-model:latest

docker build -t abm-2-post-processing 2-post-processing/.
docker tag abm-2-post-processing $HOST/abm-2-post-processing:latest
docker push $HOST/abm-2-post-processing:latest
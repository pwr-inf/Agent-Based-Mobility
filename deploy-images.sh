docker build -t abm-0-data-preparation-activity-model 0-data-preparation/activity-model/.
docker tag abm-0-data-preparation-activity-model kornelro/abm-0-data-preparation-activity-model:latest
docker push kornelro/abm-0-data-preparation-activity-model:latest

docker build -t abm-0-data-preparation-facilities 0-data-preparation/facilities/.
docker tag abm-0-data-preparation-facilities kornelro/abm-0-data-preparation-facilities:latest
docker push kornelro/abm-0-data-preparation-facilities:latest

docker build -t abm-0-data-preparation-network 0-data-preparation/network/.
docker tag abm-0-data-preparation-network kornelro/abm-0-data-preparation-network:latest
docker push kornelro/abm-0-data-preparation-network:latest
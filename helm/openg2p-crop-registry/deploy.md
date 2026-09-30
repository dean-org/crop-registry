helm dependency build .

helm dependency list .

helm lint .

helm template crop-registry .

helm install crop-registry . \
  --namespace dev \
  --create-namespace \
  --set global.registryHostname=crop-registry.dev.openg2p.test \
  --set registry.staffApi.image.repository=dharanidharan0411/openg2p-crop-registry-staff-api \
  --set registry.staffApi.image.tag=0.0.0-main.5 \
  --set registry.partnerApi.image.repository=dharanidharan0411/openg2p-crop-registry-partner-api \
  --set registry.partnerApi.image.tag=0.0.0-main.5 \
  --set registry.celeryWorker.image.repository=dharanidharan0411/openg2p-crop-registry-celery \
  --set registry.celeryWorker.image.tag=0.0.0-main.5 \
  --set registry.celeryBeat.image.repository=dharanidharan0411/openg2p-crop-registry-celery \
  --set registry.celeryBeat.image.tag=0.0.0-main.5 \
  --set registry.dbSeed.image.repository=dharanidharan0411/openg2p-crop-registry-db-seed \
  --set registry.dbSeed.image.tag=0.0.0-main.5

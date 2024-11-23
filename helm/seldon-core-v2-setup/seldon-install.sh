

helm repo add seldon-charts https://seldonio.github.io/helm-charts
helm repo update seldon-charts

helm install seldon-core-v2-crds  seldon-charts/seldon-core-v2-crds
# install example server
# helm install seldon-v2-servers seldon-charts/seldon-core-v2-servers 

minikube start  --memory no-limit --cpus no-limit
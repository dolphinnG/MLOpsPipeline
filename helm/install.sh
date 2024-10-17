#bin/bash


helm repo add jetstack https://charts.jetstack.io --force-update

helm install \
  cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --set crds.enabled=true --wait


helm upgrade trust-manager jetstack/trust-manager \
  --install \
  --namespace cert-manager \
  --wait


#   kubectl get crd | grep cert-manager | awk '{print $1}' | xargs kubectl delete crd
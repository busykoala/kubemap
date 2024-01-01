# Kube Map

Execute ephemeral pods for each pod in a cluster.

```
export SERVER=$(kubectl config view -o jsonpath="{.clusters[?(@.name=='$(kubectl config current-context)')].cluster.server}")
export TOKEN=$(kubectl get secret ephemeral-token -o jsonpath='{.data.token}' | base64 -d)
poetry install
poetry run python cli.py
```

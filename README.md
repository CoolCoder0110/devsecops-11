# DevSecOps Demo

## 1. Arkitekturöversikt
För presentationen, här är en övergripande bild av hur kodresan och klustret är uppsatt (Zero Trust, DevSecOps Lifecycle):

```mermaid
graph TD;
    A[Utvecklare] -->|Push kod till Main| B(GitHub Repository)
    B -->|Triggar Pipeline| C[GitHub Actions CI/CD]
    
    subgap CI [Pipeline Checks]
        C -->|1. SAST Scan| D{Bandit Python}
        D -->|Ok| E[2. Bygg Docker Image]
        E -->|3. SBOM| F[Generera & Ladda upp CycloneDX]
        F -->|4. Container Scan| G{Trivy Scanner}
    end

    G -->|Allt Grönt| H(Deploy till Kubernetes)

    subgraph K8s [Kubernetes Kluster]
        H --> I{OPA Gatekeeper Check}
        I -->|Kräver 'team' label| J[Namespace: nissastigen]
        J --> K[Deployment: Rootless, Read-Only]
        J --> L[Network Policy: Default Deny]
        K --> M[Prometheus Exporter]
    end
```

## Stack
- Python (Flask)
- Docker (Alpine bygge)
- Kubernetes (RBAC, NetworkPolicies, OPA Gatekeeper)
- Prometheus & Grafana (Monitoring)

## Run locally

docker build -t devsecops-demo:latest .
docker run -p 5000:5000 devsecops-demo

## Kubernetes

Skapa först namespacet och policyerna:
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/rbac.yaml
kubectl apply -f k8s/network-policy.yaml

Börja sedan med deploymenten:
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

kubectl port-forward -n nissastigen service/devsecops-demo-service 8080:5000

Open:
http://localhost:8080

## Scale

kubectl scale deployment devsecops-demo -n nissastigen --replicas=2

## Logs

kubectl logs deployment/devsecops-demo -n nissastigen

## 5. Monitoring & Operations (Presentation)
För att visa **Dashboards och Alerts** under demon, är applikationen nu utrustad med `prometheus-flask-exporter` som exponerar alla metrics (`/metrics`).

1. **Installera Prometheus & Grafana (Helm):**
   ```bash
   helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
   helm repo update
   # Installera hela stacken snabbt lokalt för demonstration
   helm install prometheus prometheus-community/kube-prometheus-stack -n monitoring --create-namespace
   ```
2. **Accessa Grafana Dashboard:**
   ```bash
   kubectl port-forward service/prometheus-grafana -n monitoring 3000:80
   # Inloggning (standard): admin / prom-operator
   ```
3. **Generera incident data för Demon:**
   Gå till [http://localhost:8080/error](http://localhost:8080/error) ett par gånger. Detta kommer ge en *HTTP 500* vilket i en riktig produktionsmiljö fångas upp av Prometheus, visas i Grafana och skapar ett **Alert** till jourhavande tekniker i t.ex. Slack/PagerDuty.

## Presentation Outline

1. **Arkitekturöversikt** — vad ni byggt och hur det hänger ihop
2. **CI/CD Pipeline** — GitHub Actions, builds, scanning
3. **Kubernetes & Deployment** — kluster, namespaces, manifests
4. **Säkerhet** — RBAC, policies, container hardening, supply chain
5. **Monitoring & Operations** — dashboards, alerts, incident hantering
6. **Live Demo** — visa det fungerande systemet

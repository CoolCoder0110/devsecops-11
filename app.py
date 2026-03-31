from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# Lägg till en statisk labels-metrik
metrics.info('app_info', 'Application info', version='1.0.0')

@app.route("/")
def home():
    return "Hello DevSecOps"

@app.route("/health")
def health():
    return {"status": "ok"}

@app.route("/error")
def trigger_error():
    # En endpoint bara för att kunna testa Alerts
    return {"status": "error", "message": "Simulerat fel under demo!"}, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
